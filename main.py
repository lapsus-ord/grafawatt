import os
import influxdb as db
from influxdb import PointData
from dotenv import load_dotenv

load_dotenv('.env')
bucket = os.getenv('INFLUXDB_BUCKET')
org = os.getenv('INFLUXDB_ORG')
token = os.getenv('INFLUXDB_TOKEN')
url = f'http://localhost:{os.getenv("INFLUXDB_PORT")}'


def main():
    db.init_influxdb(bucket, org, token, url)
    print('is connected?', not db.is_not_connected())

    db.delete_all('test_measurement')
    db.write('test_measurement', [
        PointData(False, 'tag_key1', 'tag_value1'),
        PointData(True, 'field_key1', 'field_value1'),
    ])
    print('read:', db.read_all('test_measurement'))


if __name__ == '__main__':
    main()
