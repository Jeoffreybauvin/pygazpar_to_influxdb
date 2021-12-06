# pygazpar_to_influxdb

![Docker Build Status](https://img.shields.io/docker/cloud/automated/jeoffrey54/pygazpar_to_influxdb.svg) ![Docker Build Status](https://img.shields.io/docker/cloud/build/jeoffrey54/pygazpar_to_influxdb.svg)


This repository uses [PyGazpar](https://github.com/ssenart/PyGazpar) to retrieve natural gas consumption from GrDF French provider, and push it to InfluxDB.
It is designed in order to connect to the version 2.0 of Influx data base

This repository is a fork of the https://github.com/Jeoffreybauvin/pygazpar_to_influxdb dedicated version 1.8 of Influxdb

A tentative configuration is described for Influxdb 1.8 but not tested

## Setup

There is a Docker image ready to use : https://hub.docker.com/repository/docker/pbranly/pygazpar_to_influxdb

Docker compose part is given hereunder:

```bash

#define a pygazpar2 service sans firefox et geckodriver

  pygazpar2test1:
    container_name: pygazpar2_test1
    image: pbranly/pygazpar_to_influxdb:0.4.1
    env_file:
         - .env
    depends_on:
      - influxdb2
```     

Parameters to include in your .env file:

For Influxdb 2.0:
With:
- PYPAZPAR_INFLUXDB2_HOST="local ip host of your Influxdb database:port of yourInfluxdb database" exemple: "192.168.1.20:8086"
- PYPAZPAR_INFLUXDB2_TOKEN="token of your Influxdb 2.0 data base (to find in influxdb)"
- PYPAZPAR_INFLUXDB2_BUCKET="name of the influxdb 2 bucket in which you want to write gazpar data"
- PYPAZPAR_INFLUXDB2_ORG="name of your influxdb 2 organization"
- PYPAZPAR_PYGAZPAR_LOGIN="login of your GRDF account"
- PYPAZPAR_PYGAZPAR_PASSWORD="password of your GRDF password"
- PYPAZPAR_PCE_IDENTIFIER="Identifier opf your GRDF PCE (remove blanks)"

For Influxdb 1.8: (not tested)
With:
- PYPAZPAR_INFLUXDB2_HOST="local ip host of your Influxdb database:port of yourInfluxdb database" exemple: "192.168.1.20:8086"
- PYPAZPAR_INFLUXDB2_TOKEN="USERNAME:PASSWORD of your Influxdb 1.8 database)" <------------------
- PYPAZPAR_INFLUXDB2_BUCKET="nDATABASE/RETENTION of your Influxdb 1.8 database. for exemple home_assistant/autogen" <--------------------------
- PYPAZPAR_INFLUXDB2_ORG="_" <-----------------------
- PYPAZPAR_PYGAZPAR_LOGIN="login of your GRDF account"
- PYPAZPAR_PYGAZPAR_PASSWORD="password of your GRDF password"
- PYPAZPAR_PCE_IDENTIFIER="Identifier opf your GRDF PCE (remove blanks)"