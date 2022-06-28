from datetime import date

from app.fetcher import get_weather_all

def test_get_weather_all():
    weather_date = date(2020, 8, 11)

    weather_rows = get_weather_all(weather_date)

    assert weather_rows[0] == {
      'date': weather_date,
      'humidity_2m': 10.75,
      'lat': 32.75,
      'long': -124.25,
      'month': 8,
      'precipitation': 0.25,
      'pressure': 101.49,
      'temp_2m': 18.35,
      'temp_dew_point_2m': 15.35,
      'temp_range_2m': 0.61,
      'wind_10m': 4.41
    }
