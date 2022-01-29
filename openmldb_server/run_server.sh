#!/bin/bash

set -xe

FLASK_ENV=development FLASK_APP=server flask run
