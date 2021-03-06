# pygazpar_to_influxdb

![Docker Build Status](https://img.shields.io/docker/cloud/automated/jeoffrey54/pygazpar_to_influxdb.svg) ![Docker Build Status](https://img.shields.io/docker/cloud/build/jeoffrey54/pygazpar_to_influxdb.svg)


This repository uses [PyGazpar](https://github.com/ssenart/PyGazpar) to retrieve natural gas consumption from GrDF French provider, and push it to InfluxDB.

## Setup

There is a Docker image ready to use : https://hub.docker.com/r/jeoffrey54/pygazpar_to_influxdb

```bash
docker run -ti  --rm -v /dev/shm:/dev/shm  pygazpar:latest  pygazpar_to_influxdb.py --influxdb-host 192.168.1.2 --influxdb-port 8086  --influxdb-username gazpar --influxdb-password PASSWORD  --influxdb-database gazpar  --pygazpar-login 'mail@gmail.com' --pygazpar-password 'password'
```
