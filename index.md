
# Welcome to CodeFlare-Clowder Extractor Examples and Tamplates
The CodeFlare-Clowder Template Extractors are a set of extractors that can be used to extract metadata from a variety of file types. The extractors are written in Python and are designed to be run in the Clowder environment. The extractors are available on GitHub at [CodeFlare-Extractors](https://github.com/clowder-framework/CodeFlare-Extractors). NOTE: Make sure this file is on Clowder folder

```shell
# Clone the repo if it doesn't exist
if [ ! -d "./CodeFlare-Extractors" ] 
then 
    git clone git@github.com:clowder-framework/CodeFlare-Extractors.git
fi
# start docker if it's not running
./CodeFlare-Extractors/test_bash.sh

if ! pgrep -f Docker.app > /dev/null; then
    echo "Starting Docker... please hang tight while it get's started for you."
    open -a "Docker"
    while ! docker ps > /dev/null 2>&1; do
        sleep 1
    done
    echo "✅ Docker is now running"
elif [ $(uname) = "Linux" ]; then
    sudo service docker start
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
    
    # no sudo for mac Docker, yes sudo for linux.
    # Todo: just use default browser, not specific ones on mac. 
    echo "Starting Clowder with extractors"
    if [ $(uname) = "Darwin" ]; then
        docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
        echo "🌐 Starting Clowder (http://localhost:8000) in your default browser"
        open http://localhost:8000
        echo "❓ It may take up to a minute for the containers to start up, please try refreshing the page a few times."

    elif [ $(uname) = "Linux" ]; then
        sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
        echo "Starting Firefox to appropriate Clowder URL: http://localhost:8000"
        firefox http://localhost:8000
    fi
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
    
    # no sudo for mac Docker, yes sudo for linux.
    echo "Starting Clowder with extractors"
    if [ $(uname) = "Darwin" ]; then
        docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
        echo "Starting Chrome to appropriate Clowder URL: http://localhost:8000"
        open -a "Google Chrome" http://localhost:8000
    elif [ $(uname) = "Linux" ]; then
        sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
        echo "Starting Firefox to appropriate Clowder URL: http://localhost:8000"
        firefox http://localhost:8000
    fi
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

    # no sudo for mac Docker, yes sudo for linux.
    echo "Starting Clowder with extractors"
    if [ $(uname) = "Darwin" ]; then
        docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
        echo "Starting Chrome to appropriate Clowder URL: http://localhost:8000"
        open -a "Google Chrome" http://localhost:8000
    elif [ $(uname) = "Linux" ]; then
        sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
        echo "Starting Firefox to appropriate Clowder URL: http://localhost:8000"
        firefox http://localhost:8000
    fi
    ```

=== "🛠   Make your own from a template"
    Doing ML data preprocessing? Have custom code to run over every file in your dataset? Use this template to get started.
    ```shell
    echo "👉 Please see ./CodeFlare-Extractors/template_for_custom_parallel_batch_extractors for a example & quickstart template"
    ```
