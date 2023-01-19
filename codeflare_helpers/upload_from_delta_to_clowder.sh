#!/bin/bash

# ssh into remote client and execute commands remotely
ssh kastanday@dt-login03.delta.ncsa.illinois.edu 'bash -s' << EOF

# only do this if file exists.
#!/bin/bash

if test -e /u/kastanday/codeflare/upload_from_delta_to_clowder.py; then
    echo "upload_from_delta_to_clowder.py already exists, running it"
elif test ! -e /u/kastanday/codeflare/upload_from_delta_to_clowder.py; then
    # create python file with printf
    printf "
import inspect
import os
import traceback

import pyclowder
import pyclowder.datasets
import pyclowder.files


def upload_from_delta_to_clowder():
    # clowder_url = 'https://clowder.ncsa.illinois.edu/clowder'

    # todo, get path from user input
    path_to_file_or_dir = '/scratch/bbou/kastanday/results_to_upload'
    filepath_list = collect_files(path_to_file_or_dir)

    clowder_url = 'http://localhost:8000/'
    clowder_key = 'bbe2dce9-c3eb-4188-8a70-1d6e676beeb1'
    dataset_id = '63c1f967e4b09676b09e58e1'

    client = pyclowder.datasets.ClowderClient(host=clowder_url, key=clowder_key)
    for file in filepath_list:
        print('    ⏫ Uploading:', file)
        try:
            file_id = client.post_file(f'/uploadToDataset/{dataset_id}', file)
        except Exception as e:
            print(f'❌❌ Error in {inspect.currentframe().f_code.co_name}: {e}')
            print(traceback.print_exc())
    print('    ✅ Done uploading')


def collect_files(path):
    all_files = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                all_files.append(os.path.join(root, file))
    else:
        pass # {path} is not a directory, should be a single file.
    return all_files


if __name__ == '__main__':
    upload_from_delta_to_clowder()
    " >> /u/kastanday/codeflare/upload_from_delta_to_clowder.py
else
    echo "Something went wrong checking if file exists"
fi

# ensure pyclowder is installed 
# pip install pyclowder

# execute python script
python /u/kastanday/codeflare/upload_from_delta_to_clowder.py

# echo "completed job, exiting."

EOF
