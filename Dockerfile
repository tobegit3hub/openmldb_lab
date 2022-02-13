FROM python:3.9

# Install dependencies
RUN apt-get update -y
RUN apt-get install -y vim
RUN apt-get install -y npm

# Add source code
ADD . /openmldb_lab/

WORKDIR /openmldb_lab/

# Install openmldb_lab
RUN ./install.sh
RUN python ./setup.py install

EXPOSE 7788

CMD ["openmldb_lab"]
