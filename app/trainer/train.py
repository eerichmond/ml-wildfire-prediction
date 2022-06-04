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
            learning_rate=0.5,
            gamma=0.6,
            eval_metric='error',
            colsample_bytree=0.4,
            scale_pos_weight=scale_pos_weight
        )
    else:
        model = lgbm.LGBMClassifier(
            objective='binary',
            num_leaves=20,
            min_gain_to_split=7,
            min_data_in_leaf=1000,
            metric='binary_logloss',
            max_depth=3,
            max_bin=300,
            lambda_l2=50,
            lambda_l1=10,
            learning_rate=0.2,
            feature_fraction=0.5,
            bagging_freq=1,
            bagging_fraction=0.4,
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
