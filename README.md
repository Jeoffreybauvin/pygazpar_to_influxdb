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

#define a pygazpar2 service

  pygazpar2:
    container_name: pygazpar2
    image: pbranly/pygazpar_to_influxdb:latest
    command: pygazpar_to_influxdb.py --influxdb2-host 192.168.x.x:8086  --influxdb2-token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --influxdb2-bucket home_assistant  --influxdb2-org home  --pygazpar-login 'xxx@yy.fr' --pygazpar-password 'yyyyyyyyyy' --pygazpar-pceidentifier 12345678901234 -vvv
    depends_on:
      - influxdb2
```     

For Influxdb 2.0:
With:
- influxdb2-host: local ip host of your Influxdb database
- influxdb2-token: token of your Influxdb 2.0 data base (to find in influxdb)
- influxdb2-bucket: name of the influxdb 2 bucket in which you want to write gazpar data
- influxdb2-org: name of your influxdb 2 organization
- pygazpar-login: login of your GRDF account
- pygazpar-password: password of your GRDF password
- pygazpar-pceidentifier: Identifier opf your GRDF PCE (remove blanks)


For Influxdb 1.8: (not tested)
With:
- influxdb2-host: local ip host of your Influxdb database
- influxdb2-token: USERNAME:PASSWORD of your Influxdb 1.8 database <--------------------
- influxdb2-bucket: DATABASE/RETENTION of your Influxdb 1.8 database. for exemple home_assistant/autogen <--------------------------
- influxdb2-org: "-" <-------------------------------
- pygazpar-login: login of your GRDF account
- pygazpar-password: password of your GRDF password
- pygazpar-pceidentifier: Identifier opf your GRDF PCE (remove blanks)