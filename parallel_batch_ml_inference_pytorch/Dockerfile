FROM huggingface/transformers-pytorch-cpu

WORKDIR /extractor
COPY requirements.txt ./
RUN apt-get update && apt-get --yes install libsndfile1
RUN pip install -r requirements.txt

COPY parallel_ml_inference_extractor.py extractor_info.json imagenet_classes.txt ./
CMD python3 parallel_ml_inference_extractor.py