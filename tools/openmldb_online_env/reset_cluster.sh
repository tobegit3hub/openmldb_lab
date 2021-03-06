#!/bin/bash

set -xe

./stop-all.sh

rm -rf ../db/ ../db2/ ../logs/ ../logs2/ ../recycle/ ../taskmanager/bin/logs/

/root/zookeeper-3.4.14/bin/zkCli.sh -server 0.0.0.0:2181 <<EOF
rmr /openmldb
EOF

sleep 1

./start-all.sh

sleep 5

./openmldb --zk_cluster=127.0.0.1:2181 --zk_root_path=/openmldb --role=sql_client < prepare_data.sql
