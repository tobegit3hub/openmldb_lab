#!/bin/bash

set -xe

# Install Python libraries
pip install -r ./requirements.txt

# Install frontend
cd ./vueapp
npm run build
cd ../

# Install backend
python ./setup.py install
