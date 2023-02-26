import datetime

import influxdb_client
from influxdb_client import WriteApi, QueryApi, DeleteApi
from influxdb_client.client.write_api import SYNCHRONOUS

g_bucket = ''
g_org = ''

g_write_api: WriteApi | None = None
g_read_api: QueryApi | None = None
g_delete_api: DeleteApi | None = None

def init_influxdb(bucket, org, token, url):
    global g_bucket
    global g_org
    global g_write_api
    global g_read_api
    global g_delete_api

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org,
    )

    g_bucket = bucket
    g_org = org
    g_write_api = client.write_api(write_options=SYNCHRONOUS)
    g_read_api = client.query_api()
    g_delete_api = client.delete_api()


def is_not_connected():
    return (g_write_api is None) and (g_read_api is None) and (g_delete_api is None)


def write(point: str, tuple_field_value: (str, str)):
    if is_not_connected():
        print('ERROR: InfluxDB not initialized')
        return

    field, value = tuple_field_value

    p = influxdb_client \
        .Point(point) \
        .tag("location", "London") \
        .field(field, value)

    g_write_api.write(g_bucket, g_org, p)


def read_all(measurement: str):
    if is_not_connected():
        print('ERROR: InfluxDB not initialized')
        return

    query = f'from(bucket: "{g_bucket}")\
        |> range(start: -1h)\
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")'

    result = g_read_api.query(query, g_org)

    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    return results


def delete_all(measurement: str): # problem here...
    g_delete_api.delete('-999', '0', f'_measurement="{measurement}"', g_bucket, g_org)
