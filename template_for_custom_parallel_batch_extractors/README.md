# This extractor is best run via CodeFlare, see the top-level README for usage instructions.


# Run Manually in Docker (without CodeFlare)

This extractor is ready to be run as a docker container, the only dependency is a _currently running_ Clowder instance. Simply build and run this extractor, to use it in Clowder.

1. Start Clowder. For help starting Clowder, see our [getting started guide](https://github.com/clowder-framework/clowder/blob/develop/doc/src/sphinx/userguide/installing_clowder.rst).

2. First build the extractor Docker container:

```
# from this directory, run:

docker build -t your_docker_container_name_here .
```

3. Finally run the extractor:

```
docker run -t -i --rm --net clowder_clowder -e "RABBITMQ_URI=amqp://guest:guest@rabbitmq:5672/%2f" --name "wordcount" your_docker_container_name_here
```

Then open the Clowder web app and run the wordcount extractor on a .txt file (or similar)! Done.

### Python and Docker details

You may use any version of Python 3. Simply edit the first line of the `Dockerfile`, by default it uses `FROM python:3.8`.

Intro to Docker flags:

- `--net` links the extractor to the Clowder Docker network (run `docker network ls` to identify your own.)
- `-e RABBITMQ_URI=` sets the environment variables can be used to control what RabbitMQ server and exchange it will bind itself to. Setting the `RABBITMQ_EXCHANGE` may also help.
  - You can also use `--link` to link the extractor to a RabbitMQ container.
- `--name` assigns the container a name visible in Docker Desktop.

## Troubleshooting

**If you run into _any_ trouble**, please reach out on our Clowder Slack in the [#pyclowder channel](https://clowder-software.slack.com/archives/CNC2UVBCP).
