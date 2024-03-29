#!/usr/bin/env python
"""Example extractor that runs custom inference using HuggingFace Transformers or any ML frameowrk in Python.

Usage in Clowder GUI:
# SETUP_CODE
from transformers import pipeline\npipe = pipeline(model='gpt2')

# PREDICT_CODE
output = pipe(input, max_new_tokens=20, do_sample=True)

# PIP_REQUIREMENTS
arxiv\npython-dotenv
"""

import json
import logging
import os
import io
import time
from typing import Any, Dict
import contextlib

import pyclowder.files
from pyclowder.extractors import Extractor
from transformers import pipeline

os.environ['TRANSFORMERS_CACHE'] = '/tmp/huggingface'

def run_model(setup_code: str, predict_code: str, input: str):
  """
  This function executes arbitrary Python code for machine learning inference.

  Args:
    setup_code (str): The Python code to set up the machine learning model or environment.
    predict_code (str): The Python code to run the inference using the model.
    input (str): The input data on which the inference will be performed.

  Returns:
    The result of the inference after executing the predict_code. In case of an error, it returns an error message.

  Raises:
    Exception: If there is an error during the execution of the setup or prediction code.
  """
  print()
  print("👇"*10)
  print("Setup Code Block:")
  print(setup_code)
  print("-----------------")
  print()

  print("Predict Code Block:")
  print(predict_code)
  print("-------------------")
  print()
  
  print("Input:")
  print(input)
  print("-------------------")
  print("👆"*10)

  # Setup 
  setup_globals = {}
  setup_locals = {}
  stderr = io.StringIO()
  try:
    with contextlib.redirect_stderr(stderr):
      exec(setup_code, setup_globals, setup_locals)
  except Exception as e:
    print(f"Error in setup: {e}")

  pipe = setup_locals.get('pipe')

  # Print globals and locals
  print("Globals:", setup_globals)
  print("Locals:", setup_locals)
  print("STDERR:", stderr.getvalue())

  # Predict
  predict_globals = {}
  predict_locals = {'pipe': pipe, 'input': input}
  stderr = io.StringIO()

  try:
    with contextlib.redirect_stderr(stderr):
      exec(predict_code, predict_globals, predict_locals)
  except Exception as e:
    print(f"Error in predict: {e}")

  print(f"RESULT: {predict_locals.get('output')}")
  print("STDERR:", stderr.getvalue())

  return predict_locals.get('output')


def install_dependencies(requirements: str):
  """
  Install dependencies from a string of requirements.

  Args:
      requirements (str): A string that contains the package requirements, 
                          similar to a requirements.txt file.
  """
  import subprocess
  # Split the requirements string into a list of packages
  packages = requirements.splitlines()

  # Install each package using pip
  for package in packages:
    subprocess.run(['pip', 'install', package], check=True)

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
    user_setup_code = ''
    user_predict_code = ''
    pip_requirements = None
    if 'parameters' in parameters:
      params = None
      try:
        params = json.loads(parameters['parameters'])
      except TypeError as e: 
        print(f"Error:{e}\nWarning Failed to load parameters with json.loads(), attempting loading as Python Dict.")
        if type(parameters == Dict):
          params = parameters['parameters']
      
      user_setup_code = params['SETUP_CODE'].replace('\\n', '\n')
      user_predict_code = params['PREDICT_CODE'].replace('\\n', '\n')
      if 'PIP_REQUIREMENTS' in params:
        pip_requirements = params['PIP_REQUIREMENTS'].replace('\\n', '\n') # Decode the escaped newlines
      print(f"Received SETUP_CODE: {user_setup_code}")
      print(f"Received PREDICT_CODE: {user_predict_code}")
      print(f"Received PIP_REQUIREMENTS: {pip_requirements}")

    else:
      connector.message_process(resource, "ERROR: No input parameters found for `SETUP_CODE` and `PREDICT_CODE`, which are both required for this extractor to do custom ML inference.")

    # Load file
    connector.message_process(resource, "Loading contents of file...")
    text = ''
    with open(inputfile, 'r') as file:
      text = file.read()
    connector.message_process(resource, f"Received input text:\n{text}")

    # Install custom requirements
    if pip_requirements:
      connector.message_process(resource, f"Installing custom requirements: {pip_requirements}")
      install_dependencies(pip_requirements)
    
    # PREDICT
    start_time = time.monotonic()
    predictions: Any = run_model(setup_code=user_setup_code, predict_code=user_predict_code, input=text)
    connector.message_process(resource, f"Predictions: {predictions}")

    # Format results with "contexts" in extractor_info.json
    preds = {
      "setup_code": user_setup_code,
      "predict_code": user_predict_code,
      "requirements": pip_requirements,
      "predictions": predictions,
      "⏰ runtime (seconds)": round(time.monotonic() - start_time, 2)
    }

    # UPLOAD
    host = 'http://host.docker.internal' if os.path.exists('/.dockerenv') else 'http://localhost' # !WARNING workaround for local Docker networking...
    metadata = self.get_metadata(preds, 'file', file_id, host)
    connector.message_process(resource, f"metadata to upload: {metadata}")
    pyclowder.files.upload_metadata(connector, host, secret_key, file_id, metadata)


if __name__ == "__main__":
  extractor = SingleFileHuggingFace()
  extractor.start()
