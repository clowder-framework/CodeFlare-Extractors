from typing import List

from pyclowder.client import ClowderClient
from termcolor import colored


def main():
    # Initialize the client
    creds = load_credentials()
    client = ClowderClient(host=creds['hostname'], key=creds['api_key'])

    # client.list_datasets()
    datasets = client.get('/datasets/')
    ds_list = [d['name'] for d in datasets]
    save_to_file(ds_list, '.available_clowder_datasets.txt')


def load_credentials():
    with open("/Users/kastanday/.clowder/credentials") as file:
        hostname_and_api_key = file.read().splitlines()

    hostname = hostname_and_api_key[1]
    api_key = hostname_and_api_key[2]
    print(hostname)
    print(api_key)

    return {'hostname': hostname, 'api_key': api_key}


def save_to_file(sentences: List, filename: str):
    # Open the file in write mode
    with open(filename, "w") as file:
        for sentence in sentences:
            file.write(sentence)


if __name__ == "__main__":
    main()