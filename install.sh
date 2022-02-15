#!/bin/bash

set -xe

# Install frontend
npm install -g @vue/cli
cd ./vueapp
npm install
npm run build
cd ../

# Install backend
pip install -r ./requirements.txt
python ./setup.py install
