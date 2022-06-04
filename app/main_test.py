from datetime import date

from app.main import features_api, calculate_probablity
from app.fixtures.samples import features_2020_08_11


def test_features_api():
    fire_date = date(2020, 8, 11)
    long = -120.6044
    lat = 39.6120

    features = features_api(fire_date, long, lat)
    assert features == features_2020_08_11


def test_calculate_probablity():
    proba = calculate_probablity(features_2020_08_11)

    assert proba > 5
