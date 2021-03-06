from os import mkdir, path
import pytest
from shutil import copyfile, rmtree

from app.trainer.export import main as export
from app.trainer.train import main as train

split_date = '2018-01-01'
data_dir = path.join(path.dirname(__file__), '../fixtures/')
tmp_dir = path.join(data_dir, 'tmp/')
sqlite = path.join(data_dir, 'fires_sample.sqlite')
scaler_path = path.join(path.dirname(__file__), '../models/scaler.pickle')


@pytest.fixture(autouse=True)
def run_around_tests():
    mkdir(tmp_dir)
    copyfile(scaler_path, path.join(tmp_dir, 'scaler.pickle'))
    yield
    rmtree(tmp_dir)


def test_train_xgb():
    export(data_dir=tmp_dir, model_dir=tmp_dir, sqlite_file=sqlite)
    export(data_dir=tmp_dir, model_dir=tmp_dir, sqlite_file=sqlite)
    train('xgb', data_dir=tmp_dir, model_dir=tmp_dir)

    assert path.exists(path.join(tmp_dir, 'xgb_model.pickle'))
