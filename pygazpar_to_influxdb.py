#!/usr/bin/env python3

import sys
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime
import argparse
import logging
import re
import decimal
from decimal import Decimal
import pygazpar


ENV InfluxDB_host_var=$pygazpar_influxdb2_host
ENV InfluxDB_token_var=$pygazpar_influxdb2_token
ENV InfluxDB_bucket_var=$pygazpar_influxdb2_bucket
ENV InfluxDB_org_var=$pygazpar_influxdb2_org
ENV InfluxDB_pygazpar-login_var=$pygazpar_PYGAZPAR_LOGIN
ENV InfluxDB_pygazpar-password_var=$pygazpar_PYGAZPAR_PASSWORD
ENV InfluxDB_pygazpar-pceidentifier_var=$pygazpar_PCE_IDENTIFIER




parser = argparse.ArgumentParser()

#

parser.add_argument("--source", help="Source ('json' file must be named data.json. 'pygazpar' asks to pygazpar to retrieve data)", dest="SOURCE", default="pygazpar")
parser.add_argument("--influxdb2-host", help="InfluxDB host", dest="INFLUXDB_HOST", default="influxdb-api.loc")
parser.add_argument("--influxdb2-token", help="InfluxDB token", dest="INFLUXDB_TOKEN", default="xxxxx")
parser.add_argument("--influxdb2-bucket", help="InfluxDB bucket", dest="INFLUXDB_BUCKET", default="gazpar/autogen")
parser.add_argument("--influxdb2-org", help="InfluxDB org", dest="INFLUXDB_ORG", default="home")
parser.add_argument("-v", "--verbose", dest="verbose_count", action="count", default=0, help="increases log verbosity")
parser.add_argument("--pygazpar-login", dest="PYGAZPAR_LOGIN", help="pygazpar login")
parser.add_argument("--pygazpar-password", dest="PYGAZPAR_PASSWORD", help="pygazpar password")
parser.add_argument("--pygazpar-pceidentifier", dest="PCE_IDENTIFIER", help="pygazpar-pceidentifier")
#parser.add_argument("--pygazpar-frequency", dest="Frequency.DAILY", help="pygazpar-frequency")


args = parser.parse_args()
log = logging.getLogger()
logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                    format='%(name)s (%(levelname)s): %(message)s')
log.setLevel(max(3 - args.verbose_count, 0) * 10)




url = InfluxDB_host_var
bucket = InfluxDB_bucket_var
token = InfluxDB_token_var
org = InfluxDB_org_var







influxclient = InfluxDBClient(url=url, token=token, org=org)

write_api = influxclient.write_api(write_options=SYNCHRONOUS)



#------------------------------------------------- 
        
client = pygazpar.Client(InfluxDB_pygazpar-login_var,
                         InfluxDB_pygazpar-password_var,
                         InfluxDB_pygazpar-pceidentifier_var,
                         pygazpar.Frequency.DAILY,
                         30,
                         '/tmp')

log.debug('Starting to update pygazpar data')
client.update()
log.debug('End update pygazpar data')

data = client.data()

jsonInflux = []

for measure in data:
    print(measure)
    date_time_obj = datetime.datetime.strptime(measure['time_period'], '%d/%m/%Y')
    if 'start_index_m3' in measure:
      jsonInflux.append({
        "measurement": "gazpar_consumption_per_day",
        "tags": {
        },
        "time": date_time_obj.strftime('%Y-%m-%dT%H:%M:%S'),
        "fields": {
            "value": measure['volume_m3'],
            "start_index_m3": measure['start_index_m3'],
            "end_index_m3": measure['end_index_m3'],
            "volume_m3": measure['volume_m3'],
            "energy_kwh": measure['energy_kwh'],
            "type": measure['type'],
        }
    })
    else:
      print('No measure')

write_api.write(bucket=bucket, record=jsonInflux)
