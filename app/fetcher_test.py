from datetime import date
from shapely.geometry import Point

from app.fetcher import get_all_features

def test_get_all_features():
    weather_date = date(2020, 8, 11)

    weather_rows = get_all_features(weather_date)

    assert weather_rows[0] == {
      'long': -124.3,
      'lat': 40.3,
      'point': Point(-124.3, 40.3),
      'date': weather_date,
      'month': 8,
      'aspect_east': 0.2257,
      'aspect_north': 0.2767,
      'aspect_south': 0.2066,
      'aspect_west': 0.2461,
      'barren_land': 0.0,
      'elevation': 245,
      'excess_salts': 1,
      'fips': 6023,
      'forest_land': 35.507396697998,
      'grass_land': 8.49260330200195,
      'irrigated_land': 0.0,
      'nutrient': 2,
      'oxygen': 1,
      'partial_cultivated_land': 0.0,
      'rooting': 1,
      'slope_005': 0.0055,
      'slope_005_02': 0.0394,
      'slope_02_05': 0.055,
      'slope_05_10': 0.0597,
      'slope_10_15': 0.0676,
      'slope_15_30': 0.2668,
      'slope_30_45': 0.3008,
      'slope_45': 0.2052,
      'toxicity': 1,
      'urban_land': 0.0,
      'water_land': 56.0,
      'workability': 1,
      'drought_score': 2.75,
      'humidity_2m': 7.82,
      'precipitation': 0.0,
      'pressure': 99.15,
      'temp_2m': 15.17,
      'temp_dew_point_2m': 10.09,
      'temp_range_2m': 5.39,
      'wind_10m': 4.28,
      'prior_fire_0_1_year': 0,
      'prior_fire_1_2_year': 0,
      'prior_fire_2_3_year': 0,
      'prior_fire_3_4_year': 0,
      'prior_fire_4_5_year': 0
    }
