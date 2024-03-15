## Notes for the environment

- Python version 3.9
- Files we will need
  - setup.py
  - geospatial_fm directory (this creates a package for easy code running)
  - model_inference.py (helper file for running the model)
- Install torch and torchvision
```bash
 pip install torch==1.11.0 torchvision==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu115
```
- Install setup.py
```bash
pip install -e .
```
- Install openmim
```bash
 pip install -U openmim
```
- Install mmcv-full
```bash
mim install mmcv-full==1.6.2 -f https://download.openmmlab.com/mmcv/dist/cu115/torch1.11.0/index.html
```