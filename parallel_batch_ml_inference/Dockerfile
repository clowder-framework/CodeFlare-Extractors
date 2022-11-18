FROM python:3.8 
# any python version should work

WORKDIR /extractor
COPY requirements.txt ./
RUN apt-get update && apt-get --yes install libsndfile1
RUN pip install -r requirements.txt

COPY parallel_ml_inference_extractor.py extractor_info.json ./
CMD python parallel_ml_inference_extractor.py