import requests
from requests.auth import HTTPBasicAuth
import docker
import time
import os
import uuid
import sys
import tempfile
import tarfile
import json
import shutil


class Config:
    API_HOST = "http://localhost:5000"
    UPLOAD_DIR = "uploads"
    GAME_LOG_LOCATION = "game_logs.tar.gz"
    DOCKER_IMAGE_SERVER = "br_server"
    DOCKER_IMAGE_CLIENT = "br_client"
    RESULT_FILE = "results.json"
    MAX_TIMEOUT = 5


class ScrimmageRunner:
    def __init__(self):

        if not os.path.exists(Config.UPLOAD_DIR):
                os.makedirs(Config.UPLOAD_DIR)

        if not os.path.exists(Config.GAME_LOG_LOCATION):
                os.makedirs(Config.GAME_LOG_LOCATION)

        self.auth = HTTPBasicAuth("BL_ROYALE_ADMIN", "bl_royale_admin_123")
        self.client_metadata = {}

        self.server_node = None
        self.client_nodes = {}
        self.docker_client = docker.from_env()

        self.run_id = 0



    def work(self):


        # Get latest batch of clients
        self.clear_clients()
        self.clear_logs()

        clients = self.get_clients()
        if not clients: return

        # increment run id
        self.run_id += 1


        num_clients = len(clients["teams"])
        print("Clients submitted: ", num_clients)

        self.persist_clients(clients["teams"])

        print("Starting Server")
        results = self.start_server()

        print("Starting Clients")
        self.start_clients()

        print("Waiting for server to exit...")
        run_success = self.wait_for_server()
        if not run_success:
            self.docker_remove_container("bl_server")
            return

        self.pull_server_data()
        self.pull_client_data()

        self.docker_remove_container("bl_server")

        self.send_results(results)


    def get_clients(self):
        response = requests.get(
                Config.API_HOST + "/submissions",
                auth=self.auth)

        if response.status_code != 200:
            print(response.text)
            return None
        else:
            return response.json()


    def clear_clients(self):
        for file in os.listdir(Config.UPLOAD_DIR):
            file_path = os.path.join(Config.UPLOAD_DIR, file)
            try:
                os.unlink(file_path)
            except Exception as e:
                print(e)

        self.client_metadata.clear()


    def persist_clients(self, data):

        for team_data in data:


            client_id = str(uuid.uuid4())
            client_path = os.path.join(Config.UPLOAD_DIR, client_id + ".py")

            self.client_metadata[team_data["team_name"]] = {
                "client_id": client_id,
                "log": ""
            }

            with open(client_path, "w") as f:
                f.write(team_data["client_data"])


    def start_server(self):
        try:
            self.server_node = self.docker_client.containers.run(
                    Config.DOCKER_IMAGE_SERVER,
                    name="bl_server",
                    network="bl_net",
                    detach=True)
        except Exception as e:
            print("Exception: ", e)
            if self.server_node is not None:
                self.docker_remove_container("bl_server")
            exit()

    def docker_remove_container(self, name):
        server = self.docker_client.containers.get(name)
        server.stop()
        server.remove()



    def start_clients(self):
        for team_name, metadata in self.client_metadata.items():
            client_file = metadata["client_id"] + ".py"

            path = os.path.abspath(
                    os.path.join(Config.UPLOAD_DIR, client_file))

            self.client_nodes[team_name] = self.docker_client.containers.run(
                    Config.DOCKER_IMAGE_CLIENT,
                    detach=True,
                    network="bl_net",
                    mounts=[
                        docker.types.Mount(
                            target="/code/custom_client.py",
                            source=path,
                            type="bind",
                            read_only=True)
                    ])



    def wait_for_server(self):
        self.server_node.wait()


    def pull_server_data(self):
        # clean up now that we are done waiting for server

        # copy results file out
        results = self.docker_get_file(
                self.server_node,
                "/code/" + Config.RESULT_FILE)

        print(results)
        results = json.loads(results)

        self.docker_get_dir(
                self.server_node,
                "/code/game_log",
                Config.GAME_LOG_LOCATION)

        return results


    def pull_client_data(self):
        for team_name, node in self.client_nodes.items():
            text = node.logs().decode("utf-8")
            self.client_metadata[team_name]["log"] = text


    def send_results(results):
        # send server data
        requests.post(
                Config.API_HOST + "/report/results",
                auth=self.auth,
                json=results)

        # send game logs
        with open(Config.GAME_LOG_LOCATION, "r") as f:
            data = f.read()

        requests.post(
                Config.API_HOST + "/report/results",
                auth=self.auth,
                json={
                    "file_data": data
                })

        del data

        # send client logs
        for team_name, metadata in self.client_metadata.items():
            requests.post(
                    Config.API_HOST + "/report/results",
                    auth=self.auth,
                    json={
                        "team_name": team_name,
                        "log": metadata["log"]
                    })


    def clear_logs(self):
        if os.path.exists(Config.GAME_LOG_LOCATION):
            shutil.rmtree(Config.GAME_LOG_LOCATION)

        if not os.path.exists(Config.GAME_LOG_LOCATION):
            os.makedirs(Config.GAME_LOG_LOCATION)


    def docker_get_file(self, node, file_name):
        raw_data = self.docker_client.api.get_archive(
                node.name,
                file_name)

        # save data stream to a temp file
        with tempfile.NamedTemporaryFile() as tmp:
            for chunk in raw_data[0]:
                tmp.write(chunk)

            tmp.seek(0)

            #extract temp file
            with tarfile.open(mode="r", fileobj=tmp) as tar:
                tar_info = tar.getmembers()[0]
                f = tar.extractfile(tar_info)
                data = f.read()
                print(data)
                return data


    def docker_get_dir(self, node, dir_name, extract_to):
        raw_data = self.docker_client.api.get_archive(
                node.name,
                dir_name)

        file_path = extract_to
        with open(file_path, "w") as f:
            for chunk in raw_data[0].stream():
                f.write(chunk)


if __name__ == "__main__":
    runner = ScrimmageRunner()

    while(True):
        runner.work()
        time.sleep(0.25)

