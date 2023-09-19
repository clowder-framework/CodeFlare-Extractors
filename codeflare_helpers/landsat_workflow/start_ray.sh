#!/bin/bash

# ssh into remote client and execute commands remotely
ssh kastanday@dt-login02.delta.ncsa.illinois.edu 'zsh -s' << EOF
source ~/.zshrc
conda activate ray_py38
ray start
echo "Ray started, exiting."
EOF

# port forward from local to NCSA.
# ssh -l kastanday \
#   -L localhost:8265:cn005.delta.internal.ncsa.edu:8265 dt-login02.delta.ncsa.illinois.edu