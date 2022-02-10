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

db = openmldb.dbapi.connect("db1", "127.0.0.1:6181", "/onebox")
cursor = db.cursor()

@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")

@app.route('/api/dbs')
@cross_origin()
def get_dbs():
    # TODO: Not supported yet
    return render_template("index.html")

@app.route('/api/tables')
@cross_origin()
def get_tables():
    tableNames = cursor.get_all_tables()
    tableNameMap = []
    for tableName in tableNames:
        tableNameMap.append({"name": tableName})
    result = {"tables": tableNameMap}
    return jsonify(result)

@app.route('/api/executesql', methods=['GET'])
@cross_origin()
def execute_sql():
    sql = request.args["sql"]
    try:
        cursor.execute(sql)
        result = {"success": True}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    return jsonify(result)

@app.route('/api/querysql', methods=['GET'])
@cross_origin()
def query_sql():
    sql = request.args["sql"]
    try:
        rs = cursor.execute(sql)
        # TODO: Support fetch all later
        row = rs.fetchone()
        result = {"success": True, "rows": [list(row)]}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    return jsonify(result)

@app.route('/api/tabledata', methods=['GET'])
@cross_origin()
def get_table_data():
    table_name = request.args["table"]
    sql = "SELECT * FROM {} LIMIT 3".format(table_name)
    try:
        result = cursor.execute(sql)
        # TODO: Change to fetch many instead of using limit
        schema = result.get_resultset_schema()
        row = result.fetchone()

        col_num = len(schema)
        row_data = {}
        for i in range(col_num):
            col_name = schema[i]["name"]
            col_value = row[i]
            row_data[col_name] = col_value
        # TODO: Get multiple rows instead of one row
        data_list = [row_data]

        result = {"success": True, "rows": data_list, "schema": schema}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    return jsonify(result)

def main():
  app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
  main()