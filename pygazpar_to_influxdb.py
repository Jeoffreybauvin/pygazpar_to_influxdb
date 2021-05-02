#!/usr/bin/env python3

import sys
import json
# from influxdb_client import InfluxDBClient
#from influxdb_client import InfluxDBClient
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
parser.add_argument("--influxdb2-host", help="InfluxDB host", dest="INFLUXDB_HOST", default="influxdb-api.loc")
parser.add_argument("--influxdb2-token", help="InfluxDB token", dest="INFLUXDB_TOKEN", default="xxxxx")
parser.add_argument("--influxdb2-bucket", help="InfluxDB bucket", dest="INFLUXDB_BUCKET", default="gazpar")
parser.add_argument("--influxdb2-org", help="InfluxDB org", dest="INFLUXDB_ORG", default="home")
parser.add_argument("-v", "--verbose", dest="verbose_count", action="count", default=0, help="increases log verbosity")
parser.add_argument("--pygazpar-login", dest="PYGAZPAR_LOGIN", help="pygazpar login")
parser.add_argument("--pygazpar-password", dest="PYGAZPAR_PASSWORD", help="pygazpar password")

args = parser.parse_args()
log = logging.getLogger()
logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                    format='%(name)s (%(levelname)s): %(message)s')
log.setLevel(max(3 - args.verbose_count, 0) * 10)

#influx_client = InfluxDBClient(
#    host=args.INFLUXDB_HOST,
#    token=args.INFLUXDB_TOKEN,
#    org=args.INFLUXDB_ORG,
#)
#--------------------------------------------------------------

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "gazpar/autogen"

client = InfluxDBClient(url="http://192.168.1.8:8087", token="dh7nwLEm6Oky80aWPW2zcP31I6lBJ4Rq9MfeMv46011us7lExORlcvZIaV2XF6COEdBEFKcgOtUJsjr_JGaKNg==", org="home")

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

p = Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)

write_api.write(bucket=bucket, record=p)


#------------------------------------------------- 
        
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

# influx_client.write_points(jsonInflux, batch_size=10)
write_api.write(bucket=bucket, jsonInflux, batch_size=10)