#!/usr/bin/env python
"""Parallel Machine Learning Extractor"""
from mmcv import Config

from mmseg.apis import init_segmentor
from model_inference import inference_segmentor, process_test_pipeline, inference_on_file
from huggingface_hub import hf_hub_download
from viz_helpers import load_raster, enhance_raster_for_visualization

import matplotlib
matplotlib.use('Agg')  # Since we are not using a GUI
import matplotlib.pyplot as plt
import numpy as np


class PrithviFineTunedModel:
    """Prithvi Fine-Tuned Model"""

    def __init__(self):
        self.model = None


    def get_model(self,application_name):
        """This function takes in the application name and assigns the finetuned model for that application to the object's model.
        There are 3 applications available: Flood Mapping, Burn Scars detection and Multi-temporal-crop classification.
        These models are available on Hugging Face Hub and are downloaded using the hf_hub_download function.
        Args:
            application_name (str): The name of the application for which the model is required.
        """

        if application_name == "flood_mapping":
            repo_id = "ibm-nasa-geospatial/Prithvi-100M-sen1floods11"
            config_filename = "sen1floods11_Prithvi_100M.py"
            ckpt_filename = "sen1floods11_Prithvi_100M.pth"
        elif application_name == "burn_scars":
            repo_id = "ibm-nasa-geospatial/Prithvi-100M-burn-scar"
            config_filename = "burn_scars_Prithvi_100M.py"
            ckpt_filename = "burn_scars_Prithvi_100M.pth"
        elif application_name == "cover_crop":
            repo_id = "ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification"
            config_filename = "multi_temporal_crop_classification_Prithvi_100M.py"
            ckpt_filename = "multi_temporal_crop_classification_Prithvi_100M.pth"
        else:
            raise ValueError("Invalid application name. Please choose from flood_mapping, burn_scars or cover_crop")

        config_path = hf_hub_download(repo_id=repo_id, filename=config_filename)
        ckpt = hf_hub_download(repo_id=repo_id, filename=ckpt_filename)
        self.model = init_segmentor(Config.fromfile(config_path), ckpt, device="cpu")

    def inference(self, input_data, output_file_name, save_image = False):
        """This function takes in the input data and mask image and save the inferred TIFF image and
        if set to true, the combined image is saved as well.
        Args:
            input_data (np.ndarray): The input data
            output_file_name (str): The name of the output file
            save_metadata_image (bool): A flag which would return a image to save as metadata if set to true

        """
        if self.model is None:
            raise ValueError("Model not found. Please load the model using get_model function.")

        custom_test_pipeline = process_test_pipeline(self.model.cfg.data.test.pipeline)
        inference_on_file(self.model, input_data, output_file_name, custom_test_pipeline )
        if save_image:
            input_data_inference = enhance_raster_for_visualization(load_raster(input_data))
            output_data_inference = enhance_raster_for_visualization(load_raster(output_file_name))
            norm = matplotlib.colors.Normalize(vmin=0, vmax=2)
            # Combine the input and output images and save as metadata
            fig, ax = plt.subplots()
            ax.imshow(input_data_inference)
            ax.imshow(output_data_inference, cmap="jet", alpha=0.3, norm=norm)
            ax.axis('off')
            fig.savefig(output_file_name.replace(".tif", "_masked.png"), bbox_inches='tight',
                        pad_inches=0, transparent=True)


# Test the model
# TODO: test with other applications and other input data
if __name__ == "__main__":
    model = PrithviFineTunedModel()
    model.get_model("flood_mapping")
    model.inference("Spain_7370579_S2Hand.tif", "output.tif", save_metadata_image=True)
    print("Inference successful")