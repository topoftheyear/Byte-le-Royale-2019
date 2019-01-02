import os
import click
import requests
from requests.auth import HTTPBasicAuth

@click.group()
def cli():
    pass

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
        print("There was an issue attempting to update: Bad Request: \"{0}\"".format(payload.text))
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


if __name__ == "__main__":
    cli()
