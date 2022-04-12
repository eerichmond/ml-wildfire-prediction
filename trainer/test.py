#!/usr/bin/python
import gc
import logging
from numpy import load
from sklearn.metrics import classification_report
from sklearn.externals import joblib

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

model = joblib.load('lgbm_model.pkl')

X_test = load('./data/X_test.npy')
y_pred = model.predict(X_test)

del X_test, model
gc.collect()

y_test = load('./data/y_test.npy')

logging.info(f'LightGBM Classification Report')
print(classification_report(y_test, y_pred))
