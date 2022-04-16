from datetime import date, datetime, timedelta
from fastapi import FastAPI, Request
from joblib import load
from json import dumps
import numpy as np
from os import path
import pandas as pd
from starlette.templating import Jinja2Templates
import warnings

from fetcher import get_drought_score, get_prior_fire_years, get_soil, get_weather

warnings.simplefilter(action='ignore', category=FutureWarning)

app = FastAPI()

views = Jinja2Templates(directory="views")

model_file = path.join(path.dirname(__file__), './models/xgb_model.pickle')
xgb_model = load(model_file)

scaler_file = path.join(path.dirname(__file__), './models/scaler.pickle')
scaler = load(scaler_file)


@app.get("/")
def home(*, request: Request, date: date = datetime.now() - timedelta(2), long: float = None, lat: float = None):
    features = None
    proba = 0.0

    if (date and long and lat):
        features = features_api(date, long, lat)
        proba = calculate_probablity(features)
        feature_json = dumps(
            {**features, 'date': features['date'].strftime('%Y-%m-%d')},
            indent=4
        )

    return views.TemplateResponse(
        "home.html",
        {
            "date": date, "long": long, "lat": lat, "features": feature_json, "proba": proba, "request": request
        }
    )


@app.get("/features")
def features_api(date: date, long: float, lat: float):
    weather = get_weather(date, long, lat)
    soil = get_soil(long, lat)
    prior_fire_years = get_prior_fire_years(date, long, lat)
    drought_score = get_drought_score(date, soil['fips'])
    del soil['fips']

    return {**weather, 'drought_score': drought_score, **soil, **prior_fire_years}


def calculate_probablity(features: dict):
    df = pd.DataFrame(
        {**features, 'date': int(features['date'].strftime('%s'))}, index=[0]
    )

    for month in range(12):
        df[f'month_{month+1}'] = int(df['month'] == month+1)

    df = df.drop(['month'], axis=1)

    values = scaler.transform(df)

    _, yes_fire = xgb_model.predict_proba(values)[0]

    return round(yes_fire * 100, 2)
