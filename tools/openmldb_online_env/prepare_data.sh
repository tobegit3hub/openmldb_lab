#!/bin/bash

./openmldb --zk_cluster=127.0.0.1:2181 --zk_root_path=/openmldb --role=sql_client < ./prepare_data.sql
