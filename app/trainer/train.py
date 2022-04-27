#!/usr/bin/python
import joblib
import lightgbm as lgbm
import logging
from numpy import load
import xgboost
import sys


def main():
    logging.basicConfig(
        format='%(levelname)s: %(message)s', level=logging.INFO)

    classifier = 'xgb' if len(
        sys.argv) > 1 and sys.argv[1] == 'xgb' else 'lgbm'

    scale_pos_weight = round(28404454/92659)

    if classifier == 'xgb':
        model = xgboost.XGBClassifier(
            seed=42,
            use_label_encoder=False,
            objective='binary:logistic',
            n_estimators=200,
            max_depth=9,
            learning_rate=0.2,
            gamma=0.2,
            eval_metric='logloss',
            colsample_bytree=0.4,
            scale_pos_weight=scale_pos_weight
        )
    else:
        model = lgbm.LGBMClassifier(
            objective='binary',
            num_leaves=100,
            min_data_in_leaf=200,
            metric='binary_logloss',
            max_depth=7,
            max_bin=300,
            learning_rate=0.2,
            feature_fraction=0.5,
            bagging_freq=5,
            bagging_fraction=0.7,
            scale_pos_weight=scale_pos_weight
        )

    logging.info('Loading y_train ...')
    y_train = load('./data/y_train.npy')

    logging.info('Loading X_train ...')
    X_train = load('./data/X_train.npy')

    logging.info(f'Training {classifier} ...')
    model.fit(X_train, y_train)

    logging.info('Saving model ...')
    joblib.dump(model, f'./app/models/{classifier}_model.pickle')


if __name__ == '__main__':
    main()
