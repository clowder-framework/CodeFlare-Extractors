FROM python:3.8 

WORKDIR /extractor
COPY requirements.txt ./
RUN apt-get update && apt-get --yes install libsndfile1
RUN pip install -r requirements.txt

RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8
COPY huggingface_parallel_ml_inference_extractor.py extractor_info.json ./
CMD python3 -u huggingface_parallel_ml_inference_extractor.py --heartbeat 15