#!/usr/bin/env python3

from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import openmldb.dbapi

app = Flask(__name__,
            template_folder="./dist/",
            static_folder="./dist",
            static_url_path="")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = openmldb.dbapi.connect("db_test", "127.0.0.1:6181", "/onebox")
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
    tables = cursor.get_all_tables()
    #import ipdb;ipdb.set_trace()
    return jsonify(tables=tables)

def main():
  app.run(host="0.0.0.0")

if __name__ == "__main__":
  main()