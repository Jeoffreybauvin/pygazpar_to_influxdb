#!/usr/bin/env python3

import sys
import json
from influxdb-client import InfluxDBClient
import datetime
import argparse
import logging
import re
import decimal
from decimal import Decimal
import pygazpar


parser = argparse.ArgumentParser()

#

parser.add_argument("--source", help="Source ('json' file must be named data.json. 'pygazpar' asks to pygazpar to retrieve data)", dest="SOURCE", default="pygazpar")
parser.add_argument("--influxdb-host", help="InfluxDB host", dest="INFLUXDB_HOST", default="influxdb-api.loc")
parser.add_argument("--influxdb-port", help="InfluxDB port", dest="INFLUXDB_PORT", default=8086)
parser.add_argument("--influxdb-username", help="InfluxDB username", dest="INFLUXDB_USERNAME", default="username")
parser.add_argument("--influxdb-password", help="InfluxDB password", dest="INFLUXDB_PASSWORD", default="password")
parser.add_argument("--influxdb-database", help="InfluxDB database", dest="INFLUXDB_DATABASE", default="enedis")
parser.add_argument("-v", "--verbose", dest="verbose_count", action="count", default=0, help="increases log verbosity")
parser.add_argument("--pygazpar-login", dest="PYGAZPAR_LOGIN", help="pygazpar login")
parser.add_argument("--pygazpar-password", dest="PYGAZPAR_PASSWORD", help="pygazpar password")

args = parser.parse_args()
log = logging.getLogger()
logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                    format='%(name)s (%(levelname)s): %(message)s')
log.setLevel(max(3 - args.verbose_count, 0) * 10)

influx_client = InfluxDBClient(
    host=args.INFLUXDB_HOST,
    port=args.INFLUXDB_PORT,
    username=args.INFLUXDB_USERNAME,
    password=args.INFLUXDB_PASSWORD,
    database=args.INFLUXDB_DATABASE,
    timeout=5,
    retries=2,
)

client = pygazpar.Client(args.PYGAZPAR_LOGIN,
                         args.PYGAZPAR_PASSWORD,
                         'geckodriver',
                         30,
                         '/tmp')

log.debug('Starting to update pygazpar data')
client.update()
log.debug('End update pygazpar data')

data = client.data()

jsonInflux = []

for measure in data:
    date_time_obj = datetime.datetime.strptime(measure['time_period'], '%d/%m/%Y')

    jsonInflux.append({
        "measurement": "gazpar_consumption_per_day",
        "tags": {
        },
        "time": date_time_obj.strftime('%Y-%m-%dT%H:%M:%S'),
        "fields": {
            "value": measure['volume_m3'],
            "start_index_m3": measure['start_index_m3'],
            "end_index_m3": measure['end_index_m3'],
            "energy_kwh": measure['energy_kwh'],
            "converter_factor_kwh/m3": measure['converter_factor_kwh/m3'],
            "temperature_degC": measure['temperature_degC'],
            "type": measure['type'],
        }
    })

influx_client.write_points(jsonInflux, batch_size=10)
