from datetime import datetime
from google.cloud import storage
from json import dumps
import re

bucket_name = 'eer-wildfires'

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

def get_file(date: datetime):
    file = f'fires/{date.strftime("%Y-%m-%d")}.json'
    blob = bucket.blob(file)
    
    return blob.download_as_text()

def delete_file(date: datetime):
    file = f'fires/{date.strftime("%Y-%m-%d")}.json'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file)

    if (blob.exists()):
        blob.delete()

def upload_file(data: map):
    date_string = data["date"]
    matched = re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date_string)

    if (not matched):
        raise ValueError(f'data["date"], "{date_string}", must be formated as yyyy-mm-dd')

    file = f'fires/{date_string}.json'

    blob = bucket.blob(file)

    blob.upload_from_string(dumps(data))
