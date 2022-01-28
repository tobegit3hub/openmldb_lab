#!/usr/bin/env python3

from flask import Flask, render_template

app = Flask(__name__,
            template_folder="./dist/",
            static_folder="./dist",
            static_url_path="")

@app.route('/')
def index():
    return render_template("index.html")

def main():
  app.run(host="0.0.0.0")

if __name__ == "__main__":
  main()