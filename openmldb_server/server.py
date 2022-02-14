#!/usr/bin/env python3

import os
import sys
import logging
import argparse
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import openmldb.dbapi

logger = logging.getLogger("openmldb_server")

app = Flask(__name__,
            template_folder="./dist/",
            static_folder="./dist",
            static_url_path="")
cors = CORS(app, resources=r'/*')

app.config['CORS_HEADERS'] = 'Content-Type'



# Define parameters
parser = argparse.ArgumentParser()
parser.add_argument(
    "--host",
    default=os.environ.get("HOST", "0.0.0.0"),
    help="The host of the server(eg. 0.0.0.0)")
parser.add_argument(
    "--port",
    default=int(os.environ.get("PORT", "7788")),
    help="The port of the server(eg. 7788)",
    type=int)
parser.add_argument(
    "--zk",
    default=os.environ.get("ZK", "0.0.0.0:2181"),
    help="The ZooKeeper cluster(eg. 0.0.0.0:2181)")
parser.add_argument(
    "--zk_path",
    default=os.environ.get("ZK_PATH", "/openmldb"),
    help="The ZK path of OpenMLDB cluster(eg. /openmldb)")
parser.add_argument(
    "--default_db",
    default=os.environ.get("DB", "default_db"),
    help="The default database(eg. default_db)")
parser.add_argument(
    "--debug",
    default=os.environ.get("DEBUG", ""),
    help="Enable debug for flask or not(eg. true)",
    type=bool)

args = parser.parse_args(sys.argv[1:])
for arg in vars(args):
    logger.info("{}: {}".format(arg, getattr(args, arg)))

global db
global cursor

try:
    db = openmldb.dbapi.connect(args.default_db, args.zk, args.zk_path)
    cursor = db.cursor()
except Exception as e:
    logging.warn("Fail to connect OpenMLDB server, exception: " + str(e))

@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")

@app.route('/api/dbs', methods=['GET'])
@cross_origin()
def get_dbs():
    dbNames = cursor.get_databases()
    dbNameMapList = []
    if isinstance(dbNames, list):
        for dbName in dbNames:
            dbNameMapList.append({"name": dbName})
        result = {"success": True, "databases": dbNameMapList}
    else:
        result = {"success": False, "databases": []}
    return jsonify(result)

@app.route('/api/tables', methods=['GET'])
@cross_origin()
def get_tables():
    dbName = request.args["db"]
    tableNames = cursor.get_tables(dbName)
    tableNameMap = []
    for tableName in tableNames:
        tableNameMap.append({"name": tableName})
    result = {"tables": tableNameMap}
    return jsonify(result)

@app.route('/api/executesql', methods=['POST'])
@cross_origin()
def execute_sql():
    if request.method != 'POST':
        response = {"success": False, "error": "Unsupport method: {}".format(request.method)}
        return jsonify(response)

    # Get SQL from POST json instead of GET to avoid url encoding
    sql = request.json["sql"]

    try:
        result = cursor.execute(sql)
        # Check if sql is select sql or execute sql
        is_query_sql = sql.lower().startswith("select")
        response = {"success": True, "query_sql": is_query_sql}

        if is_query_sql:
            schema = result.get_resultset_schema()
            row = result.fetchone()

            col_num = len(schema)
            if row is not None:
                row_data = {}
                for i in range(col_num):
                    col_name = schema[i]["name"]
                    col_value = row[i]
                    row_data[col_name] = col_value
                data_list = [row_data]
            else:
                data_list = []
            response["rows"] = data_list
            response["schema"] = schema

    except Exception as e:
        response = {"success": False, "error": str(e)}
    return jsonify(response)

@app.route('/api/tabledata', methods=['GET'])
@cross_origin()
def get_table_data():
    table_name = request.args["table"]
    sql = "SELECT * FROM {} LIMIT 10".format(table_name)
    try:
        result = cursor.execute(sql)
        # TODO: Change to fetch many instead of using limit
        schema = result.get_resultset_schema()
        row = result.fetchone()

        col_num = len(schema)

        if row is not None:
            row_data = {}
            for i in range(col_num):
                col_name = schema[i]["name"]
                col_value = row[i]
                row_data[col_name] = col_value
            # TODO: Get multiple rows instead of one row
            data_list = [row_data]
        else:
            data_list = []

        result = {"success": True, "rows": data_list, "schema": schema}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    return jsonify(result)

@app.route('/api/tasks', methods=['GET'])
@cross_origin()
def get_tasks():
    sql = "SELECT * FROM __INTERNAL_DB.JOB_INFO"
    try:
        result = cursor.execute(sql)
        schema = result.get_resultset_schema()
        row = result.fetchone()

        col_num = len(schema)

        if row is not None:
            row_data = {}
            for i in range(col_num):
                col_name = schema[i]["name"]
                col_value = row[i]
                row_data[col_name] = col_value
            data_list = [row_data]
        else:
            data_list = []

        result = {"success": True, "rows": data_list, "schema": schema}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    return jsonify(result)

@app.route('/api/server', methods=['POST'])
@cross_origin()
def update_openmldb_server():
    if request.method != 'POST':
        response = {"success": False, "error": "Unsupport method: {}".format(request.method)}
        return jsonify(response)

    # Get param from POST json instead of GET to avoid url encoding
    openmldb_server = request.json["openmldb_server"]

    try:
        default_db = "default_db"
        zk = openmldb_server.split("/")[0]
        zkPath = "/" + "/".join(openmldb_server.split("/")[1:])

        global db
        global cursor
        db = openmldb.dbapi.connect(default_db, zk, zkPath)
        cursor = db.cursor()

        response = {"success": True}
    except Exception as e:
        response = {"success": False, "error": str(e)}
    return jsonify(response)

@app.route('/api/tasklog', methods=['GET'])
@cross_origin()
def get_task_log():
    jobId = request.args["id"]
    try:
        # TODO: Check if jobId is integer
        log = cursor.connection._sdk.getJobLog(int(jobId))
        result = {"success": True, "log": log}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    return jsonify(result)

def main():
  # TODO: debug config does not work
  app.run(host=args.host,
          port=args.port,
          threaded=True,
          debug=args.debug)

if __name__ == "__main__":
  main()
