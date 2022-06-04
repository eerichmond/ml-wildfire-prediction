import logging
import numpy as np
import pandas as pd
import sqlite3

dtype = {
    'long': np.float32,
    'lat': np.float32,
    'month': np.int8,
    'date': np.int64,
    'precipitation': np.float32,
    'pressure': np.float32,
    'humidity_2m': np.float32,
    'temp_2m': np.float32,
    'temp_dew_point_2m': np.float32,
    'temp_range_2m': np.float32,
    'wind_10m': np.float32,
    'drought_score': np.float32,
    'elevation': np.int32,
    'slope_005': np.float32,
    'slope_005_02': np.float32,
    'slope_02_05': np.float32,
    'slope_05_10': np.float32,
    'slope_10_15': np.float32,
    'slope_15_30': np.float32,
    'slope_30_45': np.float32,
    'slope_45': np.float32,
    'aspect_north': np.float32,
    'aspect_east': np.float32,
    'aspect_south': np.float32,
    'aspect_west': np.float32,
    'water_land': np.float32,
    'barren_land': np.float32,
    'urban_land': np.float32,
    'grass_land': np.float32,
    'forest_land': np.float32,
    'partial_cultivated_land': np.float32,
    'irrigated_land': np.float32,
    'nutrient': np.int8,
    'rooting': np.int8,
    'oxygen': np.int8,
    'excess_salts': np.int8,
    'toxicity': np.int8,
    'workability': np.int8,
    'prior_fire_0_1_year': np.int8,
    'prior_fire_1_2_year': np.int8,
    'prior_fire_2_3_year': np.int8,
    'prior_fire_3_4_year': np.int8,
    'prior_fire_4_5_year': np.int8,
    'has_fire': np.int8
}


def get_no_fires_df(sqlite_file):
    conn = sqlite3.connect(sqlite_file)

    no_fires_df = pd.read_sql_query(f"""
  select
    weather_geo.long,
    weather_geo.lat,
    weather_geo.month,
    strftime('%s', weather_geo.date) as date,
    weather_geo.precipitation,
    weather_geo.pressure,
    weather_geo.humidity_2m,
    weather_geo.temp_2m,
    weather_geo.temp_dew_point_2m,
    weather_geo.temp_range_2m,
    weather_geo.wind_10m,
    weather_geo.drought_score,
    soil_geo.elevation,
    soil_geo.slope_005,
    soil_geo.slope_005_02,
    soil_geo.slope_02_05,
    soil_geo.slope_05_10,
    soil_geo.slope_10_15,
    soil_geo.slope_15_30,
    soil_geo.slope_30_45,
    soil_geo.slope_45,
    soil_geo.aspect_north,
    soil_geo.aspect_east,
    soil_geo.aspect_south,
    soil_geo.aspect_west,
    soil_geo.water_land,
    soil_geo.barren_land,
    soil_geo.urban_land,
    soil_geo.grass_land,
    soil_geo.forest_land,
    soil_geo.partial_cultivated_land,
    soil_geo.irrigated_land,
    soil_geo.nutrient,
    soil_geo.rooting,
    soil_geo.oxygen,
    soil_geo.excess_salts,
    soil_geo.toxicity,
    soil_geo.workability,
    prior_fire_0_1_year,
    prior_fire_1_2_year,
    prior_fire_2_3_year,
    prior_fire_3_4_year,
    prior_fire_4_5_year,
    0 as has_fire
  from weather_geo_no_fire as weather_geo
  inner join soil_geo
    on soil_geo.long = weather_geo.long
    and soil_geo.lat = weather_geo.lat
  """, conn, dtype=dtype)

    conn.close()

    logging.info(f'Found {len(no_fires_df)} no fire data points')

    return no_fires_df


def get_fires_df(sqlite_file):
    conn = sqlite3.connect(sqlite_file)

    fires_df = pd.read_sql_query(f"""
  select
    weather_geo.long,
    weather_geo.lat,
    weather_geo.month,
    strftime('%s', weather_geo.date) as date,
    weather_geo.precipitation,
    weather_geo.pressure,
    weather_geo.humidity_2m,
    weather_geo.temp_2m,
    weather_geo.temp_dew_point_2m,
    weather_geo.temp_range_2m,
    weather_geo.wind_10m,
    weather_geo.drought_score,
    soil_geo.elevation,
    soil_geo.slope_005,
    soil_geo.slope_005_02,
    soil_geo.slope_02_05,
    soil_geo.slope_05_10,
    soil_geo.slope_10_15,
    soil_geo.slope_15_30,
    soil_geo.slope_30_45,
    soil_geo.slope_45,
    soil_geo.aspect_north,
    soil_geo.aspect_east,
    soil_geo.aspect_south,
    soil_geo.aspect_west,
    soil_geo.water_land,
    soil_geo.barren_land,
    soil_geo.urban_land,
    soil_geo.grass_land,
    soil_geo.forest_land,
    soil_geo.partial_cultivated_land,
    soil_geo.irrigated_land,
    soil_geo.nutrient,
    soil_geo.rooting,
    soil_geo.oxygen,
    soil_geo.excess_salts,
    soil_geo.toxicity,
    soil_geo.workability,
    fires_rollup.prior_fire_0_1_year,
    fires_rollup.prior_fire_1_2_year,
    fires_rollup.prior_fire_2_3_year,
    fires_rollup.prior_fire_3_4_year,
    fires_rollup.prior_fire_4_5_year,
    1 as has_fire
  from weather_geo
  inner join soil_geo
    on soil_geo.long = weather_geo.long
    and soil_geo.lat = weather_geo.lat
  inner join fires_rollup
    on fires_rollup.date = weather_geo.date
    and fires_rollup.long = weather_geo.long
    and fires_rollup.lat = weather_geo.lat
    and fires_rollup.cause in ('Other causes', 'Natural', 'Power', 'Recreation')
  """, conn, dtype=dtype)

    conn.close()

    logging.info(f'Found {len(fires_df)} fire data points')

    return fires_df


def get_df(sqlite_file):
    return pd.concat([get_no_fires_df(sqlite_file), get_fires_df(sqlite_file)], axis=0)


def one_hot_encode(orig_df):
    df = orig_df.copy()

    for i in range(12):
        df[f'month_{i+1}'] = (df['month'] == i+1).astype(int)

    for i in [0, 1, 2, 3, 4, 7]:
        df[f'nutrient_{i}'] = (df['nutrient'] == i).astype(int)

    for i in [0, 1, 2, 3, 4, 5, 7]:
        df[f'rooting_{i}'] = (df['rooting'] == i).astype(int)

    for i in [0, 1, 2, 3, 7]:
        df[f'oxygen_{i}'] = (df['oxygen'] == i).astype(int)

    for i in [0, 1, 2, 3, 4, 5, 7]:
        df[f'excess_salts_{i}'] = (df['excess_salts'] == i).astype(int)

    for i in [0, 1, 2, 3, 7]:
        df[f'toxicity_{i}'] = (df['toxicity'] == i).astype(int)

    for i in [0, 1, 2, 3, 4, 5, 7]:
        df[f'workability_{i}'] = (df['workability'] == i).astype(int)

    return df.drop(
        ['month', 'nutrient', 'rooting', 'oxygen',
         'excess_salts', 'toxicity', 'workability'],
        axis=1
    )
