# OpenMLDB Lab

## Intro

The web lab of [OpenMLDB](https://github.com/4paradigm/openmldb) which provides battery-included functions.

* Web Console of OpenMLDB databases
* Playground of OpenMLDB SQL
* Multiple labs for beginners
* SQL debugger of OpenMLDB SQL

## Install

Install OpenMLDB firstly with <https://github.com/4paradigm/openmldb>.

Install OpenMLDB Lab with single script.

```
./install.sh
```

## Usage

Start the server with single script.

```
./start.sh
```

Then open browser in `http://127.0.0.1:5000`.

![](./images/lab1.png)

## Development

Front-end uses [Vue.js](https://vuejs.org/) in JavaScript and we can start front-end directly.

```
cd ./vueapp/

npm run serve
```

Back-end uses [Flask](https://flask.palletsprojects.com/) in Python and we can start the server.

```
cd ./openmldb_server/

FLASK_ENV=development FLASK_APP=server flask run
```

## License

[Apache License](./LICENSE)
