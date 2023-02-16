## Select the destination location

=== "Destination: Clowder Dataset"
    Select from available datasets in Clowder, or create a new dataset to be the destination.

    ## Select the destination Clowder dataset.
    === "expand(cat .v2_available_clowder_datasets.txt | tr -d '[]')"
        ```shell
        echo "👉 Selected destination dataset: ${choice}"
        ```

=== "Destination: HPC [default: none]"
    SSH to your HPC resource and copy data from any path there to any destination. You can supply a list of files, or a path to a directory. 
    ```shell
    python ./CodeFlare-Extractors/codeflare_helpers/select_path_on_hpc.py
    echo "👉 Starting copy from Clowder 🐱 to HPC 🏢."
    ```

    # Enter the destination path on HPC. The dataset will be copied to a folder inside this path.
    === "Enter the destination path on HPC (e.g. name@hpc_cluster:/data_path/) [default: ~/]"
        details here.
        ```shell
        echo "👉 Selected destination path: ${choice}"
        # export HPC_DESTINATION_PATH=${choice}
        ```

=== "Destination: AWS S3"
    Select from available buckets in AWS S3. Transfer the entire bucket, or a list of files. Ensure '$ aws s3 ls' works on your machine.

    # Enter the destination S3 bucket name and sub-folder. The dataset will be copied to a folder inside this path.
    === "Enter the destination path on S3 (e.g. s3://my-bucket/data/destination/) [default: s3://my-bucket]"
        details here.
        ```shell
        echo "👉 Selected destination path: ${choice}"
        # export HPC_DESTINATION_PATH=${choice}
        ```
