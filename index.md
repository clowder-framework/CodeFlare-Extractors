# Run a parallel Clowder file extractor via CodeFlare

NOTE: Make sure this file is on Clowder folder

# Clone the CodeFlare-Clowder Template Extractors

The CodeFlare-Clowder Template Extractors are a set of extractors that can be used to extract metadata from a variety of file types. The extractors are written in Python and are designed to be run in the Clowder environment. The extractors are available on GitHub at [CodeFlare-Extractors](https://github.com/clowder-framework/CodeFlare-Extractors).

```shell
if [ ! -d "./CodeFlare-Extractors" ] 
then 
    git clone git@github.com:clowder-framework/CodeFlare-Extractors.git
fi
```

=== "Bulk Dataset Extractor"
    ## Add the Bulk Dataset Extractor to the Clowder Environment Adding to Docker compose extractors.
    ```shell
    cd CodeFlare-Extractors/parallel_batch_ml_inference/

    # Build the image
    docker build . -t bulk-dataset-extractor:latest

    # Add the image to Clowder docker-compose file
    cd ../../
    if ! grep bulk-dataset-extractor:latest -q docker-compose.extractors.yml; then
      printf '%s' '''
      bulkdatasetextractor:
        image: bulk-dataset-extractor:latest
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
    ```

    ## Starting Clowder
    You may need to enter your sudo password for Docker.
    ```shell
    sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    ```

=== "Event-Driven, file-added extractor"
    ## Add the Bulk Dataset Extractor to the Clowder Environment Adding to Docker compose extractors.
    ```shell
    cd CodeFlare-Extractors/event_driven_ml_inference/

    # Build the image
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
    ```

    ## Starting Clowder
    You may need to enter your sudo password for Docker.
    ```shell
    sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
    ```

=== "Make your own from a template"
    ```shell
    ```



## Add the CodeFlare-Extractors to the Clowder Environment Adding to Docker compose extractors.
```shell
cd /home/phantuanminh/clowder/

if ! grep img-extractor:latest -q docker-compose.extractors.yml; then
  echo """
    imgextractor:
      image: img-extractor:latest
      restart: unless-stopped
      networks:
        - clowder
      depends_on:
        - rabbitmq
        - clowder
      environment:
        - RABBITMQ_URI=${RABBITMQ_URI:-amqp://guest:guest@rabbitmq/%2F}
  """ >> /home/phantuanminh/clowder/docker-compose.extractors.yml
fi
```

## Starting Clowder with a template extractor
You may need to enter your sudo password for Docker.

<!-- ```shell
cd /home/phantuanminh/clowder
sudo docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d
``` -->