#!/usr/bin/python
import gc
from joblib import dump, load
import logging
from numpy import save
from os import path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sys import argv

from app.trainer.queries import get_df, one_hot_encode


def main(data_dir: str, model_dir: str, sqlite_file: str):
    logging.basicConfig(
        format='%(levelname)s: %(message)s', level=logging.INFO)

    df = get_df(sqlite_file=sqlite_file)

    y = df.has_fire.to_numpy()
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

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42
    )

    del y
    gc.collect()

    save(f'{data_dir}X_train.npy', X_train)
    save(f'{data_dir}X_test.npy', X_test)
    save(f'{data_dir}y_train.npy', y_train)
    save(f'{data_dir}y_test.npy', y_test)


if __name__ == '__main__':
    main(
        data_dir='./data/', model_dir='./app/models/', sqlite_file='./data/fires.sqlite'
    )
