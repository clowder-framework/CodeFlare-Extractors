
# Welcome to CodeFlare-Clowder Extractor Examples and Tamplates
The CodeFlare-Clowder Template Extractors are a set of extractors that can be used to extract metadata from a variety of file types. The extractors are written in Python and are designed to be run in the Clowder environment. The extractors are available on GitHub at [CodeFlare-Extractors](https://github.com/clowder-framework/CodeFlare-Extractors). NOTE: Make sure this file is on Clowder folder

```shell
if [ ! -d "./CodeFlare-Extractors" ] 
then 
    git clone git@github.com:clowder-framework/CodeFlare-Extractors.git
fi
if [[ $(uname -m) == 'arm64' ]]; then
  echo "⚠️  ERROR: These demos will NOT work on Apple Silicon (or arm64) because of the Tensorflow model being used. But you can still edit these demos to fit your needs for any parallel extractors. These demos are a great starting point.\n"
fi
```

=== "🏎   Pytorch -- Parallel Dataset Extractor -- run ML inference on whole dataset"
    This demo runs Tensorflow inference over every file in a dataset. Change it to fit your needs!

    ```shell
    cd CodeFlare-Extractors/parallel-batch-ml-inference-pytorch/

    # Build the image
    echo "Docker will likely require sudo password"s
    export DOCKER_DEFAULT_PLATFORM=linux/amd64  ## for better compatibility with M1. 
    docker build . -t parallel-batch-ml-inference-pytorch:latest

    # Add the image to Clowder docker-compose file
    cd ../../
    if ! grep parallel-batch-ml-inference-pytorch:latest -q docker-compose.extractors.yml; then
      printf '%s' '''
      parallel-batch-ml-inference-pytorch:
        image: parallel-batch-ml-inference-pytorch:latest
        restart: unless-stopped
        networks:_
          - clowder
        depends_on:
          - rabbitmq
          - clowder
        environment:
          - RABBITMQ_URI=${RABBITMQ_URI:-amqp://guest:guest@rabbitmq/%2F}
      ''' >> docker-compose.extractors.yml
    fi
    ```
    
    ```shell
    echo "Starting Clowder with extractors"
    echo "Docker will likely require sudo password"
    sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    ```

    Done!


=== "🏎   Tensorflow -- Parallel Dataset Extractor -- run ML inference on whole dataset"
    This demo runs Tensorflow inference over every file in a dataset. Change it to fit your needs!

    ```shell
    cd CodeFlare-Extractors/parallel_batch_ml_inference/

    # Build the image
    echo "Docker will likely require sudo password"s
    export DOCKER_DEFAULT_PLATFORM=linux/amd64  ## for better compatibility with M1. 
    docker build . -t parallel-batch-ml-inference-tensorflow:latest

    # Add the image to Clowder docker-compose file
    cd ../../
    if ! grep parallel-batch-ml-inference-tensorflow:latest -q docker-compose.extractors.yml; then
      printf '%s' '''
      parallel-batch-ml-inference-tensorflow:
        image: parallel-batch-ml-inference-tensorflow:latest
        restart: unless-stopped
        networks:_
          - clowder
        depends_on:
          - rabbitmq
          - clowder
        environment:
          - RABBITMQ_URI=${RABBITMQ_URI:-amqp://guest:guest@rabbitmq/%2F}
      ''' >> docker-compose.extractors.yml
    fi
    ```
    
    ```shell
    echo "Starting Clowder with extractors"
    echo "Docker will likely require sudo password"
    sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    ```

    Done!

=== "⏰  Event-Driven -- triggers when files are added to dataset"
    Even-driven extractors are perfect for when you upload data to Clowder via the REST API. This way, whenever you add files, you can run them through your ML inference, or whatever you want, post-processing. All in parallel, making full use of your hardware. Warning: Demo uses Tensorflow that is NOT compatible with Apple Silicon.

    ```shell
    cd CodeFlare-Extractors/event_driven_ml_inference/

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
        networks:
          - clowder
        depends_on:
          - rabbitmq
          - clowder
        environment:
          - RABBITMQ_URI=${RABBITMQ_URI:-amqp://guest:guest@rabbitmq/%2F}
      ''' >> docker-compose.extractors.yml
    fi

    sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    ```

=== "🛠   Make your own from a template"
    Doing ML data preprocessing? Have custom code to run over every file in your dataset? Use this template to get started.
    ```shell
    echo "👉 Please see ./CodeFlare-Extractors/template_for_custom_parallel_batch_extractors for a example & quickstart template"
    ```
