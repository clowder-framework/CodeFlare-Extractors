#!/bin/bash

# Build and push docker image
docker build -t kastanday/landsattrend2 --platform linux/amd64 CodeFlare-Extractors/codeflare_helpers/landsat_workflow
docker push kastanday/landsattrend2:latest

# ssh into remote client and execute commands remotely
# ssh kastanday@dt-login02.delta.ncsa.illinois.edu 'bash -s' << EOF
ssh kastanday@dt-login02.delta.ncsa.illinois.edu 'zsh -s' << EOF

source ~/.zshrc

apptainer pull docker://kastanday/landsattrend2:latest

# or use conda (instead of apptainer)
# conda activate landsattrend2

### Setup Ingmar's github ###
mkdir -p ~/codeflare_utils/landsat_workflow
cd ~/codeflare_utils/landsat_workflow

if [ ! -d "landsattrend" ]; then
  git clone git@github.com:initze/landsattrend.git
fi

cd landsattrend
git checkout dev4Clowder_Ingmar_deployed_delta

#### Run code ###
# step 1: Google Earth to Google Cloud Storage.

# step 2: GCS to HPC.

# step 4a - upload results to clowder. 
bash ~/codeflare_utils/landsat_workflow/landsattrend/import_export/upload_region_output.sh https://pdg.clowderframework.org/ 981ab4c8-7d22-418d-93a2-b47019c2f583 ALASKA /scratch/bbou/toddn/landsat-delta/landsattrend/process 649232e2e4b00aa1838f0fc2
echo "Completed Step 4a: 'upload_region_output.sh'"

# step 4b - upload results to clowder. 
bash ~/codeflare_utils/landsat_workflow/landsattrend/import_export/upload_region.sh https://pdg.clowderframework.org/ 981ab4c8-7d22-418d-93a2-b47019c2f583 ALASKA /scratch/bbou/toddn/landsat-delta/landsattrend/process 649232e2e4b00aa1838f0fc2
echo "Completed Step 4b: 'upload_input_regions'"

EOF