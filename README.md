<p align="center">
    <img width=200px height=200px src="/docs/nomenclate_logo.png" alt="nomenclate logo">
</p>

<h2 align="center">Nomenclate API</h2>

<div align="center">
    <a href="https://github.com/AndresMWeber/nomenclate-api-python">
        <img alt="Status" src="https://img.shields.io/badge/status-active-success.svg" />
    </a>
    <a href="https://github.com/AndresMWeber/nomenclate-api-python/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/andresmweber/nomenclate-api-python.svg" />
    </a>
    <a href="https://github.com/AndresMWeber/nomenclate-api-python/actions/workflows/python-app.yml">
        <img alt="Issues" src="https://github.com/AndresMWeber/nomenclate-api-python/actions/workflows/python-app.yml/badge.svg" />
    </a>
    <br />
    <a href="https://github.com/AndresMWeber/nomenclate-api-python/blob/master/LICENSE">
        <img alt="License" src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" />
    </a>
    <a href=".">
        <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/andresmweber/nomenclate-api-python" />
    </a>
</div>

<br />

<p align="center">
An API using the Nomenclate package to automate and generate strings based on arbitrary user-defined naming conventions.
</p>

<br />

<h3 align="center">
    <code>
    <a href="https://nom-api.andresmweber.com/"><img width=14px alt="Github Favicon" src="https://aws.amazon.com/favicon.ico" /> Live Demo</a>
    ·
    <a href="#installation">Installation</a>
    </code>
</h3>

## 📝 Table of Contents

- [Installation](#installation)
- [Deployment](#deployment)
- [Built Using](#tech)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

# Installation

### Prerequsites

1. [Python](https://www.python.org/) and [Python Poetry](https://python-poetry.org/) is installed
2. [NodeJS](https://www.nodejs.org/) is installed
3. You have a [Serverless](https://www.serverless.com/) account
4. You have an [AWS](https://aws.amazon.com/) account
5. You have started a [MongoDB Atlas](https://www.mongodb.com/) cluster.

### Install steps
1. `npm install`  
2. `poetry install` (To install in the top level directory always: `poetry config virtualenvs.in-project true`)
3. You should now have access to the serverless CLI (if you haven't, you need to login using `sls login`)
4. Now feel free to [invoke the lambdas](https://www.serverless.com/framework/docs/providers/aws/cli-reference/invoke-local/) using `sls invoke local --function <function name>`

## 🚀 Deployment <a name = "deployment"></a>

### Modifications to `serverless.yml`
1. The default is an `AWS profile` named '**aw**'.  If you have a different profile in your [credentials file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) you need to change the name in the provider.profile section.
2. If you do not require/have a [custom domain name or certificate](https://www.serverless.com/blog/serverless-api-gateway-domain), remove the `customDomain` section.

### Deploying to AWS

This project is deployed on AWS using Serverless to automate the deployment.

Once the modifications are put in to `serverless.yml` you can use the [Serverless CLI](https://www.serverless.com/framework/docs/providers/aws/cli-reference/) to deploy.

There are also ease of use Poetry commands in place:
- `poetry run poe deploy-domain` - To deploy the custom domain (necessary before deploying if you set it up in the modifications)
- `poetry run poe deploy` - To deploy the stack to AWS


## ⛏️ Tech Stack <a name = "tech"></a>

- [NodeJS](https://www.nodejs.org/) - Web Server
- [Python](https://www.python.org/) - Front End
- [AWS](https://aws.amazon.com/) - Hosting
- [Serverless](https://www.serverless.com/) - CD
- [MongoDB](https://www.mongodb.com/) - Database

## ✍️ Authors <a name = "authors"></a>

<a href="https://github.com/andresmweber/">
    <img title="Andres Weber" src="https://github.com/andresmweber.png" height="50px">
</a>
