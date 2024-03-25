#Source - https://huggingface.co/spaces/ibm-nasa-geospatial/Prithvi-100M-sen1floods11-demo/blob/main/Dockerfile

FROM python:3.8

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  wget \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user
# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH \
    PYTHONPATH=$HOME/app \
	PYTHONUNBUFFERED=1 \
	GRADIO_ALLOW_FLAGGING=never \
	GRADIO_NUM_PORTS=1 \
	GRADIO_SERVER_NAME=0.0.0.0 \
	GRADIO_THEME=huggingface \
	SYSTEM=spaces

# RUN conda install python=3.8

RUN pip install setuptools-rust
RUN pip install torch==1.11.0+cu115 torchvision==0.12.0+cu115 --extra-index-url https://download.pytorch.org/whl/cu115
RUN pip install gradio scikit-image pillow openmim
RUN pip install --upgrade setuptools

WORKDIR /home/user

WORKDIR /extractor

COPY . .

RUN pip install -e .

RUN mim install mmcv-full==1.6.2 -f https://download.openmmlab.com/mmcv/dist/11.5/1.11.0/index.html

CMD ["python3", "-u", "prithvi_finetuned_extractor.py", "--heartbeat", "15"]
