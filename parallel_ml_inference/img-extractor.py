#!/usr/bin/env python

"""Example extractor based on the clowder code."""

import logging
import ray
import numpy as np
import matplotlib.pyplot as plt

from pyclowder.extractors import Extractor
import pyclowder.files


@ray.remote
def process_file(filepaths):
    from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.applications.resnet50 import ResNet50

    model = ResNet50(weights='imagenet')

    # pre-process image
    original = image.load_img(filepaths, target_size=(224, 224))
    numpy_image = image.img_to_array(original)
    image_batch = np.expand_dims(numpy_image, axis=0)
    processed_image = preprocess_input(image_batch, mode='caffe')

    # run predictions
    processed_image = preprocess_input(image_batch, mode='caffe')
    preds = model.predict(processed_image)
    pred_class = decode_predictions(preds, top=1)
    return str(pred_class)

class WavExtractor(Extractor):
    """Count the number of characters, words and lines in a text file."""
    def __init__(self):
        Extractor.__init__(self)

        # add any additional arguments to parser
        # self.parser.add_argument('--max', '-m', type=int, nargs='?', default=-1,
        #                          help='maximum number (default=-1)')

        # parse command line and load default logging configuration
        self.setup()

        # setup logging for the exctractor
        logging.getLogger('pyclowder').setLevel(logging.DEBUG)
        logging.getLogger('__main__').setLevel(logging.DEBUG)

    def process_message(self, connector, host, secret_key, resource, parameters):
        # Process the file and upload the results

        logger = logging.getLogger(__name__)
        inputfile = resource["local_paths"][0]
        file_id = resource['id']

        # These process messages will appear in the Clowder UI under Extractions.
        connector.message_process(resource, "Loading contents of file...")

        # Print resource
        logging.warning(resource)
        logging.warning("SEPERATE\n")
        logging.warning(resource["local_paths"])
        logging.warning(resource["local_paths"][0])
        classification = ray.get(process_file.remote(str(inputfile)))
        # classification = self.process_file.remote(resource["local_paths"][0])

        # Upload metadata to original file
        result = {
                'Classification': classification
        }

        # post metadata to Clowder
        metadata = self.get_metadata(result, 'file', file_id, host)

        # Normal logs will appear in the extractor log, but NOT in the Clowder UI.
        logger.debug(metadata)

        # Upload metadata to original file
        pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)
        logging.warning("DONE Process!")

if __name__ == "__main__":
    LOCAL_PORT = 10001
    ray.init() # f"ray://127.0.0.1:{LOCAL_PORT}"
    extractor = WavExtractor()
    extractor.start()
