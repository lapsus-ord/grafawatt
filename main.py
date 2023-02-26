import os
import influxdb as db
from dotenv import load_dotenv

load_dotenv('.env')
bucket = os.getenv('INFLUXDB_BUCKET')
org = os.getenv('INFLUXDB_ORG')
token = os.getenv('INFLUXDB_TOKEN')
url = f'http://localhost:{os.getenv("INFLUXDB_PORT")}'


def main():
    db.init_influxdb(bucket, org, token, url)

    print('is connected?', not db.is_not_connected())
    print('read:', db.read_all('temperature'))


if __name__ == '__main__':
    main()
