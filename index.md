
# Welcome to CodeFlare-Clowder Extractor Examples and Tamplates
The CodeFlare-Clowder Template Extractors are a set of extractors that can be used to extract metadata from a variety of file types. The extractors are written in Python and are designed to be run in the Clowder environment. The extractors are available on GitHub at [CodeFlare-Extractors](https://github.com/clowder-framework/CodeFlare-Extractors). NOTE: Make sure this file is on Clowder folder

```shell
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

=== "🏎   Pytorch -- Parallel Dataset Extractor -- run ML inference on whole dataset"
    This demo runs Tensorflow inference over every file in a dataset. Change it to fit your needs!

    ```shell
    # Build the image
    echo "Docker will likely require your sudo password"
    export DOCKER_DEFAULT_PLATFORM=linux/amd64  ## for better compatibility with M1. 
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

=== "⏬   Download data from Clowder to HPC"
    This will SSH to your HPC resource, and ask where you want your data downloaded to. Takes care of port forwarding for you.
    ```shell
    echo "👉 Starting download_from_clowder_to_delta.sh"
    bash ./CodeFlare-Extractors/codeflare_helpers/download_from_clowder_to_delta.sh
    ```

=== "⏫   Upload data form HPC to Clowder"
    This will SSH to your HPC resource, ask for the local path to your data, and upload it to Clowder for you.
    ```shell
    echo "👉 Starting upload_from_delta_to_clowder.sh"
    bash ./CodeFlare-Extractors/codeflare_helpers/upload_from_delta_to_clowder.sh
    echo "🌐 Opening destination dataset in default browser (http://localhost:8000/datasets/63c1f967e4b09676b09e58e1)"
    open http://localhost:8000/datasets/63c1f967e4b09676b09e58e1
    ```


=== "🛠   Make your own from a template"
    Doing ML data preprocessing? Have custom code to run over every file in your dataset? Use this template to get started.
    ```shell
    echo "👉 Please see ./CodeFlare-Extractors/template_for_custom_parallel_batch_extractors for a example & quickstart template"
    ```
