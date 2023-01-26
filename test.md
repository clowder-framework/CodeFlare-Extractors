
# Welcome to CodeFlare-Clowder Extractor Examples and Tamplates
The CodeFlare-Clowder Template Extractors are a set of extractors that can be used to extract metadata from a variety of file types. The extractors are written in Python and are designed to be run in the Clowder environment. The extractors are available on GitHub at [CodeFlare-Extractors](https://github.com/clowder-framework/CodeFlare-Extractors). NOTE: Make sure this file is on Clowder folder

```shell
python CodeFlare-Extractors/test.py
```

=== "↔️  Move in and out of Clowder"
    You can import data from anywhere, and export data to anywhere. Just select a source, then a destination.

    === "Source: Clowder Dataset"
        Text in the index
        ```shell
        python ./CodeFlare-Extractors/codeflare_helpers/ds.py
        ```
        
    === "Source: HPC"
        ```shell
        echo "👉 Starting download_from_delta_to_clowder.sh"
        bash ./CodeFlare-Extractors/codeflare_helpers/download_from_delta_to_clowder.sh
        ```
    === "Source: AWS S3"
        ```shell
        echo "todo"
        ```