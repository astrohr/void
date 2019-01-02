#!/bin/bash
sudo pip3 install -r python3-requirements.txt
sed 's/#.*//' packages.txt | xargs sudo apt-get install
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt-get install postgis