from datetime import date, datetime, timedelta
import numpy as np
from os import path
import pandas as pd
import requests
from shapely.geometry import Point
import time
import urllib.parse

soil_file = path.join(path.dirname(__file__), './models/soil.csv')
soil_df = pd.read_csv(soil_file)
ca_lat_min = soil_df['lat'].min()
ca_lat_max = soil_df['lat'].max()
ca_long_min = soil_df['long'].min()

# HACK: subtract 0.2 to bypass NASA 10 deg range limit
ca_long_max = int(soil_df['long'].max() * 10 - 2)/10
soil_df = soil_df.set_index(['long', 'lat'])

weather_params = [
    'QV2M', 'T2M_RANGE', 'WS10M', 'T2M', 'PS', 'T2MDEW', 'PRECTOT'
]


def map_weather_params(date: date, row: dict):
    i = date.strftime('%Y%m%d')

    return {
        'date': date,
        'month': date.month,
        'precipitation': row['PRECTOTCORR'][i],
        'pressure': row['PS'][i],
        'humidity_2m': row['QV2M'][i],
        'temp_2m': row['T2M'][i],
        'temp_dew_point_2m': row['T2MDEW'][i],
        'temp_range_2m': row['T2M_RANGE'][i],
        'wind_10m': row['WS10M'][i]
    }


def get_all_features(
    date: date, *, long_min=ca_long_min, long_max=ca_long_max, lat_min=ca_lat_min, lat_max=ca_lat_max, limit: int = -1
):
    start = date.strftime('%Y%m%d')

    timer = time.perf_counter()
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

    if 'messages' in raw_json and len(raw_json['messages']) > 0:
        raise Exception(raw_json['messages'])

    print(f'NASA weather API: {(time.perf_counter() - timer):.2f}s')

    weather_rows = []
    for row in raw_json['features']:
        weather_long, weather_lat, _ = row['geometry']['coordinates']
        weather = {
            'point': Point(weather_long, weather_lat),
            **map_weather_params(date, row['properties']['parameter'])
        }

        weather_rows.append(weather)

    features = []
    i = 0
    for row in soil_df.itertuples():
        if i == limit:
            break

        i = i + 1
        long = row.Index[0]
        lat = row.Index[1]
        soil = row._asdict()

        min_dist = 100
        closet_weather = {}
        for weather in weather_rows:
            soil_point = Point(long, lat)
            dist = soil_point.distance(weather['point'])
            if (dist < min_dist):
                closet_weather = weather
                min_dist = dist
                if (min_dist < 0.1):
                    break

        timer_step = time.perf_counter()
        drought_score = get_drought_score(date, row.fips)
        print(f'Drought API: {(time.perf_counter() - timer_step):.2f}s')

        timer_step = time.perf_counter()
        prior_fire_years = get_prior_fire_years(date, long, lat)
        print(f'Prior fire API: {(time.perf_counter() - timer_step):.2f}s')

        feature = {
            'long': long,
            'lat': lat,
            **closet_weather,
            'drought_score': drought_score,
            **soil,
            **prior_fire_years
        }
        del feature['Index']
        del feature['point']

        features.append(feature)

    print(f'get_all_features took {(time.perf_counter() - timer):.2f}s')

    return features


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

    if 'messages' in raw_json and len(raw_json['messages']) > 0:
        raise Exception(raw_json['messages'])

    weather = map_weather_params(date, raw_json['properties']['parameter'])

    return {
        'long': round(long, 1),
        'lat': round(lat, 1),
        **weather
    }


def combine_drought_scores(item: dict) -> float:
    return float(item['D0'])/100 + float(item['D1'])/100 \
        + float(item['D2'])/100 + float(item['D3'])/100 + float(item['D4'])/100


drought_score_cache = {}


def get_drought_score(date: date, fips: int) -> float:
    if (fips in drought_score_cache.keys()):
        return drought_score_cache[fips]

    items = requests.get(
        'https://usdmdataservices.unl.edu/api/CountyStatistics/GetDroughtSeverityStatisticsByAreaPercent',
        {
            'aoi': f'0{fips}',
            'startdate': date.strftime('%m/%d/%Y'),
            'enddate': date.strftime('%m/%d/%Y'),
            'statisticsType': 1,
        }
    ).json()

    score = 0 if len(items) == 0 else combine_drought_scores(items[0])

    drought_score_cache[fips] = score

    return score


def get_soil(long: float, lat: float) -> dict:
    soil = soil_df.loc[(round(long, 1), round(lat, 1))].to_dict()

    soil['fips'] = int(soil['fips'])

    return soil


def get_prior_fire_years(date: date, long: float, lat: float):
    url_prefix = 'https://egis.fire.ca.gov/arcgis/rest/services/FRAP/FirePerimeters_FS/FeatureServer/0/query?outFields=*&outSR=4326&f=json'

    current_year = date.year
    max_date = date
    min_date = date - timedelta(1 * 365 * 5)

    where = urllib.parse.quote(
        f"ALARM_DATE>=DATE '{min_date.strftime('%Y-%m-%d')}' and ALARM_DATE<DATE '{max_date.strftime('%Y-%m-%d')}'"
    )
    geo = f'geometryType=esriGeometryPoint&geometry={long},{lat}&spatialRel=esriSpatialRelIntersects&inSR=4326'
    url = f'{url_prefix}&where={where}&{geo}'

    response_json = requests.get(url).json()

    if ('error' in response_json):
        raise Exception(response_json['error']['message'])

    results = response_json['features']

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


def get_ca_fire_geo(start_date: date, end_date: date):
    url_prefix = 'https://egis.fire.ca.gov/arcgis/rest/services/FRAP/FirePerimeters_FS/FeatureServer/0/query?outFields=ALARM_DATE&outSR=4326&f=json'

    where = urllib.parse.quote(
        f"STATE='CA' and ALARM_DATE>=DATE '{start_date.strftime('%Y-%m-%d')}' and ALARM_DATE<DATE '{end_date.strftime('%Y-%m-%d')}'"
    )
    url = f'{url_prefix}&where={where}'

    response_json = requests.get(url).json()

    if ('error' in response_json):
        raise Exception(response_json['error']['message'])

    results = response_json['features']

    return results
