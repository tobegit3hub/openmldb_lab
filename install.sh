#!/bin/bash

set -xe

# Install Python libraries
pip install -r ./openmldb_server/requirements.txt

# Install frontend
cd ./vueapp
npm run build

