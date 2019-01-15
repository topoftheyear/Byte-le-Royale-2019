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


class Config:
    API_HOST = "http://localhost:5000"
    UPLOAD_DIR = "uploads"


class ScrimmageRunner:
    def __init__(self):

        if not os.path.exists(Config.UPLOAD_DIR):
                os.makedirs(Config.UPLOAD_DIR)

        self.auth = HTTPBasicAuth("BL_ROYALE_ADMIN", "bl_royale_admin_123")
        self.client_metadata = {}



    def work(self):

        # Get latest batch of clients
        self.clear_clients()

        clients = self.get_clients()
        if not clients: return


        num_clients = len(clients["teams"])

        self.persist_clients(clients["teams"])







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
        for file in os.lsdir(Config.UPLOAD_DIR):
            file_path = os.path.join(Config.UPLOAD_DIR, file)
            try:
                os.path.unlink(file_path)
            except Exception e:
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













if __name__ == "__main__":
    runner = ScrimmageRunner()

    while(True):
        runner.work()
        time.sleep(0.25)

