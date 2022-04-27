from os import path

from app.trainer.queries import get_no_fires_df, get_fires_df

split_date = '2018-01-01'
dir = path.dirname(__file__)
file = path.join(dir, '../fixtures/fires_sample.sqlite')


def test_get_no_fires_df_min_date():
    df = get_no_fires_df(min_date=split_date, max_date=None, sqlite_file=file)

    assert len(df.columns) == 44
    assert len(df) == 1
    assert df.iloc[0].date == 1530403200
    assert df.iloc[0].has_fire == 0


def test_get_fires_df_min_date():
    df = get_fires_df(min_date=split_date, max_date=None, sqlite_file=file)

    assert len(df.columns) == 44
    assert len(df) == 1
    assert df.iloc[0].date == 1530403200
    assert df.iloc[0].has_fire == 1


def test_get_no_fires_df_max_date():
    df = get_no_fires_df(min_date=None, max_date=split_date, sqlite_file=file)

    assert len(df) == 1
    assert df.iloc[0].date == 1246406400
    assert df.iloc[0].has_fire == 0


def test_get_fires_df_max_date():
    df = get_fires_df(min_date=None, max_date=split_date, sqlite_file=file)

    assert len(df) == 1
    assert df.iloc[0].date == 1246406400
    assert df.iloc[0].has_fire == 1
