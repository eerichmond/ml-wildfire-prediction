#!/usr/bin/python
import joblib
import lightgbm as lgbm
import logging
from numpy import load
import xgboost
import sys


def main(classifier: str, data_dir: str, model_dir: str):
    logging.basicConfig(
        format='%(levelname)s: %(message)s', level=logging.INFO)

    scale_pos_weight = round(28404454/92659)

    if classifier == 'xgb':
        model = xgboost.XGBClassifier(
            seed=42,
            use_label_encoder=False,
            objective='binary:logistic',
            n_estimators=500,
            max_depth=9,
            learning_rate=0.1,
            gamma=0.2,
            eval_metric='error',
            colsample_bytree=0.2,
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
    y_train = load(f'{data_dir}y_train.npy')

    logging.info('Loading X_train ...')
    X_train = load(f'{data_dir}X_train.npy')

    logging.info(f'Training {classifier} ...')
    model.fit(X_train, y_train)

    logging.info('Saving model ...')
    joblib.dump(model, f'{model_dir}{classifier}_model.pickle')


if __name__ == '__main__':
    classifier = 'lgbm' if len(
        sys.argv) > 1 and sys.argv[1] == 'lgbm' else 'xgb'
    main(classifier, data_dir='./data/', model_dir='./app/models/')
