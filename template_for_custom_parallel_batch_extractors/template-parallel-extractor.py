#!/usr/bin/env python

""" 
Example parallel Machine Learning Extractor. 
👉 Read the ⭐️starred⭐️ comments for usage instructions/
"""

from distutils import extension
import logging
import time
from typing import List, Dict
import pyclowder.files
from pyclowder.extractors import Extractor
import ray


@ray.remote
class AsyncActor:
    def __init__(self):
        """
        ⭐️ Here, define global values and setup your models. 
           This code runs a once per thread, if you're running this in parall, when your code first launches.
        
        For example:
        ```
        from tensorflow.keras.applications.resnet50 import ResNet50
        self.model = ResNet50(weights='imagenet')
        ```
        """
        self.model = 'load your model here' # example
    
    def process_file(self, filepaths: str):
        """
        ⭐️ Here you define the action taken for each fo your files. 
        This function will be called once for each file in your dataset, when you manually click 
        "extract this dataset"

        param filepath is a single filepath
        return {Dictionary}: Return any dictionary you'd like. It will be attached to this file as Clowder Metadata.
        """
        print("In process file \n")
        start_time = time.monotonic()

        """ 
        ⭐️ ADD YOUR PARALLEL CODE HERE 
        """
        # prediction = model.run(filepath)


        # return results (example). MUST return a Python dictionary.
        my_predicted_class = 'happy cats!'
        metadata = {
            "Predicted class": my_predicted_class,
            "Extractor runtime": f"{start_time - time.monotonic():.2f} seconds",
        }

        assert type(metadata) == Dict  # must return a dictionary.
        return metadata

class ChangeMyName_Parallel_Extractor(Extractor):
    """ This extractor..... runs machine learning inference in parallel (for example). """
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
        """ Dataset extractor. We get all filenames at once, and start parallel extractors. """
        logger = logging.getLogger(__name__)
        
        # ⬇️ Download files: a list of all files in dataset
        filelist = pyclowder.datasets.get_file_list(connector, host, secret_key, parameters['datasetId'])
        localfiles = []
        
        # Loop through dataset and download all file "locally"
        for file_dict in filelist:
            extension = "." + file_dict['contentType'].split("/")[1]
            localfiles.append(pyclowder.files.download(connector, host, secret_key, file_dict['id'], ext=extension))
        connector.message_process(resource, "Loading contents of file...")
        
        # Initialize actor and run machine learning module concurrently
        # TODO: Make "max_concurrency an argument?"
        # NOTE: Only "max_concurrency" tasks will be running concurrently. Once "max_concurrency" finish, the next "max_concurrency" batch should run.
        actor = AsyncActor.options(max_concurrency=5).remote()
        extractor_produced_metadata = ray.get([actor.process_file.remote(localfiles[i]) for i in range(len(localfiles))])

        # ⬆️ Upload & attach metadata to original input file
        for metadat_dictionary in extractor_produced_metadata:
            # Create Clowder metadata object
            metadata = self.get_metadata(metadat_dictionary, 'file', filelist[i]['id'], host)
            # Normal logs will appear in the extractor log, but NOT in the Clowder UI.
            logger.debug(metadata)
            # Upload metadata to original file
            pyclowder.files.upload_metadata(connector, host, secret_key, filelist[i]['id'], metadata)
        
        # Done!
        logging.warning("Successfully finished all extractions!")

if __name__ == "__main__":
    # LOCAL_PORT = 10001
    # f"ray://127.0.0.1:{LOCAL_PORT}"
    ray.init() 
    extractor = ChangeMyName_Parallel_Extractor() # ⭐️ Change my name!
    extractor.start()

