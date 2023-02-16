import os
from typing import List

from pyclowder.client import ClowderClient
from termcolor import colored


def main():
    # Initialize the client
    client = ClowderClient(host="http://localhost:8000", key="bbe2dce9-c3eb-4188-8a70-1d6e676beeb1")

    # client.list_datasets()
    # datasets = client.get('/datasets/')
    # ds_list = [d['name'] for d in datasets]
    # print(ds_list)
    # save_to_file(ds_list, 'clowder_db')
    # for i, dataset in enumerate(datasets):
    #     print('\t', f'{i}.', dataset['name'])

    # or enter a new dataset name, and create a new dataset

    # works, but should use CodeFlare instead.
    # n = input(
    #     colored(
    #         f"👉 Enter the destination filepath on the HPC resource. Your Clowder dataset will be transferred here, and arrive as a folder.",
    #         "yellow",
    #         attrs=["bold"]))
    # print("You entered", n)
    # os.environ['HPC_DESTINATION_PATH'] = n
    return


def save_to_file(sentences: List, filename: str):
    # Open the file in write mode
    with open(filename, "w") as file:
        for sentence in sentences:
            file.write(sentence)
            # ASCII
            #.encode(encoding='ascii', errors='ignore').decode()


if __name__ == "__main__":
    main()