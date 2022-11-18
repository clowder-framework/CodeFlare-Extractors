#!/usr/bin/env python

"""Parallel Machine Learning Extractor"""

from distutils import extension
import logging

import numpy as np
import ray
from ray.util.queue import Queue
import pyclowder.files
from pyclowder.extractors import Extractor


@ray.remote
class AsyncActor:
    def __init__(self):
        from tensorflow.keras.applications.resnet50 import ResNet50
        self.model = ResNet50(weights='imagenet')
        print("Finish Init")
    
    def process_file(self, filepaths):
        print("Process file \n")
        from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
        from tensorflow.keras.models import load_model
        from tensorflow.keras.preprocessing import image

        # pre-process image
        original = image.load_img(filepaths, target_size=(224, 224))
        numpy_image = image.img_to_array(original)
        image_batch = np.expand_dims(numpy_image, axis=0)
        processed_image = preprocess_input(image_batch, mode='caffe')

        # run predictions
        processed_image = preprocess_input(image_batch, mode='caffe')
        preds = self.model.predict(processed_image)
        pred_class = decode_predictions(preds, top=1)
        return str(pred_class)

class ImgExtractor(Extractor):
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
        """Dataset extractor. We get all filenames at once."""
        logger = logging.getLogger(__name__)
        
        # Get list of all files in dataset
        filelist = pyclowder.datasets.get_file_list(connector, host, secret_key, parameters['datasetId'])
        localfiles = []
        
        # # Loop through dataset and download all file "locally"
        for file_dict in filelist:
            extension = "." + file_dict['contentType'].split("/")[1]
            localfiles.append(pyclowder.files.download(connector, host, secret_key, file_dict['id'], ext=extension))

        # These process messages will appear in the Clowder UI under Extractions.
        connector.message_process(resource, "Loading contents of file...")

        # Print resource
        logging.warning("Printing Resources:")
        logging.warning(resource)
        logging.warning("\n")
        
        # Print localfiles
        logging.warning("Printing local files:")
        logging.warning(localfiles)
        logging.warning("\n")
        
        # Initialize actor and run machine learning module concurrently
        # TODO: Make "max_concurrency an argument?"
        # NOTE: Only "max_concurrency" tasks will be running concurrently. Once "max_concurrency" finish, the next "max_concurrency" batch should run.
        actor = AsyncActor.options(max_concurrency=5).remote()
        classifications = ray.get([actor.process_file.remote(localfiles[i]) for i in range(len(localfiles))])

        for i in range(len(classifications)):
            # Upload metadata to original file
            my_metadata = {
                    'Output': classifications[i]
            }

            # Create Clowder metadata object
            metadata = self.get_metadata(my_metadata, 'file', filelist[i]['id'], host)

            # Normal logs will appear in the extractor log, but NOT in the Clowder UI.
            logger.debug(metadata)

            # Upload metadata to original file
            pyclowder.files.upload_metadata(connector, host, secret_key, filelist[i]['id'], metadata)
        
        # Finish
        logging.warning("Successfully extracted!")

if __name__ == "__main__":
    LOCAL_PORT = 10001
    ray.init() # f"ray://127.0.0.1:{LOCAL_PORT}"
    extractor = ImgExtractor()
    extractor.start()




