# Predicting United States Wildfires from Drought and Soil Conditions

One topic I am passionate about is the environment, especially the impact that climate change has on our natural world and standard of living. To get an idea of what kind of climate related datasets were out there, I scrubbed [Kaggle.com](Kaggle.com) for high quality datasets that involved the environment. A couple datasets caught my attention because they were so close to home. The two datasets were [United States wildfires over a 24 year period](https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires) and [United States droughts and soil conditions over a 20 year period](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data). I live in the central valley of California (US) where every year the fires in the hills on either side of the valley become worse and worse, creating horrible air quality and destroying the forests. I am interested in predicting when and where wildfires will occur next. Identifying these locations could lead to better fire preparation and population planning.

### [Capstone Project Proposal Google Doc](https://docs.google.com/document/d/1jK7I5DkK1wicWTT9E59OClmK7noie6oWeQ8o-KBUqVo/edit#)

## Datasets

### [Kaggle: Predict Droughts using Weather & Soil Data](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data)

- 3 zipped csv files with 23,841,471 records
- License CC0: Public Domain
- [Drought notebooks](https://github.com/MiniXC/droughted_scripts)

### [Kaggle: 1.88 Million US Wildfires](https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires)

- Sqlite zip with 1,880,456 records
- License CC0: Public Domain
- Newer version of the data (up to 2018) at [US Forest Service](https://www.fs.usda.gov/rds/archive/Catalog/RDS-2013-0009.5)

### How to Train

- Run through `experiments/1_data_wrangling.ipynb` // TODO: need to automate this part
- `python trainer/export.py` to generate the `X_train.npy, X_test.npy, y_train.npy, x_test.npy` numpy array binaries. This is a separate step
  because it takes 3+ hours to turn the ~27 million non-fire data points into a 13GB `X_train.npy`
- `python trainer/train.py` to generate the `lgbm_model.pickle`
