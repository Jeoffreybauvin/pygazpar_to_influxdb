# pygazpar_to_influxdb

![Docker Build Status](https://img.shields.io/docker/cloud/automated/jeoffrey54/pygazpar_to_influxdb.svg) ![Docker Build Status](https://img.shields.io/docker/cloud/build/jeoffrey54/pygazpar_to_influxdb.svg)


This repository uses [PyGazpar](https://github.com/ssenart/PyGazpar) to retrieve natural gas consumption from GrDF French provider, and push it to InfluxDB.
It is designed in order to connect to the version 2.0 of Influx data base

## Setup

There is a Docker image ready to use : https://hub.docker.com/repository/docker/pbranly/pygazpar_test

```bash
docker run -ti  --rm -v /dev/shm:/dev/shm  pbranly/pygazpar_to_influxdb:0.2.5 pygazpar_to_influxdb.py --influxdb2-host 192.168.1.x:8086  --influxdb2-token xxxxxxxxxxxxxxxxxxxx  --influxdb2-bucket gazpar/autogen  --influxdb2-org xxx  --pygazpar-login 'xxx@fff.fr' --pygazpar-password 'fgfgfrt' -vvv
```
