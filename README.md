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

## Why Extractors?

At its heart, **extractors run a Python function over every file in a dataset**. They can run at the click of a button in Clowder web UI or like an event listener every time a new file is uploaded.

Extractors are performant, parallel-by-default, web-native [Clowder Extractors](https://github.com/clowder-framework/pyclowder) using [CodeFlare](https://research.ibm.com/blog/codeflare-ml-experiments) &amp; [Ray.io](https://www.ray.io/).

### ML Inference

Need to process a lot of files? **This is great for ML inference and data pre-processing**. Check out our ML inference examples, or just swap out the model to your own!

<img src="https://pytorch.org/assets/images/pytorch-logo.png" width="40" align="left">

[PyTorch example](https://github.com/clowder-framework/CodeFlare-Extractors/tree/main/parallel-batch-ml-inference-pytorch)

<img src="https://upload.wikimedia.org/wikipedia/commons/2/2d/Tensorflow_logo.svg" width="35" align="left">

[TensorFlow Keras example](https://github.com/clowder-framework/CodeFlare-Extractors/tree/main/parallel_batch_ml_inference)

### Event-driven

Have daily data dumps? **Extractors are perfect for event-driven actions**. They will run code every time a file is uploaded. Uploads themselves can be automated via [PyClowder](https://github.com/clowder-framework/pyclowder) for a totally hands-free data pipeline.

### Clowder's rich scientific data ecosystem

Benefit from the rich featureset & full extensibility of Clowder:
* Instead of files on your laptop, use Clowder to add collaborators & share datasets via the browser.
* Scientists like that we work with every filetype, and have rich extensibility for any job you need to run.


## 🚀 Quickstart install
1. Clone this repo inside your [Clowder](https://github.com/clowder-framework/clowder) directory (or [install Clowder](https://clowder-framework.readthedocs.io/en/latest/userguide/installing_clowder.html) if you haven't yet):
<img src="https://avatars.githubusercontent.com/u/51137373?s=200&v=4" width="100" align="left">

```bash
cd your/path/to/clowder
git clone git@github.com:clowder-framework/CodeFlare-Extractors.git
```

2. Install [CodeFlare-CLI](https://github.com/project-codeflare/codeflare-cli) 
<img src="./utils/media/codeflare_cli.svg" width="100" height="100" align="left">


```bash
brew tap project-codeflare/codeflare-cli https://github.com/project-codeflare/codeflare-cli
brew install codeflare
```
On Linux, please install from source, as described in the [CodeFlare-CLI repo](https://github.com/project-codeflare/codeflare-cli). Windows has not been tested.


## Usage

Invoke from **inside your Clowder directory,** so that we may respect Clowder's existing Docker Compose files. 

1. Launch the codeflare CLI to try our default extractors. This will launch Clowder.

```bash
cd your/path/to/clowder 
codeflare ./CodeFlare-Extractors
```

2. Now, upload an image to a [Clowder Dataset](https://clowder-framework.readthedocs.io/en/latest/userguide/ug_datasets.html) so we can try to classify it (into one of 1000 imagenet classes).

3. Finally, run the extractor! In the web app, click “Submit for extraction” (shown below).

![CleanShot 2022-11-17 at 20 45 55](https://user-images.githubusercontent.com/13607221/202605295-b76e2e8f-a398-4997-8f50-091a5279ba87.png)


## 🛠 Make your own
You can edit it to fit your needs, or write your own Extractor starting with our heavily documented template here: `./template_for_custom_parallel_batch_extractors`.

#### Worked example
Todo: Show the Python funciton in-line here, so we can walk thru exactly what to modify.

#### Using the CodeFlare CLI
Running the CodeFlare-CLI adds the extractor to Clowder’s `docker-compose-extractors.yaml` file. Then Clowder is started as normal, e.g. `docker-compose -f docker-compose.yml -f docker-compose.extractors.yml up -d`.

## Documentation

* [Extractor overview](https://clowder-framework.readthedocs.io/en/latest/develop/extractors.html)

* [Extractor Details](https://opensource.ncsa.illinois.edu/confluence/display/CATS/Extractors#Extractors-Extractorbasics)

* [PyClowder Extractors Source](https://github.com/clowder-framework/pyclowder)
