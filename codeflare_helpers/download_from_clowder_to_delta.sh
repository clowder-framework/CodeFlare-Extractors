#!/bin/bash

# ssh into remote client and execute commands remotely
ssh kastanday@dt-login03.delta.ncsa.illinois.edu 'bash -s' << EOF

# todo here mkdir -p ~/codeflare_utils

# Create python file only if it doesn't already exist
if test ! -e /u/kastanday/codeflare/download_from_clowder_to_delta.py; then
    # create python file with printf
    printf "
import os
import shutil

import pyclowder.datasets
import requests

clowder_host = 'http://localhost:8000/'
clowder_key = 'bbe2dce9-c3eb-4188-8a70-1d6e676beeb1'
dataset_id = '63c1f967e4b09676b09e58e1'

client = pyclowder.datasets.ClowderClient(host=clowder_host, key=clowder_key)

def download_file_to_location(file_url, file_location):
    r = requests.get(file_url, stream=True)
    if r.ok:
        with open(file_location, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        pass

if __name__ == '__main__':
    dataset_files = client.get('/datasets/' + dataset_id + '/files')
    print('num files in dataset: ' + str(len(dataset_files)))
    path_to_download = '/scratch/bbou/kastanday/'
    for file in dataset_files:
        file_name = file['filename']
        file_id = file['id']
        download_url = clowder_host + 'api/files/' + file_id + '/blob?key=' + clowder_key
        location_to_download = os.path.join(path_to_download, file_name)
        # download_file = requests.get(download_url)
        try:
            print('    ⏬ Downloading from Clowder to local path:', location_to_download)
            with requests.get(download_url, stream=True) as r:
                with open(location_to_download, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            # download_file_to_location(download_url, location_to_download)
        except Exception as e:
            print('Error while downloading file', file_name)
            print(e)
    print('    ✅ Done downloading')
    " >> /u/kastanday/codeflare/download_from_clowder_to_delta.py
else
  echo "Something went wrong checking if file exists"
fi

# ensure pyclowder is installed 
# pip install pyclowder

# execute python script
python /u/kastanday/codeflare/download_from_clowder_to_delta.py

# echo "Completed job, exiting."

EOF
