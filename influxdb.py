from datetime import timezone, datetime
from influxdb_client import InfluxDBClient, WriteApi, QueryApi, DeleteApi, Point
from influxdb_client.client.write_api import SYNCHRONOUS

g_bucket = ''
g_org = ''
g_client: InfluxDBClient | None = None
g_write_api: WriteApi | None = None
g_read_api: QueryApi | None = None
g_delete_api: DeleteApi | None = None


def init_influxdb(bucket, org, token, url):
    global g_bucket
    global g_org
    global g_client
    global g_write_api
    global g_read_api
    global g_delete_api

    g_client = InfluxDBClient(
        url=url,
        token=token,
        org=org)

    g_bucket = bucket
    g_org = org
    g_write_api = g_client.write_api(write_options=SYNCHRONOUS)
    g_read_api = g_client.query_api()
    g_delete_api = g_client.delete_api()


def is_connected():
    return g_client.ping() and \
        (g_write_api is not None) and \
        (g_read_api is not None) and \
        (g_delete_api is not None)


class PointData:
    def __init__(self, is_field: bool, key: str, value: str):
        self.is_field = is_field
        self.key = key
        self.value = value


def write(measurement_name: str, timestamp: datetime | None, fields: list[PointData]):
    if not is_connected():
        print('ERROR: InfluxDB not initialized')
        return

    p = Point(measurement_name)

    if timestamp is not None:
        p = p.time(timestamp.isoformat())

    for field in fields:
        if field.is_field:
            p = p.field(field.key, field.value)
        else:
            p = p.tag(field.key, field.value)

    g_write_api.write(g_bucket, g_org, p)


def read_all(measurement_name: str):
    if not is_connected():
        print('ERROR: InfluxDB not initialized')
        return

    query = f'from(bucket: "{g_bucket}")' \
            f'|> range(start: 1970-01-01T00:00:00Z)' \
            f'|> filter(fn: (r) => r._measurement == "{measurement_name}")' \
            f'|> last()'

    result = g_read_api.query(query, g_org)

    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    return results


def delete_all(measurement_name: str):
    if not is_connected():
        print('ERROR: InfluxDB not initialized')
        return

    g_delete_api.delete(
        start='1970-01-01T00:00:00Z',
        stop=datetime.now(tz=timezone.utc).isoformat(),
        predicate=f'_measurement="{measurement_name}"',
        bucket=g_bucket,
        org=g_org)
