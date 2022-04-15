#!/usr/bin/python
import gc
import logging
from numpy import save
import pandas as pd
from sklearn.preprocessing import StandardScaler
import sys

import queries


def main():
    logging.basicConfig(
        format='%(levelname)s: %(message)s', level=logging.INFO)

    partition = 'train' if len(
        sys.argv) > 1 and sys.argv[1] == 'train' else 'test'

    if partition == 'train':
        min_date = None
        max_date = '2018-01-01'
    else:
        min_date = '2018-01-01'
        max_date = None

    no_fires_df = queries.get_no_fires_df(min_date, max_date)
    logging.info(f'Found {len(no_fires_df)} no fire {partition} data points')

    fires_df = queries.get_fires_df(min_date, max_date)
    logging.info(f'Found {len(fires_df)} fire {partition} data points')

    df = pd.concat([no_fires_df, fires_df], axis=0).sample(frac=1)

    del no_fires_df, fires_df
    gc.collect()

    y = df.has_fire.to_numpy()
    save(f'./data/y_{partition}.npy', y)

    del y
    gc.collect()

    df_encoded = pd.get_dummies(
        df.drop(['has_fire'], axis=1), columns=['month'])

    del df
    gc.collect()

    scaler = StandardScaler()
    scaler.fit(df_encoded)
    X = scaler.transform(df_encoded)

    del df_encoded
    gc.collect()

    save(f'./data/X_{partition}.npy', X)


if __name__ == '__main__':
    main()
