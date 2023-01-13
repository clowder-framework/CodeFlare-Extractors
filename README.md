<div align="center">
<p align="center">

<!-- prettier-ignore -->
<h1><img src="https://avatars.githubusercontent.com/u/51137373?s=200&v=4" height="45px"> Clowder Framework Data Processors</h1>

**The open-source tool for Long Tail Data Management**

<!-- prettier-ignore -->
<a href="https://clowderframework.org/">Website</a> •
<a href="https://clowder-framework.readthedocs.io/en/latest/userguide/installing_clowder.html">Install</a> •
<a href="https://clowder-framework.readthedocs.io/en/latest/">Docs</a> •
<a href="https://github.com/clowder-framework/CodeFlare-Extractors/tree/main/template_for_custom_parallel_batch_extractors">Make your own from a Template</a> •
<a href="https://clowder.ncsa.illinois.edu/clowder/">Try it now</a>

Join our Slack to talk to the devs 

[![Join our Slack for support](https://img.shields.io/badge/Slack-4A154B?logo=slack&logoColor=white)](https://clowder-software.slack.com/join/shared_invite/enQtMzQzOTg0Nzk3OTUzLTYwZDlkZDI0NGI4YmI0ZjE5MTZiYmZhZTIyNWE1YzM0NWMwMzIxODNhZTA1Y2E3MTQzOTg1YThiNzkwOWQwYWE#/shared-invite/email)

[![CodeFlare Clowder](./utils/media/CodeFlare_CLI_Demo.png)](https://clowder-framework.readthedocs.io/en/latest/userguide/installing_clowder.html)

CodeFlare + Clowder makes it easy to run ML inference and similar workloads over your files, no matter how unique your data is.

</p>
</div>

---

# CodeFlare-Extractors
Performance-oriented, parallel, [Clowder Extractors](https://github.com/clowder-framework/pyclowder) using [CodeFlare](https://research.ibm.com/blog/codeflare-ml-experiments) &amp; [Ray.io](https://www.ray.io/).

These are well suited for running ML Inference inside Clowder the extractors GUI. 

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

Running the CodeFlare-CLI adds the extractor to Clowder’s Docker compose file, then you to use it, you most likely have to actually go into Clowder web app and click “Submit for extraction” in any particular Dataset.
![CleanShot 2022-11-17 at 20 45 55](https://user-images.githubusercontent.com/13607221/202605295-b76e2e8f-a398-4997-8f50-091a5279ba87.png)

## Use our templates to build a high performance Clowder Extractor

Need to process a lot of files? These demos are a great starting point to write your own parallel file extractor. 

This is great for:
* ML Inference
* Data pre-processing

Try out our demo by running `$ cd ../ && codeflare CodeFlare-Extractors`.

You can edit it to fit your needs, or write your own Extractor starting with our heavily documented template here: `./template_for_custom_parallel_batch_extractors`.

## Documentation

* [Extractor overview](https://clowder-framework.readthedocs.io/en/latest/develop/extractors.html)

* [Extractor Details](https://opensource.ncsa.illinois.edu/confluence/display/CATS/Extractors#Extractors-Extractorbasics)

* [PyClowder Extractors Source](https://github.com/clowder-framework/pyclowder)
