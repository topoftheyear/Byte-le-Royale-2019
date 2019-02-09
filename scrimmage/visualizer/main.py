import subprocess
import sys
import requests
import time
import json
import tarfile
import os
import shutil
from requests.auth import HTTPBasicAuth


UNITY_VIS = False
FINALS = False
API_URL = "http://scrimmage.royale.ndacm.org:5000"
auth = HTTPBasicAuth("BL_ROYALE_ADMIN", "bl_royale_admin_123")

def main():

    if not FINALS:
        # clean up old files
        try: shutil.rmtree("game_log")
        except: pass

        try: os.unlink("game_data.json")
        except: pass

        try: os.unlink("results.json")
        except:pass

    if UNITY_VIS:
        visualizer_args = ["visualizer"]
    else:
        visualizer_args = ["vis/test.exe" ]
        #visualizer_args = [sys.executable, "br_launcher.pyz", "visualizer", "--dont-wait", ]
        #visualizer_args = [sys.executable, "br_launcher.pyz", "visualizer", "--dont-wait", "--fullscreen", ]

    while True:

        if not FINALS:
            print("Pulling latest scrimmage data.")
            response = requests.get(API_URL + "/report/game_logs", auth=auth)

            if response.status_code != 200:
                print(response.text)
                time.sleep(5) # wait a bit
                continue

            json_data = response.json()

            with open("game_data.json", "w") as f:
                f.write(json_data["game_data"])

            with open("results.json", "w") as f:
                f.write(json_data["results"])

            with open("game_log.tar", "wb") as f:
                f.write(json_data["log_data"].encode("utf-8"))

            print("Extracting game logs...")
            with tarfile.open("game_log.tar") as t:
                t.extractall(".")

            os.unlink("game_log.tar")

            print("Data loaded.")

        else:
            print("FINALS RUN, don't get latest.")



        print("Starting scrimmage playback")
        try:
            visualizer_proc = subprocess.Popen(visualizer_args, cwd="vis")
            visualizer_proc.wait()
        except KeyboardInterrupt:
            print("Ctrl + C detected, exiting...")
            exit(0)
        print("Scrimmage playback Finished")

        if not FINALS:
            print("Cleaning up files...")

            shutil.rmtree("game_log")
            os.unlink("game_data.json")
            os.unlink("results.json")


        time.sleep(2) # wait a bit



if __name__ == "__main__":
    main()
