#!/usr/bin/env python
"""Example extractor based on the clowder code."""

import logging
import os
from distutils import extension
from typing import Dict

import numpy as np
import pyclowder.files
import ray
from pyclowder.extractors import Extractor
from ray.util.queue import Queue
from scipy.special import softmax
from transformers import (AutoConfig, AutoModelForSequenceClassification,
                          AutoTokenizer, TFAutoModelForSequenceClassification)


def preprocess(single_filepath):
  """Helper..."""
  text = ""
  with open(single_filepath, 'r') as file:
    text = file.read().replace('\n', '')
  new_text = []
  for t in text.split(" "):
    t = '@user' if t.startswith('@') and len(t) > 1 else t
    t = 'http' if t.startswith('http') else t
    new_text.append(t)
  return " ".join(new_text)


class SingleFileHuggingFace(Extractor):
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

    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
    self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
    self.config = AutoConfig.from_pretrained(MODEL)
    
    os.makedirs('/tmp/huggingface', exist_ok=True)
    self.model = AutoModelForSequenceClassification.from_pretrained(MODEL, cache_dir='/tmp/huggingface')

  def predict(self, text):
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

    logging.warning(f"Sentiments for this text file: {sentiments}")
    return sentiments

  def process_message(self, connector, host, secret_key, resource, parameters):
    logger = logging.getLogger(__name__)
    inputfile = resource["local_paths"][0]
    file_id = resource['id']

    # These process messages will appear in the Clowder UI under Extractions.
    connector.message_process(resource, "Loading contents of file...")

    # PREDICT
    text = preprocess(inputfile)
    connector.message_process(resource, f"raw text: {text}")
    predictions: Dict = self.predict(text)
    connector.message_process(resource, f"Predictions: {predictions}")

    # Format with "contexts" in extractor_info.json
    preds = {"predictions": predictions}

    # UPLOAD
    host = 'http://host.docker.internal'  # !WARNING Crazy workaround for docker...
    metadata = self.get_metadata(preds, 'file', file_id, host)
    connector.message_process(resource, f"metadata to upload: {metadata}")
    pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)


if __name__ == "__main__":
  extractor = SingleFileHuggingFace()
  extractor.start()
