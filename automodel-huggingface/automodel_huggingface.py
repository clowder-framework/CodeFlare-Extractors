#!/usr/bin/env python
"""Example extractor based on the clowder code."""

import json
import logging
import os
import time
from typing import Dict

import pyclowder.files
from pyclowder.extractors import Extractor
from transformers import pipeline

os.environ['TRANSFORMERS_CACHE'] = '/tmp/huggingface'

def run_automodel(prompt: str , model: str, **pipeline_kwargs):
  """
  This function runs a HuggingFace model on a given prompt.

  Args:
    prompt (`str`): The input text that the model will process.
    model (`str`): The full name of a HuggingFace model to be used for the task.
    pipeline_kwargs (`dict`, *optional*): Additional keyword arguments to be passed to the HuggingFace pipeline.

  Returns:
    The output of the model after processing the prompt. In case of a CUDA Out Of Memory error, it returns an error message.

  Raises:
    RuntimeError: If there is an error other than CUDA OOM while running the model.
  """
  try:
    # Removing the task requirement for now... task=task, 
    pipe = pipeline(model=model, device='cpu', **pipeline_kwargs)
    return pipe(prompt)
  except RuntimeError as e:
    if "out of memory" in str(e):
      print(f"Cuda OOM error: {e}")
      return f"Cuda OOM error: {e}"
    else:
      raise e

class SingleFileHuggingFace(Extractor):
  def __init__(self):
    Extractor.__init__(self)
    self.setup()
    logging.getLogger('pyclowder').setLevel(logging.DEBUG)
    logging.getLogger('__main__').setLevel(logging.DEBUG)

  def process_message(self, connector, host, secret_key, resource, parameters):
    logger = logging.getLogger(__name__)
    inputfile = resource["local_paths"][0]
    file_id = resource['id']

    # Load user-defined params from the GUI.
    MODEL_NAME = ''
    KWARGS = {}
    if 'parameters' in parameters:
      params = None
      try:
        params = json.loads(parameters['parameters'])
      except TypeError as e: 
        print(f"Failed to load parameters, it's not compatible with json.loads().\nError:{e}")
        if type(parameters == Dict):
          params = parameters['parameters']

      if 'MODEL_NAME' in params:
          MODEL_NAME = params['MODEL_NAME']
          print(f"Received MODEL_NAME: {MODEL_NAME}")
      if 'KWARGS' in params:
          try:
            KWARGS = json.loads(params['KWARGS'])
            print(f"Received KWARGS: {KWARGS}")
          except TypeError as e:
            connector.message_process(resource, f"Failed to load Kwargs, your input was incompatible with json.loads(). Your input was:\n{params['KWARGS']}.\n\nError:\n{e}")
            KWARGS = params['KWARGS']
            print(f"Received KWARGS: {KWARGS}")

    # Load file
    connector.message_process(resource, "Loading contents of file...")
    text = ''
    with open(inputfile, 'r') as file:
      text = file.read()
    connector.message_process(resource, f"Received input text:\n{text}")
    
    # PREDICT
    start_time = time.monotonic()
    predictions: Dict = run_automodel(prompt=text, model=MODEL_NAME, **KWARGS)
    connector.message_process(resource, f"Predictions: {predictions}")

    # Format results with "contexts" in extractor_info.json
    preds = {
      "model_name": MODEL_NAME,
      "kwargs": KWARGS,
      "predictions": predictions,
      "⏰ runtime (seconds)": round(time.monotonic() - start_time, 2)
    }

    # UPLOAD
    host = 'http://host.docker.internal'  # !WARNING Crazy workaround for docker...
    metadata = self.get_metadata(preds, 'file', file_id, host)
    connector.message_process(resource, f"metadata to upload: {metadata}")
    pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)


if __name__ == "__main__":
  extractor = SingleFileHuggingFace()
  extractor.start()
