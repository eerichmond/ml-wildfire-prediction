from datetime import datetime
from json import dumps
import pytest

from app.storage import delete_file, get_file, upload_file

date = datetime.now()

@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    delete_file(date)

def test_upload_and_get():
  data = { 'date': date.strftime('%Y-%m-%d') }
  upload_file(data)

  download = get_file(date)

  assert download == dumps(data)
