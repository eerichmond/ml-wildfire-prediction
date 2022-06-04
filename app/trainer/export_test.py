from os import mkdir, path, rmdir
import pytest
from shutil import rmtree

from app.trainer.export import main as export

data_dir = path.join(path.dirname(__file__), '../fixtures/')
tmp_dir = path.join(data_dir, 'tmp/')
sqlite = path.join(data_dir, 'fires_sample.sqlite')


@pytest.fixture(autouse=True)
def run_around_tests():
    mkdir(tmp_dir)
    yield
    rmtree(tmp_dir)


def test_export_test_npy():
    export(data_dir=tmp_dir, model_dir=tmp_dir, sqlite_file=sqlite)

    assert path.exists(path.join(tmp_dir, 'scaler.pickle'))
    assert path.exists(path.join(tmp_dir, 'y_test.npy'))
    assert path.exists(path.join(tmp_dir, 'X_test.npy'))


def test_export_train_npy():
    export(data_dir=tmp_dir, model_dir=tmp_dir, sqlite_file=sqlite)

    assert path.exists(path.join(tmp_dir, 'scaler.pickle'))
    assert path.exists(path.join(tmp_dir, 'y_train.npy'))
    assert path.exists(path.join(tmp_dir, 'X_train.npy'))
