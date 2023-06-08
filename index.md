
# Welcome to CodeFlare-Clowder Extractor Examples and Tamplates
The CodeFlare-Clowder Template Extractors are a set of extractors that can be used to extract metadata from a variety of file types. The extractors are written in Python and are designed to be run in the Clowder environment. The extractors are available on GitHub at [CodeFlare-Extractors](https://github.com/clowder-framework/CodeFlare-Extractors). NOTE: Make sure this file is on Clowder folder

```shell
# todo: set the base path based on clowder path + CodeFlare-Extractors
export CODEFLARE_BASE_PATH=/Users/kastanday/code/ncsa/clean_clowder_no_edits/another/clowder/CodeFlare-Extractors

# Clone the repo if it doesn't exist
if [ ! -d "./CodeFlare-Extractors" ] 
then 
    git clone git@github.com:clowder-framework/CodeFlare-Extractors.git
fi

# start docker if it's not running
if ! pgrep -f Docker.app > /dev/null; then
    echo "Starting Docker... please hang tight while it get's started for you."
    open -a "Docker"
    while ! docker ps > /dev/null 2>&1; do
        sleep 1
    done
    echo "✅ Docker is now running"
elif [ $(uname) = "Linux" ]; then
    docker ps > /dev/null 2>&1
    if [ ! $? -eq 0 ]; then
        # docker is NOT running
        echo "Docker is running, please start Docker."
        # my attempts were unreliable... especially with WSL2.
        # sudo service docker start
        # sudo systemctl start docker
    fi 
fi
```

=== "🔥   Pytorch -- Parallel Dataset Extractor -- run ML inference on whole dataset"
    This demo runs Tensorflow inference over every file in a dataset. Change it to fit your needs!

    ```shell
    # Build the image
    echo "Docker will likely require your sudo password"
    docker build CodeFlare-Extractors/parallel-batch-ml-inference-pytorch/ -t parallel-batch-ml-inference-pytorch:latest --shm-size=3.5gb

    # Add the image to Clowder docker-compose file
    if ! grep parallel-batch-ml-inference-pytorch:latest -q docker-compose.extractors.yml; then
      printf '%s' '''
      parallel-batch-ml-inference-pytorch:
        image: parallel-batch-ml-inference-pytorch:latest
        restart: unless-stopped
        shm_size: '4gb'
        networks:
          - clowder
        depends_on:
          - rabbitmq
          - clowder
        environment:
          - RABBITMQ_URI=${RABBITMQ_URI:-amqp://guest:guest@rabbitmq/%2F}
      ''' >> docker-compose.extractors.yml
    fi
    
    # Launch script (docker compose up)
    bash ./CodeFlare-Extractors/codeflare_helpers/launch_clowder.sh
    ```


=== "🏎   Tensorflow -- Parallel Dataset Extractor -- run ML inference on whole dataset"
    This demo runs Tensorflow inference over every file in a dataset. Change it to fit your needs.

    ```shell
    # Build the image
    echo "Docker will likely require your sudo password"
    export DOCKER_DEFAULT_PLATFORM=linux/amd64  ## for better compatibility with M1. 
    docker build ./CodeFlare-Extractors/parallel_batch_ml_inference/ -t parallel-batch-ml-inference-tensorflow:latest

    # Add the image to Clowder docker-compose file
    if ! grep parallel-batch-ml-inference-tensorflow:latest -q docker-compose.extractors.yml; then
      printf '%s' '''
      parallel-batch-ml-inference-tensorflow:
        image: parallel-batch-ml-inference-tensorflow:latest
        restart: unless-stopped
        shm_size: '4gb'
        networks:
          - clowder
        depends_on:
          - rabbitmq
          - clowder
        environment:
          - RABBITMQ_URI=${RABBITMQ_URI:-amqp://guest:guest@rabbitmq/%2F}
      ''' >> docker-compose.extractors.yml
    fi
    
    # Launch script (docker compose up)
    bash ./CodeFlare-Extractors/codeflare_helpers/launch_clowder.sh
    ```

    Done!

=== "🤗   Huggingface -- Parallel Dataset Extractor -- run ML inference on whole dataset"
    This demo runs Huggingface inference over every file in a dataset. Change it to fit your needs.

    ```shell
    # Build the image
    echo "Docker will likely require your sudo password"
    export DOCKER_DEFAULT_PLATFORM=linux/amd64  ## for better compatibility with M1. 
    docker build ./CodeFlare-Extractors/parallel-batch-ml-inference-huggingface/ -t parallel-batch-ml-inference-huggingface:latest

    # Add the image to Clowder docker-compose file
    if ! grep parallel-batch-ml-inference-huggingface:latest -q docker-compose.extractors.yml; then
      printf '%s' '''
      parallel-batch-ml-inference-huggingface:
        image: parallel-batch-ml-inference-huggingface:latest
        restart: unless-stopped
        shm_size: '4gb'
        networks:
          - clowder
        depends_on:
          - rabbitmq
          - clowder
        environment:
          - RABBITMQ_URI=${RABBITMQ_URI:-amqp://guest:guest@rabbitmq/%2F}
      ''' >> docker-compose.extractors.yml
    fi
    
    # Launch script (docker compose up)
    bash ./CodeFlare-Extractors/codeflare_helpers/launch_clowder.sh
    ```

    Done!

=== "⏰  Event-Driven -- triggers when files are added to dataset"
    Even-driven extractors are perfect for when you upload data to Clowder via the REST API. This way, whenever you add files, you can run them through your ML inference, or whatever you want, post-processing. All in parallel, making full use of your hardware. Warning: Demo uses Tensorflow that is NOT compatible with Apple Silicon.

    ```shell
    cd CodeFlare-Extractors/event_driven_ml_inference/

    echo "Docker will likely require your sudo password"
    # Build the image
    export DOCKER_DEFAULT_PLATFORM=linux/amd64  ## for better compatibility with M1. 
    docker build . -t event-driven-extractor:latest

    # Add the image to Clowder docker-compose file
    cd ../../
    if ! grep event-driven-extractor:latest -q docker-compose.extractors.yml; then
      printf '%s' '''
      eventdrivenextractor:
        image: event-driven-extractor:latest
        restart: unless-stopped
        shm_size: '4gb'
        networks:
          - clowder
        depends_on:
          - rabbitmq
          - clowder
        environment:
          - RABBITMQ_URI=${RABBITMQ_URI:-amqp://guest:guest@rabbitmq/%2F}
      ''' >> docker-compose.extractors.yml
    fi

    # Launch script (docker compose up)
    bash ./CodeFlare-Extractors/codeflare_helpers/launch_clowder.sh
    ```

=== "↔️  Move in and out of Clowder"
    You can import data from anywhere, and export data to anywhere. Just select a source, then a destination. First select your source files, then your destination location.

    ```shell
    bash ./CodeFlare-Extractors/codeflare_helpers/launch_clowder.sh
    ```

    ## Select the data you wish to transfer (data source)
    === "Source: Clowder Dataset"
        Select from available datasets in Clowder. This transfers the entire dataset, which is a recommended workflow.
        :import{CodeFlare-Extractors/codeflare_helpers/keys.md}

        After auth, collect the available datasets in Clowder. 
        ```shell
        python CodeFlare-Extractors/codeflare_helpers/ds.py
        ```

        ## Select the Clowder dataset you wish to transfer. 
            :import{CodeFlare-Extractors/codeflare_helpers/select_clowder_dataset.md}

            ## Select the destination location.
            :import{CodeFlare-Extractors/codeflare_helpers/data_movement_select_destination.md}
    
    === "Source: HPC"
        SSH to your HPC resource and copy data from any path there to any destination. You can supply a list of files, or a path to a directory. 
        ```shell
        echo "👉 Starting download_from_delta_to_clowder.sh"
        bash CodeFlare-Extractors/codeflare_helpers/download_from_delta_to_clowder.sh
        ```

        # Select the destination location.
        :import{CodeFlare-Extractors/codeflare_helpers/data_movement_select_destination.md}

        # Enter the Source path on HPC. Everything inside this directory will be copied to your destination.
        === "Enter the destination path on HPC (e.g. /home/user/data/) [default: ~/]"
            ```shell
            echo "👉 Selected destination path: ${choice}"
            # export HPC_DESTINATION_PATH=${choice}
            ```

    === "Source: AWS S3"
        Select from available buckets in AWS S3. Transfer the entire bucket, or a list of files. Ensure '$ aws s3 ls' works on your machine.
        ```shell
        echo "todo"
        ```
        
        # Select the source filepath you wish to copy from S3.
        === "Enter the source path on S3 (e.g. s3://my-bucket/data/destination/) [default: s3://my-bucket]"
            ```shell
            echo "👉 Selected destination path: ${choice}"
            # export HPC_DESTINATION_PATH=${choice}
            ```

            # Select the destination location.
            :import{CodeFlare-Extractors/codeflare_helpers/data_movement_select_destination.md}
    
    === "Source: Google Cloud Storage"
        Select from available buckets in Google Cloud Storage. Transfer the entire bucket, or a list of files. Ensure '$ gsutil ls' already works on your machine.
        ```shell
        echo "todo"
        ```
        
        # Select the source filepath you wish to copy from Google Cloud Storage.
        === "Enter the source path on S3 (e.g. gs://my-bucket/data/destination/) [default: gs://my-bucket]"
            ```shell
            echo "👉 Selected destination path: ${choice}"
            # export HPC_DESTINATION_PATH=${choice}
            ```

            # Select the destination location.
            :import{CodeFlare-Extractors/codeflare_helpers/data_movement_select_destination.md}

