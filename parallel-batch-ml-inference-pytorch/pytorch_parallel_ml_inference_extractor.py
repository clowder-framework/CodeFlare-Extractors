#!/usr/bin/env python
"""Parallel Machine Learning Extractor"""

import logging
from distutils import extension

import pyclowder.files
import ray
import torch
import torchvision
from pyclowder.extractors import Extractor
from ray.util.queue import Queue


@ray.remote
class AsyncActor:

    def __init__(self):
        # Load the pre-trained model
        print("Starting to load model")
        self.model = torchvision.models.resnet18(pretrained=True)
        print("After model loaded")
        # Put the model in eval mode
        self.model.eval()
        print("Finish Init")

    def process_file(self, single_filepath):
        print(f"Starting to process file {single_filepath}\n")
        logging.warning(f"Starting to process file {single_filepath}")

        # sample execution (requires torchvision)
        # adapted from Pytorch Hub: https://pytorch.org/hub/pytorch_vision_resnet/
        from PIL import Image
        from torchvision import transforms
        input_image = Image.open(single_filepath)
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(
            0)  # create a mini-batch as expected by the model

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            self.model.to('cuda')

        with torch.no_grad():
            output = self.model(input_batch)
        # Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
        # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        probabilities = torch.nn.functional.softmax(output[0], dim=0)

        # Read the categories
        # classes from here: wget https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt
        with open("imagenet_classes.txt", "r") as f:
            categories = [s.strip() for s in f.readlines()]
        # Return top categories per image
        top5_prob, top5_catid = torch.topk(probabilities, 5)
        top_5_probs = {}
        for i in range(top5_prob.size(0)):
            top_5_probs[categories[top5_catid[i]]] = float(top5_prob[i].item())
            # print(f"{categories[top5_catid[i]]}, {(float(top5_prob[i].item())):2f}")

        logging.warning("Most likely categories for this image are:",
                        top_5_probs)
        return top_5_probs


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
    print("Main() called")
    ray.shutdown()
    print("before ray.init")
    # f"ray://127.0.0.1:{LOCAL_PORT}"
    ray.init(f"ray://127.0.0.1:{LOCAL_PORT}")
    assert ray.is_initialized()
    print("Ray initialized")
    extractor = ImgExtractor()
    print("After extractor inited")
    extractor.start()
    print("After extractor.start()")
