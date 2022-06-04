from os import path

from app.trainer.queries import get_df

split_date = '2018-01-01'
dir = path.dirname(__file__)
file = path.join(dir, '../fixtures/fires_sample.sqlite')


def test_get_no_fires_df_min_date():
    df = get_df(sqlite_file=file)

    assert len(df.columns) == 44
    assert len(df) == 4
    assert df.iloc[0].date == 1246406400
    assert df.iloc[0].has_fire == 0
    assert df.iloc[1].date == 1530403200
    assert df.iloc[1].has_fire == 0
    assert df.iloc[2].date == 1246406400
    assert df.iloc[2].has_fire == 1
    assert df.iloc[3].date == 1530403200
    assert df.iloc[3].has_fire == 1
