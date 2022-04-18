from datetime import date, datetime, timedelta
from os import path
from pandas import read_csv
import requests
from shapely.geometry import Point
import urllib.parse

soil_file = path.join(path.dirname(__file__), './models/soil.csv')
soil_df = read_csv(soil_file).drop(
    ['aspect_unknown', 'cultivated_land', 'nutrient_retention'], axis=1
)
soil_df = soil_df[(soil_df.fips >= 6000) & (soil_df.fips < 7000)]
soil_pt_1 = Point(soil_df.iloc[0].longitude, soil_df.iloc[0].latitude)


def get_weather(date: date, long: float, lat: float):
    params = ['QV2M', 'T2M_RANGE', 'WS10M', 'T2M', 'PS', 'T2MDEW', 'PRECTOT']

    start = date.strftime('%Y%m%d')
    end = start

    raw_json = requests.get(
        'https://power.larc.nasa.gov/api/temporal/daily/point',
        {
            'parameters': ','.join(params),
            'community': 'SB',
            'longitude': long,
            'latitude': lat,
            'start': start,
            'end': end,
            'format': 'JSON',
        }
    ).json()['properties']['parameter']

    return {
        'long': round(long, 1),
        'lat': round(lat, 1),
        'month': date.month,
        'date': date,
        'precipitation': raw_json['PRECTOTCORR'][start],
        'pressure': raw_json['PS'][start],
        'humidity_2m': raw_json['QV2M'][start],
        'temp_2m': raw_json['T2M'][start],
        'temp_dew_point_2m': raw_json['T2MDEW'][start],
        'temp_range_2m': raw_json['T2M_RANGE'][start],
        'wind_10m': raw_json['WS10M'][start]
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

    return float(item['D0'])/100 + float(item['D1'])/100 + float(
        item['D2'])/100 + float(item['D3'])/100 + float(item['D4'])/100


def get_soil(long: int, lat: int):
    pt = Point(long, lat)
    nearest_soil_dist = soil_pt_1.distance(pt)
    soil = {}

    for _, soil_row in soil_df.iterrows():
        soil_pt = Point(soil_row.longitude, soil_row.latitude)

        if soil_pt.distance(pt) < nearest_soil_dist:
            nearest_soil_dist = soil_pt.distance(pt)
            soil = soil_row.to_dict()

    soil['fips'] = int(soil['fips'])
    del soil['longitude']
    del soil['latitude']

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
