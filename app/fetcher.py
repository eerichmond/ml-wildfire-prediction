from datetime import date, datetime, timedelta
from os import path
from pandas import read_csv
import requests
from shapely.geometry import Point
import urllib.parse

soil_file = path.join(path.dirname(__file__), './models/soil.csv')
soil_df = read_csv(soil_file).drop(['cultivated_land'], axis=1)
lat_min = soil_df['lat'].min()
lat_max = soil_df['lat'].max()
long_min = soil_df['long'].min()
# HACK: subtract 0.1 to bypass NASA 10 deg range limit
long_max = soil_df['long'].max() - 0.1
soil_df = soil_df.set_index(['long', 'lat'])

weather_params = [
    'QV2M', 'T2M_RANGE', 'WS10M', 'T2M', 'PS', 'T2MDEW', 'PRECTOT'
]


def map_weather_params(date: date, row: map):
    i = date.strftime('%Y%m%d')

    return {
        'month': date.month,
        'date': date,
        'precipitation': row['PRECTOTCORR'][i],
        'pressure': row['PS'][i],
        'humidity_2m': row['QV2M'][i],
        'temp_2m': row['T2M'][i],
        'temp_dew_point_2m': row['T2MDEW'][i],
        'temp_range_2m': row['T2M_RANGE'][i],
        'wind_10m': row['WS10M'][i]
    }


def get_weather_all(date: date):
    start = date.strftime('%Y%m%d')

    params = {
        'parameters': ','.join(weather_params),
        'community': 'SB',
        'latitude-min': lat_min,
        'latitude-max': lat_max,
        'longitude-min': long_min,
        'longitude-max': long_max,
        'start': start,
        'end': start,
        'format': 'JSON',
    }
    raw_json = requests.get(
        'https://power.larc.nasa.gov/api/temporal/daily/regional', params
    ).json()

    weather_rows = []
    for row in raw_json['features']:
        long, lat, _ = row['geometry']['coordinates']

        if ((long, lat) in soil_df.index):
            print(f'({long}, {lat}) in soil_df.index = true')
            weather = {
                'long': long,
                'lat': lat,
                **map_weather_params(date, row['properties']['parameter'])
            }

            weather_rows.append(weather)
        else:
            print(f'({long}, {lat}) in soil_df.index = false')

    return weather_rows


def get_weather(date: date, long: float, lat: float):
    start = date.strftime('%Y%m%d')

    params = {
        'parameters': ','.join(weather_params),
        'community': 'SB',
        'longitude': long,
        'latitude': lat,
        'start': start,
        'end': start,
        'format': 'JSON',
    }
    raw_json = requests.get(
        'https://power.larc.nasa.gov/api/temporal/daily/point', params
    ).json()

    weather = map_weather_params(
        date, raw_json['properties']['parameter'], long, lat
    )

    return {
        'long': round(long, 1),
        'lat': round(lat, 1),
        **weather
    }


def get_drought_score(date: date, fips: int):
    start = date.strftime('%m/%d/%Y')
    end = start

    raw_json = requests.get(
        'https://usdmdataservices.unl.edu/api/CountyStatistics/GetDroughtSeverityStatisticsByAreaPercent',
        {
            'aoi': f'0{fips}',
            'startdate': start,
            'enddate': end,
            'statisticsType': 1,
        }
    ).json()

    if len(raw_json) == 0:
        return 0

    item = raw_json[0]

    return float(item['D0'])/100 + float(item['D1'])/100 \
        + float(item['D2'])/100 + float(item['D3'])/100 + float(item['D4'])/100


def get_soil(long: float, lat: float):
    soil = soil_df.loc[(round(long, 1), round(lat, 1))].to_dict()

    soil['fips'] = int(soil['fips'])

    return soil


def get_prior_fire_years(date: date, long: int, lat: int):
    url_prefix = 'https://egis.fire.ca.gov/arcgis/rest/services/FRAP/FirePerimeters_FS/FeatureServer/0/query?outFields=*&outSR=4326&f=json'

    current_year = date.year
    max_date = date
    min_date = date - timedelta(1 * 365 * 5)

    where = urllib.parse.quote(
        f"ALARM_DATE>=DATE '{min_date.strftime('%Y-%m-%d')}' and ALARM_DATE<DATE '{max_date.strftime('%Y-%m-%d')}'"
    )
    geo = f'geometryType=esriGeometryPoint&geometry={long},{lat}&spatialRel=esriSpatialRelIntersects&inSR=4326'
    url = f'{url_prefix}&where={where}&{geo}'

    results = requests.get(url).json()['features']

    years_ago = set([
        current_year - datetime
        .fromtimestamp(result['attributes']['ALARM_DATE'] / 1000)
        .year
        for result in results
    ])

    prior_fires = {
        f'prior_fire_{i}_{i+1}_year': int(i in years_ago) for i in range(5)
    }

    return prior_fires
