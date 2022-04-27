# Predict California Wildfires from Weather and Soil Conditions

[![Build](https://github.com/eerichmond/ml-wildfire-prediction/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/eerichmond/ml-wildfire-prediction/actions/workflows/build.yml)

### Demo

- Google Cloud Run at https://ml-wildfire-v2m4frgpla-uw.a.run.app/

### How to Train

- [fires.sqlite on Google Cloud Storage](https://storage.googleapis.com/eer-wildfires/fires.sqlite)
- Run through `experiments/1_data_wrangling.ipynb` // TODO: need to automate this part
- `python trainer/export.py test` to generate `X_test.npy, x_test.npy` and
  `python trainer/export.py train` to generate `X_train.npy, y_train.npy, src/app/models/scalar.pickle` numpy
  array binaries. These are a separate steps because it takes 3+ hours to turn the ~27 million
  non-fire data points into a 13GB `X_train.npy`
- `python trainer/train.py xgb` to generate the `src/app/models/xgb_model.pickle`

### Start App

- `pip install -r requirements.txt`
- `yarn install`
- `yarn build`
- `uvicorn app.main:app --reload`

### Run Tests

- `ptw --runner "pytest --testmon"`

One topic I am passionate about is the environment, especially the impact that climate change has on our natural world and standard of living. To get an idea of what kind of climate related datasets were out there, I scrubbed [Kaggle.com](Kaggle.com) for high quality datasets that involved the environment. A couple datasets caught my attention because they were so close to home. The two datasets were [United States wildfires over a 24 year period](https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires) and [United States droughts and soil conditions over a 20 year period](https://www.kaggle.com/datasets/cdminix/us-drought-meteorological-data). I live in the central valley of California (US) where every year the fires in the hills on either side of the valley become worse and worse, creating horrible air quality and destroying the forests. I am interested in predicting when and where wildfires will occur next. Identifying these locations could lead to better fire preparation and population planning.

### Deploying to Google Cloud Run

- [Google Cloud Dashboard](https://console.cloud.google.com/home/dashboard)
- Create `ml-wildfire` Google Cloud Run service and Google Artifact Registry
  - `sh ./gcp_setup.sh`
- GitHub Actions `build.yml` will
  - Install and test the Python app
  - Build Docker image and store in both GitHub Container Registry and Google Artifact Registry (Docker)
  - Deploy the `:latest` Docker image to Google Cloud Run
- [Deployment Diagrams](https://docs.google.com/document/d/1XApYnanNj7glBL0Cuacg09lvcSD3Uhkhly44ez15XmU/edit?usp=sharing)

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
