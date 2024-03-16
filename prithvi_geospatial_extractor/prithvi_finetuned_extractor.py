#!/usr/bin/env python
"""Prithvi fine-tuned extractor based on the example extractor clowder code."""

import logging
import json
import subprocess
from typing import Dict

from pyclowder.utils import CheckMessage
from pyclowder.extractors import Extractor
import pyclowder.files

from prithvi_finetuned_model import PrithviFineTunedModel

class PrithviFineTunedExtractor(Extractor):
    """Prithvi Fine-Tuned Extractor"""

    def __init__(self):
        Extractor.__init__(self)
        # parse command line and load default logging configuration
        self.setup()

        # setup logging for the extractor
        logging.getLogger('pyclowder').setLevel(logging.DEBUG)
        logging.getLogger('__main__').setLevel(logging.DEBUG)


    def process_message(self, connector, host, secret_key, resource, parameters):

        input_file = resource["local_paths"][0]
        file_id = resource['id']
        dataset_id = resource['parent']['id']

        # Load user-defined params from the GUI.
        APPLICATION_TYPE = ''
        SAVE_IMAGE = False
        if 'parameters' in parameters:
            params = None
            try:
                params = json.loads(parameters['parameters'])
            except TypeError as e:
                print(f"Failed to load parameters, it's not compatible with json.loads().\nError:{e}")
                if type(parameters == Dict):
                    params = parameters['parameters']

            if 'APPLICATION_TYPE' in params:
                APPLICATION_TYPE = params['APPLICATION_TYPE']
                print(f"Received APPLICATION_TYPE: {APPLICATION_TYPE}")

            if 'SAVE_IMAGE' in params:
                SAVE_IMAGE = params['SAVE_IMAGE']
                print(f"Received SAVE_IMAGE: {SAVE_IMAGE}")

        # Load tif file
        connector.message_process(resource, "Loading contents of file...")

        # PREDICT
        model = PrithviFineTunedModel()
        model.get_model(APPLICATION_TYPE)
        output_file = input_file.replace(".tif", "_pred.tif")
        model.inference(input_file, output_file, save_image=SAVE_IMAGE)
        print("Inference successful")

        # Upload predicted tiff file to Clowder dataset as a new file
        # if save_image is true upload the combined image as well
        # TODO: Use application_name to name the output file
        connector.message_process(resource, "Uploading predicted tiff file...")
        pyclowder.files.upload_to_dataset(connector, host, secret_key, dataset_id, output_file)
        if SAVE_IMAGE:
            combined_image = output_file.replace(".tif", "_masked.png")
            pyclowder.files.upload_to_dataset(connector, host, secret_key, dataset_id, combined_image)


if __name__ == "__main__":
    extractor = PrithviFineTunedExtractor()
    extractor.start()