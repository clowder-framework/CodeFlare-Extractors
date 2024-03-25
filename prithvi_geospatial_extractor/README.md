# This extractor is best run via CodeFlare, see the top-level README for more. 

# Manual Docker (no CodeFlare)

This extractor is ready to be run as a docker container, the only dependency is a running Clowder instance. Simply build and run.

1. Start Clowder. For help starting Clowder, see our [getting started guide](https://github.com/clowder-framework/clowder/blob/develop/doc/src/sphinx/userguide/installing_clowder.rst).

2. First build the extractor Docker container:

```
# from this directory, run:

docker build -t prithvi-finetuned-extractor .
```

3. Finally run the extractor:

```
docker run -t -i --rm --net clowder_clowder -e "RABBITMQ_URI=amqp://guest:guest@rabbitmq:5672/%2f" --name "prithvi-finetuned-extractor" prithvi-finetuned-extractor
```

Then open the Clowder web app and run the wordcount extractor on a .txt file (or similar)! Done.

### Python and Docker details

You may use any version of Python 3. Simply edit the first line of the `Dockerfile`, by default it uses `FROM python:3.8`.

Docker flags:

- `--net` links the extractor to the Clowder Docker network (run `docker network ls` to identify your own.)
- `-e RABBITMQ_URI=` sets the environment variables can be used to control what RabbitMQ server and exchange it will bind itself to. Setting the `RABBITMQ_EXCHANGE` may also help.
  - You can also use `--link` to link the extractor to a RabbitMQ container.
- `--name` assigns the container a name visible in Docker Desktop.

## Troubleshooting

**If you run into _any_ trouble**, please reach out on our Clowder Slack in the [#pyclowder channel](https://clowder-software.slack.com/archives/CNC2UVBCP).

Alternate methods of running extractors are below.

# Commandline Execution

To execute the extractor from the command line you will need to have the required packages installed. It is highly recommended to use python virtual environment for this. You will need to create a virtual environment first, then activate it and finally install all required packages.

```
virtualenv /home/clowder/virtualenv/clowder2
. /home/clowder/virtualenv/clowder2/bin/activate
cd prithvi_finetune_extractor/
pip install -e .
```

To start the extractor you will need to load the virtual environment and start the extractor.

```
. /home/clowder/virtualenv/wordcount/bin/activate
/home/clowder/extractors/wordcount/prithvi_finetune_extractor.py
```
