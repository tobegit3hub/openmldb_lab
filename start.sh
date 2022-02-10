#!/bin/bash

set -xe

cd ./openmldb_server/

FLASK_ENV=production FLASK_APP=server flask run

#python3 -m webbrowser http://127.0.0.1:5000
