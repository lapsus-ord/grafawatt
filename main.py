import os
import rte_data as rte
import influxdb as db
from datetime import datetime, timezone
from influxdb import PointData
from dotenv import load_dotenv
from influxdb_client.rest import ApiException

load_dotenv('.env')
bucket = os.getenv('INFLUXDB_BUCKET')
org = os.getenv('INFLUXDB_ORG')
token = os.getenv('INFLUXDB_TOKEN')
url = f'http://localhost:{os.getenv("INFLUXDB_PORT")}'


def main():
    db.init_influxdb(bucket, org, token, url)
    print('[STATUS] is db alive?', db.is_connected())
    # db.delete_all('eco2mix_national_measurement')  # DEBUG

    # 1. read config to get last fetch to ODRÉ
    config = open('grafawatt.config', 'r')
    last_fetch_date = datetime.fromisoformat(config.read())
    config.close()

    # 2. first fetch
    fetch = rte.get_latest_eco2mix_national_data(last_fetch_date)
    result = fetch

    # 3. update last date of the fetch
    last_fetch_date = fetch[-1].date

    number_of_fetch = 1
    # 4. continue to fetch until no more are required
    #    equivalent to: last_fetch_date = datetime.now()
    while len(fetch) >= 99:
        print(f'[{number_of_fetch}] doing a fetch, date: {fetch[0].date.isoformat()}, count: {len(fetch)}')
        fetch = rte.get_latest_eco2mix_national_data(last_fetch_date)
        fetch.pop(0)  # info: to remove duplicate
        result = result + fetch

        last_fetch_date = fetch[-1].date
        number_of_fetch += 1

    print(f'[RESULT]'
          f'\n\ttotal_record: {len(result)}'
          f'\n\tnumber of fetch: {number_of_fetch}'
          f'\n\tlast_date: {result[-1].date.isoformat()}')

    number_of_insert = 1
    # 5. send to influxdb
    for record in result:
        print(f'[{number_of_insert}] doing an insert, date: {record.date.isoformat()}')
        try:
            db.write(
                'eco2mix_national_measurement',
                record.date,
                [
                    PointData(False, 'perimeter', record.perimeter),
                    PointData(True, 'consumption', record.consumption),
                    PointData(True, 'nuclear', record.nuclear),
                    PointData(True, 'coal', record.coal),
                    PointData(True, 'solar', record.solar),
                    PointData(True, 'fuel_oil', record.fuel_oil),
                    PointData(True, 'bioenergies', record.bioenergies),
                    PointData(True, 'hydro', record.hydro),
                    PointData(True, 'gas', record.gas),
                    PointData(True, 'wind', record.wind),
                    PointData(True, 'co2', record.co2),
                ])
            last_fetch_date = record.date
        except ApiException:
            print('ERROR: when persisting to database')

    # 6. save last inserted record date in the config
    config = open('grafawatt.config', 'w')
    config.write(last_fetch_date.isoformat())
    config.close()


if __name__ == '__main__':
    main()
