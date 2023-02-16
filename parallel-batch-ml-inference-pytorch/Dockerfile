# FROM huggingface/transformers-pytorch-cpu
FROM rayproject/ray-ml
# use -gpu to use Nvidia CUDA images, requires NGC Docker Runtime. 

### TODO: use non-ray image, and use pre-build ray wheels. details in github issues.

WORKDIR /extractor
COPY requirements.txt ./
RUN sudo apt-get update && sudo apt-get -y install libsndfile1
RUN pip install -r requirements.txt
# RUN export LC_CTYPE=en_US.UTF-8
# RUN export LC_ALL=C.UTF-8
# RUN export LANG=C.UTF-8

COPY pytorch_parallel_ml_inference_extractor.py extractor_info.json imagenet_classes.txt ./
CMD ray start --head --port=10001 && python3 -u pytorch_parallel_ml_inference_extractor.py --heartbeat 15
