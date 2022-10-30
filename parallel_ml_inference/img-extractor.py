#!/usr/bin/env python

"""Parallel Machine Learning Extractor"""

# from asyncio import futures
import logging
# import time
# import asyncio

import requests

from importlib_metadata import files

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
    
    # def run_concurrent(self, file):
    #     data = [] 
    #     while not self.queue.empty():
    #         future = self.process_file(self.queue.pop())
    #         data.append(ray.get(future))
    #     return data
    
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
        # Process the file and upload the results
        
        # all files = resource["local_paths"]
        items = resource["local_paths"]
        
        
        # Now add all your files to the processing queue, 
        # in whatever format you want the model to read them
        q = Queue()
        for item in items: 
            q.put(item)
        
        for item in items: 
            assert item == q.get()
            
        # Create Queue with the underlying actor reserving 1 CPU.
        

        logger = logging.getLogger(__name__)
        inputfile = resource["local_paths"][0]
        file_id = resource['id']

        # These process messages will appear in the Clowder UI under Extractions.
        connector.message_process(resource, "Loading contents of file...")

        # Print resource
        logging.warning("Printing Resources:\n")
        logging.warning(resource)
        logging.warning(resource["local_paths"])
        
        classification = ray.get(process_file.remote(str(inputfile)))
        ray.get([actor.run_concurrent.remote() for _ in range(4)])
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
        logging.warning("Done extracting!")

if __name__ == "__main__":
    print("Hello")
    LOCAL_PORT = 10001
    ray.init() # f"ray://127.0.0.1:{LOCAL_PORT}"
    # extractor = ImgExtractor()
    # extractor.start()
    
    # get files
    files = []
    for _ in range(10):
        files.append("/home/phantuanminh/CodeFlare-Extractors/parallel_ml_inference/pics/saiki.jpg")
        
    print(files)
    
    # init actor and run
    print("Initing Actor")
    actor = AsyncActor.options(max_concurrency=5).remote()

    # only 10 tasks will be running concurrently. Once 10 finish, the next 10 should run.
    metadata = ray.get([actor.process_file.remote(files[i]) for i in range(len(files))])
    print(metadata)

