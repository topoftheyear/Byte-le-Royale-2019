import os
import click
import requests
from requests.auth import HTTPBasicAuth

from validate import validate


@click.group()
def cli():
    pass


@cli.command()
@click.option("--server-verbose", is_flag=True)
@click.option("--port", default=8080)
@click.option("--no-wait", is_flag=True, help="Prevents server from waiting on client response for longer than configured turn time.")
@click.option("--connection-wait-timer", default=3, help="Number of seconds to wait for clients to connect to server after the first has connected.")
@click.option("--wait-timeout", default=-1, help="Number of seconds to wait for the first client to connect to the server.")
def server(server_verbose, port, no_wait, connection_wait_timer, wait_timeout):
    from game.server import start

    if server_verbose:
        print("Server Verbosity: ON")

    start(server_verbose, port, no_wait, connection_wait_timer, wait_timeout)


@cli.command()
@click.option("--client-verbose", is_flag=True)
@click.option("--script", default="custom_client")
@click.option("--port", default=8080)
@click.option("--host", default="127.0.0.1")
def client(client_verbose, script, port, host):
    import importlib

    from game.client import start
    from game.client.client_logic import ClientLogic

    if client_verbose:
        print("Client Verbosity: ON")

    import importlib.util
    import os

    script = os.getcwd() + "/" + script + ".py"

    with open(script, "r") as f:
        script_text = f.read()
    if not validate(script_text):
        print("Client script failed to validate. Please fix any illegal imports and try again.")
        exit()


    spec = importlib.util.spec_from_file_location("custom_client", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    #mod = importlib.import_module(script)


    start(ClientLogic(client_verbose, module.CustomClient()), client_verbose, port, host)


@cli.command()
def generate():
    from game.utils.generate_game import generate as gen_data
    gen_data()


@cli.command()
@click.option("--verbose", is_flag=True)
@click.option("--log-path", default="./game_log")
@click.option("--gamma", default=1.0)
@click.option("--dont-wait", is_flag=True)
@click.option("--fullscreen", is_flag=True)
@click.option("--team-name", default=None)
def visualizer(verbose, log_path, gamma, dont_wait, fullscreen, team_name):
    from game.visualizer import start
    start(verbose, log_path, gamma, dont_wait, fullscreen, team_name)


@cli.command()
def update():
    # check version number
    import version
    current_version = version.v

    # check latest release version
    auth = HTTPBasicAuth("byte-le-royale-slave", "21b9b335294445199026eda76431621251886775")
    payload = requests.get("https://api.github.com/repos/topoftheyear/Byte-le-Royale-2019/releases/latest", auth=auth)


    if payload.status_code == 200:
        json = payload.json()
        remote_version = json["tag_name"]
        asset_id = json["assets"][0]["id"]
    else:
        print("There was an issue attempting to update: Bad Request: \"{0}\"".format(payload.body))
        exit()

    try:
        remote_version = float(remote_version)
    except:
        print("There was an issue attempting to update: Invalid remote version: \"{0}\"".format(remote_version))
        exit()

    if current_version >= remote_version:
        print("Launcher is up to date.")
        exit()

    print("There is a new version availiable: v{0}. Downloading update!".format(remote_version))

    from update_utils import download_file

    import os
    import shutil

    if not os.path.exists("br_updates"):
        os.makedirs("br_updates")

    remote_url = "https://api.github.com/repos/topoftheyear/Byte-le-Royale-2019/releases/assets/{0}".format(asset_id)
    local_file = "br_updates/v{0}.pyz".format(remote_version)

    if not download_file(local_file, remote_url, auth):
        print("Update failed, please try again later.")
        exit()

    old_file = "br_launcher.pyz"
    print("Replacing {0} with updated launcher.".format(old_file))
    shutil.copyfile(local_file, old_file)

    print("Update complete!")



@cli.command()
def version():
    # check version number
    import version
    print("Current version is: v{0}".format(version.v))

@cli.command()
@click.option("--client-verbose", is_flag=True)
@click.option("--server-verbose", is_flag=True)
@click.option("--client-script", default="custom_client")
@click.option("--port", default=8080)
@click.option("--server-no-wait", is_flag=True)
def run(client_verbose, server_verbose, client_script, port, server_no_wait):
    import subprocess

    import signal
    import sys
    import time
    import functools


    # Prep server args
    server_args = ["./br_launcher.pyz", "server"]

    if server_verbose:
        server_args.append("--server-verbose")
    if server_no_wait:
        server_args.append("--no_wait")
    server_args.extend(["--port", str(port)])


    # Prep client args
    client_args = ["./br_launcher.pyz", "client"]

    if client_verbose:
        client_args.append("--client-verbose")
    client_args.extend(["--script", client_script])
    client_args.extend(["--port", str(port)])

    # Ctrl + C (sigint) handler
    def signal_handler(server_proc, client_proc, sig, frame):
        print('\nCtrl+C - Exiting!')

        try:
            server_proc.kill()
        except:
            pass

        try:
            client_proc.kill()
        except:
            pass

        sys.exit(0)

    # start server
    server_proc = subprocess.Popen(server_args)

    time.sleep(1)

    # start client
    client_proc = subprocess.Popen(client_args)

    # build sigint handler, and register
    signal_handler = functools.partial(signal_handler, server_proc, client_proc)
    signal.signal(signal.SIGINT, signal_handler)

    client_proc.wait()
    server_proc.wait()


host = os.getenv("BL_ROYALE_HOST",  "scrimmage.royale.ndacm.org")

@cli.group()
def scrim():
    pass


@scrim.command()
def ui():
    from scrimmage import run_scrimmage_ui
    run_scrimmage_ui()


admin_password = os.getenv("BL_ROYALE_ADMIN_PASSWORD", False)
if admin_password:
    @scrim.group()
    def admin():
        pass

    @admin.group()
    def announcements():
        pass

    @announcements.command("add")
    @click.argument("title")
    @click.argument("message")
    def add_announcement(title, message):
        auth = HTTPBasicAuth("BL_ROYALE_ADMIN", admin_password)
        payload = requests.post("http://" + host + "/announcements", auth=auth, json={
            "title": title,
            "message": message
        })

        if payload.status_code != 200 :
            click.echo("An error occurred " + payload.raw)
        else:
            click.echo("Successfully added announcement")

    @announcements.command("clear")
    def clear_announcements():
        auth = HTTPBasicAuth("BL_ROYALE_ADMIN", admin_password)
        payload = requests.delete("http://" + host + "/announcements?all=true", auth=auth)

        if payload.status_code != 200 :
            click.echo("An error occurred " + payload.raw)
        else:
            click.echo("Successfully cleared announcements")








if __name__ == "__main__":
    cli()
