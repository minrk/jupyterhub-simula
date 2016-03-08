#!/bin/bash
# install jupyterhub, dependencies
# run me with sudo
set -e

apt-get update && apt-get -y dist-upgrade
apt-get -y install \
  git build-essential \
  supervisor \
  npm nodejs-legacy \
  python3-dev python3-pip

pip3 install -r requirements.txt

npm install -g configurable-http-proxy

