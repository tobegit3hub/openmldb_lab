#!/bin/bash

set -xe

cd ./openmldb_server/

FLASK_ENV=production FLASK_APP=server flask run -p 7788
# ./openmldb_server/server.py
