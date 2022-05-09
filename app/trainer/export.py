#!/usr/bin/python
import gc
from joblib import dump, load
import logging
from numpy import save
from os import path
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sys import argv

from app.trainer.queries import get_fires_df, get_no_fires_df, one_hot_encode


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

    df_encoded = one_hot_encode(df.drop(['has_fire'], axis=1))

    del df
    gc.collect()

    if path.exists(f'{model_dir}scaler.pickle'):
        scaler = load(f'{model_dir}scaler.pickle')
    else:
        scaler = StandardScaler()
        scaler.fit(df_encoded)
        dump(scaler, f'{model_dir}scaler.pickle')

    X = scaler.transform(df_encoded)

    del df_encoded
    gc.collect()

    save(f'{data_dir}/X_{partition}.npy', X)


if __name__ == '__main__':
    partition = 'train' if len(argv) > 1 and argv[1] == 'train' else 'test'
    main(
        partition, data_dir='./data/', model_dir='./app/models/',
        sqlite_file='./data/fires.sqlite'
    )
