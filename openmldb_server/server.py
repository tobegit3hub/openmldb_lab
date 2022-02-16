#!/usr/bin/env python3

import os
import sys
import logging
import argparse
import webbrowser
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
    default=bool(os.environ.get("DEBUG", "false")),
    help="Enable debug for flask or not(eg. true)",
    type=bool)

args = parser.parse_args(sys.argv[1:])
for arg in vars(args):
    logger.info("{}: {}".format(arg, getattr(args, arg)))

global db
global cursor
global current_default_db
global current_zk
global current_zk_path

current_default_db = args.default_db
current_zk = args.zk
current_zk_path = args.zk_path

try:
    db = openmldb.dbapi.connect(current_default_db, current_zk, current_zk_path)
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
        response = {"success": False, "error": "Unsupported method: {}".format(request.method)}
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
            col_num = len(schema)
            rows = result.fetchall()

            return_rows_list = []
            for row in rows:
                row_data = {}
                for i in range(col_num):
                    col_name = schema[i]["name"]
                    col_value = row[i]
                    row_data[col_name] = col_value
                return_rows_list.append(row_data)

            response["rows"] = return_rows_list
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
        schema = result.get_resultset_schema()
        col_num = len(schema)
        rows = result.fetchmany(10)

        return_rows_list = []
        for row in rows:
            row_data = {}
            for i in range(col_num):
                col_name = schema[i]["name"]
                col_value = row[i]
                row_data[col_name] = col_value
            return_rows_list.append(row_data)

        result = {"success": True, "rows": return_rows_list, "schema": schema}
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
        col_num = len(schema)

        rows = result.fetchall()

        return_rows_list = []
        for row in rows:
            row_data = {}
            for i in range(col_num):
                col_name = schema[i]["name"]
                col_value = row[i]
                row_data[col_name] = col_value
            return_rows_list.append(row_data)

        result = {"success": True, "rows": return_rows_list, "schema": schema}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    return jsonify(result)

@app.route('/api/server', methods=['POST'])
@cross_origin()
def update_openmldb_server():
    if request.method != 'POST':
        response = {"success": False, "error": "Unsupported method: {}".format(request.method)}
        return jsonify(response)

    # Get param from POST json instead of GET to avoid url encoding
    openmldb_server = request.json["openmldb_server"]

    try:
        zk = openmldb_server.split("/")[0]
        zkPath = "/" + "/".join(openmldb_server.split("/")[1:])

        global db
        global cursor
        global current_default_db
        global current_zk
        global current_zk_path

        # Update zk and zk path
        current_zk = zk
        current_zk_path = zkPath
        db = openmldb.dbapi.connect(current_default_db, current_zk, current_zk_path)
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

@app.route('/api/defaultdb', methods=['POST'])
@cross_origin()
def update_default_db():
    if request.method != 'POST':
        response = {"success": False, "error": "Unsupported method: {}".format(request.method)}
        return jsonify(response)

    default_db = request.json["db"]

    try:
        global db
        global cursor
        global current_default_db
        global current_zk
        global current_zk_path

        # Update default db
        current_default_db = default_db

        db = openmldb.dbapi.connect(current_default_db, current_zk, current_zk_path)
        cursor = db.cursor()

        response = {"success": True}
    except Exception as e:
        response = {"success": False, "error": str(e)}
    return jsonify(response)

def main():
  # Start web browser if possible
  # webbrowser.open("http://{}:{}".format(args.host, args.port))

  # TODO: debug config does not work
  app.run(host=args.host,
          port=args.port,
          threaded=True,
          debug=args.debug)

if __name__ == "__main__":
  main()
