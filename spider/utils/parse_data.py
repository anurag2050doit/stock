import logging
from zipfile import ZipFile
import csv
from utils import constant
from os.path import join
import redis
import json


def extract_zip_file(file_name):
    """
    Extract zip and return list of csv files
    :param file_name: Name of zip file
    :return:
    """
    with ZipFile('%s/%s' % (constant.ZIP_FILE_DIR, file_name)) as zip_file:
        list_of_zip_file = [file.filename for file in zip_file.filelist]
        zip_file.extractall('%s' % constant.CSV_FILE_DIR)
        logging.info('All files extracted successful')
        return list_of_zip_file


def parse_csv_file(csv_files):
    """
    Get list of csv files and load into redis
    :param csv_files: csv files
    :return:
    """
    data = []
    r = redis.StrictRedis(host=constant.REDIS_HOST, port=constant.REDIS_PORT, db=constant.REDIS_DB)
    for file in csv_files:
        path = join(constant.CSV_FILE_DIR, file)
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_row = {
                    'code': row.get('SC_CODE'),
                    'name': row.get('SC_NAME'),
                    'open': row.get('OPEN'),
                    'high': row.get('HIGH'),
                    'low': row.get('LOW'),
                    'close': row.get('CLOSE')
                }
                r.set(row.get('SC_NAME', '').strip().upper(), json.dumps(data_row))
                data.append(data_row)
    r.set(constant.REDIS_DB_KEY, json.dumps(data))
    logging.info('File loaded successfully to redis DB')
