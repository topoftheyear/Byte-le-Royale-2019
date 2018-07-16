import math
import requests
from tqdm import  tqdm

def download_file(local_filename, url, auth):
    r = requests.get(url, auth=auth, stream=True, headers={
        "Accept": "application/octet-stream"
    })

    if r.status_code not in [200, 302]:
        return False


    total_size = int(r.headers.get('content-length', 0));
    block_size = 1024
    wrote = 0
    with open(local_filename, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")


    return True
