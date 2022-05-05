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


def get_no_fires_df(min_date, max_date, sqlite_file):
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
  where
    {'1 = 1' if min_date is None else f"weather_geo.date >= '{min_date}'"}
    and
    {'1 = 1' if max_date is None else f"weather_geo.date < '{max_date}'"}
  """, conn, dtype=dtype)

    conn.close()

    return no_fires_df


def get_fires_df(min_date, max_date, sqlite_file):
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
  where
    {'1 = 1' if min_date is None else f"weather_geo.date >= '{min_date}'"}
    and
    {'1 = 1' if max_date is None else f"weather_geo.date < '{max_date}'"}
  """, conn, dtype=dtype)

    conn.close()

    return fires_df
