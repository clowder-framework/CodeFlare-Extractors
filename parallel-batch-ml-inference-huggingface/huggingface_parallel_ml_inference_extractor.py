#!/usr/bin/env python
"""Parallel Machine Learning Extractor"""

import logging
from distutils import extension

import pyclowder.files
import ray
from pyclowder.extractors import Extractor
from ray.util.queue import Queue
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax


@ray.remote
class AsyncActor:

    def __init__(self):
        # Load the pre-trained model
        print("Starting to load model")
        MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.config = AutoConfig.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        print("Finish Init")

    def process_file(self, single_filepath):
        print(f"Starting to process file {single_filepath}\n")
        logging.warning(f"Starting to process file {single_filepath}")

        # sample execution (requires torchvision)
        # adapted from Huggingface Hub: https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest?text=Covid+cases+are+increasing+fast%21
        def preprocess(text):
            new_text = []
            for t in text.split(" "):
                t = '@user' if t.startswith('@') and len(t) > 1 else t
                t = 'http' if t.startswith('http') else t
                new_text.append(t)
            return " ".join(new_text)
        
 
                
        text = ""
        with open(single_filepath, 'r') as file:
            text = file.read().replace('\n', '')

        text = preprocess(text)
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        sentiments = {}
        for i in range(scores.shape[0]):
            l = self.config.id2label[ranking[i]]
            s = scores[ranking[i]]
            sentiments[l] = np.round(float(s), 4)

        logging.warning("Sentiments for this text file:",
                        sentiments)
        return sentiments


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

    def process_message(self, connector, host, secret_key, resource,
                        parameters):
        """Dataset extractor. We get all filenames at once."""
        logger = logging.getLogger(__name__)

        # Get list of all files in dataset
        filelist = pyclowder.datasets.get_file_list(connector, host,
                                                    secret_key,
                                                    parameters['datasetId'])
        localfiles = []

        # # Loop through dataset and download all file "locally"
        for file_dict in filelist:
            extension = "." + file_dict['contentType'].split("/")[1]
            localfiles.append(
                pyclowder.files.download(connector,
                                         host,
                                         secret_key,
                                         file_dict['id'],
                                         ext=extension))

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
        actor = AsyncActor.options(max_concurrency=3).remote()
        classifications = ray.get([
            actor.process_file.remote(localfiles[i])
            for i in range(len(localfiles))
        ])

        for i in range(len(classifications)):
            # Upload metadata to original file
            my_metadata = {'Output': classifications[i]}

            # Create Clowder metadata object
            metadata = self.get_metadata(my_metadata, 'file',
                                         filelist[i]['id'], host)

            # Normal logs will appear in the extractor log, but NOT in the Clowder UI.
            logger.debug(metadata)

            # Upload metadata to original file
            pyclowder.files.upload_metadata(connector, host, secret_key,
                                            filelist[i]['id'], metadata)

        # Finish
        logging.warning("Successfully extracted!")


if __name__ == "__main__":
    LOCAL_PORT = 10001
    ray.init() # f"ray://127.0.0.1:{LOCAL_PORT}"
    extractor = ImgExtractor()
    extractor.start()
