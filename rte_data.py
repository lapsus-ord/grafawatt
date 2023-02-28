import requests
from datetime import datetime, timezone

odre_base_api = 'https://odre.opendatasoft.com/api/v2'


class Eco2mixNationalData:
    def __init__(self,
                 date: datetime,
                 perimeter: str,
                 consumption: int,
                 nuclear: int,
                 coal: int,
                 solar: int,
                 fuel_oil: int,
                 bioenergies: int,
                 hydro: int,
                 gas: int,
                 wind: int,
                 co2: int):
        self.date = date
        self.perimeter = perimeter
        self.consumption = consumption
        self.nuclear = nuclear
        self.coal = coal
        self.solar = solar
        self.fuel_oil = fuel_oil
        self.bioenergies = bioenergies
        self.hydro = hydro
        self.gas = gas
        self.wind = wind
        self.co2 = co2


def get_latest_eco2mix_national_data(date_ago: datetime):
    """date_ago needs to be in the UTC timezone"""

    dataset_id = 'eco2mix-national-tr'

    fields = [
        'perimetre',
        'nature',
        'date_heure',  # or 'date' & 'heure'
        'consommation',
        'nucleaire', 'charbon', 'solaire', 'fioul', 'bioenergies', 'hydraulique', 'gaz', 'eolien',
        'taux_co2',
    ]

    params = {
        'select': ','.join(fields),
        'order_by': 'date_heure asc',
        'limit': 100,
        'where': f'date_heure >= date\'{date_ago}\' and '
                 f'date_heure < date\'{datetime.now(tz=timezone.utc).isoformat()}\' and '
                 'consommation is not null',
    }
    r = requests.get(f'{odre_base_api}/catalog/datasets/{dataset_id}/records', params=params)
    if r.status_code != 200:
        print('ERROR: when sending request to ODRÉ api')
        return None

    result = []
    for record_container in r.json()['records']:
        fields = record_container['record']['fields']
        record = Eco2mixNationalData(
            datetime.fromisoformat(fields['date_heure']),
            fields['perimetre'],
            fields['consommation'],
            fields['nucleaire'],
            fields['charbon'],
            fields['solaire'],
            fields['fioul'],
            fields['bioenergies'],
            fields['hydraulique'],
            fields['gaz'],
            fields['eolien'],
            fields['taux_co2'])
        result.append(record)

    return result
