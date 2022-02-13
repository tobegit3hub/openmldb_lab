#!/usr/bin/env python3

import logging
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import openmldb.dbapi

app = Flask(__name__,
            template_folder="./dist/",
            static_folder="./dist",
            static_url_path="")
cors = CORS(app, resources=r'/*')

app.config['CORS_HEADERS'] = 'Content-Type'

global db
global cursor

try:
    db = openmldb.dbapi.connect("db1", "127.0.0.1:6181", "/onebox")
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

def main():
  app.run(host="0.0.0.0", port=7788)

if __name__ == "__main__":
  main()
