#!/usr/bin/python
import gc
import joblib
import logging
from numpy import save
import pandas as pd
from sklearn.preprocessing import StandardScaler
import sys

from app.trainer.queries import get_fires_df, get_no_fires_df


def main(partition: str, data_dir: str, model_dir: str, sqlite_file: str):
    logging.basicConfig(
        format='%(levelname)s: %(message)s', level=logging.INFO)

    if partition == 'train':
        min_date = None
        max_date = '2018-01-01'
    else:
        min_date = '2018-01-01'
        max_date = None

    no_fires_df = get_no_fires_df(min_date, max_date, sqlite_file=sqlite_file)
    logging.info(f'Found {len(no_fires_df)} no fire {partition} data points')

    fires_df = get_fires_df(min_date, max_date, sqlite_file=sqlite_file)
    logging.info(f'Found {len(fires_df)} fire {partition} data points')

    df = pd.concat([no_fires_df, fires_df], axis=0).sample(frac=1)

    del no_fires_df, fires_df
    gc.collect()

    y = df.has_fire.to_numpy()
    save(f'{data_dir}y_{partition}.npy', y)

    del y
    gc.collect()

    df_encoded = pd.get_dummies(
        df.drop(['has_fire'], axis=1), columns=['month', 'nutrient', 'rooting', 'oxygen', 'excess_salts', 'toxicity', 'workability']
    )

    del df
    gc.collect()

    if partition == 'train':
        scaler = StandardScaler()
        scaler.fit(df_encoded)
        joblib.dump(scaler, f'{model_dir}scaler.pickle')
    else:
        scaler = joblib.load(f'{model_dir}scaler.pickle')

    X = scaler.transform(df_encoded)

    del df_encoded
    gc.collect()

    save(f'{data_dir}/X_{partition}.npy', X)


if __name__ == '__main__':
    partition = 'train' if len(
        sys.argv) > 1 and sys.argv[1] == 'train' else 'test'
    main(
        partition, data_dir='./data/', model_dir='./app/models/',
        sqlite_file='./data/fires.sqlite'
    )
