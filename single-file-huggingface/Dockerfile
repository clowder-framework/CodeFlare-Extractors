## USAGE: 
# 1. Build
# docker build -t kastanday/huggingface-single-file-extractor .
# 2. Run (with clowder in full development mode.)
# docker run -t -i --rm --net clowder2_clowder2 \
#   -e CLOWDER_URL=http://host.docker.internal:80/ \
#   -e "CLOWDER_VERSION=2" \
#   -e RABBITMQ_URI="amqp://guest:guest@clowder2-rabbitmq-1:5672/%2F" \
#   --shm-size=2.17gb \
#   --name huggingface-extractor-aarch64-4 \
#   kastanday/huggingface-single-file-extractor

FROM python:3.8 

WORKDIR /extractor
COPY requirements.txt ./
RUN apt-get update && apt-get --yes install libsndfile1
RUN pip install -r requirements.txt

RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8
COPY single_file_huggingface.py extractor_info.json ./
CMD python3 -u single_file_huggingface.py --max-retry 1 --heartbeat 5 --connector RabbitMQ