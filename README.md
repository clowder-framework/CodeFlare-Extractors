# CodeFlare-Extractors
Performance-oriented, parallel, [Clowder Extractors](https://github.com/clowder-framework/pyclowder) using [CodeFlare](https://research.ibm.com/blog/codeflare-ml-experiments) &amp; [Ray.io](https://www.ray.io/).

These are well suited for running ML Inference inside Clowder via a GUI. 

## Install
1. Clone this repo inside your [Clowder](https://github.com/clowder-framework/clowder) directory, for example:
```text
── Clowder
└─── CodeFlare-Extractors
```
2. Install [CodeFlare-CLI](https://github.com/project-codeflare/codeflare-cli) 

```bash
brew tap project-codeflare/codeflare-cli https://github.com/project-codeflare/codeflare-cli
brew install codeflare
```
If you're on Windows or Linux, please install from source, as described in the [CodeFlare-CLI repo](https://github.com/project-codeflare/codeflare-cli).


## Usage

Invoke from **inside your Clowder directory,** so that we may respect Clowder's existing Docker Compose files. 

```
cd ../ && codeflare CodeFlare-Extractors
```

Follow the CLI to run one of our demos, or modify our demos to fit your needs!


## Documentation

* [Extractor overview](https://clowder-framework.readthedocs.io/en/latest/develop/extractors.html)

* [Extractor Details](https://opensource.ncsa.illinois.edu/confluence/display/CATS/Extractors#Extractors-Extractorbasics)

* [PyClowder Extractors Source](https://github.com/clowder-framework/pyclowder)
