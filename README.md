# Bachelor Thesis: Design and Prototype of a Blockchain-Based Credential Revocation for IoT Device Lifecycle Management

This framework was developed as part of a bachelor thesis at the University of Zürich, ath the
Communication Systems Group (CSG), under supervision from Daria Schumm and Thomas Grübl.

## Abstract

The Internet of Things (IoT) has significantly impacted various fields, integrating deeply into daily and industrial processes. However, the heterogeneous nature of IoT devices presents substantial security challenges, making them vulnerable to attacks. Identity and Access Management (IAM) is crucial for securing IoT environments by regulating access and privileges. A key component of IAM is credential revocation, which removes permissions from compromised credentials to prevent unauthorized access and mitigate risks. While Decentralized Ledger Technology (DLT) offers a transparent and reliable solution for credential management, existing blockchain-based revocation methods struggle with scalability and performance issues. 

This thesis is dedicated to advancing the lifecycle management of IoT devices by integrating blockchain-based credential revocation. The primary goal was to create a revocation mechanism that addresses the limitations found in related work, including immediate revocation, selective revocation, real-time availability, consistency of revocation status in the network, and scalable processing of revocation requests. The system integrates Decentralized Identifiers (DIDs) and blockchain-based mechanisms for efficient credential management, utilizing Docker for containerization and Hyperledger technologies for decentralized identity and revocation.

The implementation in this thesis utilizes Docker containers for seamless deployment, the system incorporates three primary revocation workflows: Selective Batch Revocation, where credentials are revoked in batches and the Orion database is updated in bulks; Concurrent Revocation, which allows simultaneous processing of multiple nodes for vulnerabilities and revocations; and Systematic Vulnerability Revocation, which sequentially processes nodes to ensure thorough checks and updates. The implementation demonstrated that the system generally met its objectives, successfully maintaining device identifiers and ensuring consistency between the CMDB and ledger. It effectively processed revocation actions and maintained real-time availability of revocation status. However, challenges were identified, particularly concerning resource management and the constrained possibilities to adapt revocation mechanisms within the Hyperledger landscape. Future work involves addressing these limitations by exploring alternative revocation mechanisms, optimizing resource allocation, and enhancing interoperability with other blockchain technologies.

<!-- ## Challenges -->

## Setup

The full repo including submodules needs to be cloned:

`git clone --recursive https://github.com/BlackStar-cyborg/iot-revocation-component`

In order to run the demo network `docker` is needed. (add other requirements)

For local development, we offer to solutions for python environments.
Either use `conda` and setup an environment using the `acapy-env.yml` and subsequently installing missing packages
through pip with the `requirements.dev.txt` file or using Python virtual environment solely with
`requirements.dev.noconda.txt`.

To use the deployed Software Defined Network (SDN) you need to install [ZeroTier](https://www.zerotier.com/), which
requires `root` privileges.

### Maintainer

Navigate to the `./dependencies/von-network` and create a local image, over which we will be running
our Indy development network: `./manage build`

Going back to the root of the repository, to setup the infrastructures run `./manage setup`

### Physical Node

The physical nodes we deployed were Raspberry Pi 4 based, which are `ARM64`, where the Docker based
infrastructure does not run, wherefore we deploy natively.

Activate the Conda/Mamba environment to be able to run our setup, directly through `python3`: `micromamba activate aries`,
use your choice of `conda` drop in command.
At the root of the repository, to setup the infrastructures run `./manage setup node` and finally
`./run_local_node`, optionally specifying a name, which by default will be `node_raspi`.

## Repository Structure

### [Crypto](./crypto)

Holds cryptographic information for connection to the Hyperledger Orion Database. In a production
environment, this folder should ideally stay a secret for plain plain security purpose.

### [Dependencies](./dependencies)

Holds git submodules, that we depend on for running our framework.

### [Docker](./docker/)

Holds `Dockerfiles` for every type of agent we have.

### [Graphs](./graphs)

Holds some of the visualizations and the corresponding scripts used in evaluating the performance.

### [Scripts](./scripts)

Holds relevant scripts, that are either used in the `manage` or `run` scripts, or they are
completely standalone, such as the `./scripts/setup-many-nodes.sh` and `./scripts/stop-nodes.sh`.

### [Source](./src)

Holds all the python source files used to implement our framework.

### [Agent Cache](./.agent_cache) and [Logs](./logs)

Both are used to hold temporary information while running the framework.

### [Archive](./.archive)

Holds experiments with other frameworks and unused artifacts.
