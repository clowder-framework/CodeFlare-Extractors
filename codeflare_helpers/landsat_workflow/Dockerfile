
### USAGE ### 

#### FIRST: BUILD DOCKER (off HPC) ####
# 1. MUST be x64
# export DOCKER_DEFAULT_PLATFORM=linux/amd64
# 2.
# docker build -t kastanday/landsattrend2 .
# 3. 
# docker push kastanday/landsattrend2:latest

#### SECOND: Pull Apptainer (on HPC) ####
# 1. Pull and convert that image to a local .sif apptainer/singulairty file.
# apptainer pull kastanday/landsattrend2:latest
#   WARNING: Fast internet recommended. This takes a long time and uses significant disk space.

# use NGC images when ML is needed: FROM nvcr.io/nvidia/tensorflow:19.10-py3
FROM python:3.8

LABEL name="landsattrend2"
LABEL summary="Build a Docker / Apptainer image for landsattrend2."
LABEL URL="https://github.com/initze/landsattrend/blob/dev4Clowder_Ingmar_deployed_delta"
LABEL maintaner="Kastan Day"
LABEL architecture="x86_64"
LABEL version="0.1"
LABEL release-date="2023-06-30"

WORKDIR /app

# necessary for cv2 https://exerror.com/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directory/
# and gdal
RUN apt-get update && apt-get install -y \
  curl     \
  wget     \
  build-essential     \
  ffmpeg     \
  libsm6     \
  libxext6   \
  gdal-bin   \
  libgdal-dev     \
  && apt-get clean

# these args are untested, and probably unnecessary. Try adding if problems w gdal. 
# might need to switch ARG to ENV
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN python3 -m pip install --upgrade pip
RUN pip install \
  bottleneck \ 
  fiona==1.8.20 \ 
  gdal==3.3.2 \ 
  geopandas==0.9.0 \ 
  googledrivedownloader==0.4 \ 
  jupyter \ 
  notebook \ 
  pycaret \ 
  rasterio==1.2 \ 
  scikit-image==0.19.1 \ 
  netCDF4 \ 
  pyclowder 