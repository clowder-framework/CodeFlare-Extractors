FROM python:3.8

WORKDIR /extractor
COPY requirements.txt ./
RUN apt-get update && apt-get --yes install libsndfile1
RUN pip install -r requirements.txt

COPY wav-extractor.py extractor_info.json ./
CMD python wav-extractor.py