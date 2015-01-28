#!/bin/sh
echo "apt-get started..."
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y build-essential
sudo apt-get install -y python-dev
sudo apt-get install -y libxml2-dev
sudo apt-get install -y libxml2
sudo apt-get install -y libxslt-dev
sudo apt-get install -y libffi-dev
sudo apt-get install -y python-pip
sudo apt-get install libssl-dev
echo "apt-get ended..."
echo "pip install started..."
sudo pip install -r required.txt