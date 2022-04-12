#!/usr/bin/python
import joblib
import lightgbm as lgbm
import logging
from numpy import load

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

gbm = lgbm.LGBMClassifier()

scale_pos_weight = round(28404454/92659)

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

logging.info('Training LGBMClassifier ...')
model.fit(X_train, y_train)

logging.info('Saving model ...')
joblib.dump(model, 'lgbm_model.pickle')
