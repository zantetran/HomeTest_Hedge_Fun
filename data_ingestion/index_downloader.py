import os.path
import urllib.request
import logging.config
from datetime import datetime, timedelta

import config

logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def get_date(index):
    """
    Get the date from the file downloaded from a specific URL.

    This function fetches the date information from a file's metadata
    retrieved from a URL.

    Parameters:
        index (int): The index used to construct the URL.

    Returns:
        str: The date in the format 'YYYYMMDD'.
    """
    url = f'https://links.sgx.com/1.0.0/derivatives-historical/{index}/TC.txt'

    try:
        with urllib.request.urlopen(url, timeout=10) as request:
            filename = request.headers.get('Content-Disposition', '').split('=')[1]
            try:
                date = filename.split('_')[1].split('.')[0]
                logging.info(f'Date {date} coordinates index {index}')
            except:
                logging.info(f'Index {index} is empty')
                date = '0'
    except Exception as err:
        logging.warning(f'Index {index} is failure get date, {err}')
        date = 'NA'
        with open(f'{config.INDEX_TABLES}/index_error.txt', 'r') as f:
            if str(index) not in f.read().split():
                with open(f'{config.INDEX_TABLES}/index_error.txt', 'a') as file:
                    file.write(str(index) + ' ')

    return date


def add_table(index):
    """
    Add an index to the index table.

    This function adds an index to the index table and logs the addition.

    Parameters:
        index (int): The index to be added.

    Returns:
        None
    """
    path_index_table = f"{config.INDEX_TABLES}/index_table.txt"
    if os.path.exists(path_index_table):
        with open(path_index_table, 'r') as f:
            index_table = eval(f.read())

        index_table[get_date(index)] = index

        with open(path_index_table, 'w') as f:
            f.write(str(index_table))
    else:
        with open(path_index_table, 'w') as f:
            f.write(str({'20231006': 5523}))

    logging.info(f'Index {index} is added')


def get_latest_index():
    """
    This function is used to retrieve and update an index from the 'latest_index.txt' file in the 'index_table' directory.
    The index consists of a date and an integer value.

    Returns:
        tuple: A tuple containing two elements. The first element is the latest date ('latest_date'),
        and the second element is the latest index ('latest_index').

    """
    latest_index = 5523
    latest_date = '20231006'
    os.makedirs(config.INDEX_TABLES, exist_ok=True)
    path_latest_index = f"{config.INDEX_TABLES}/latest_index.txt"
    if os.path.exists(path_latest_index):
        with open(path_latest_index, 'r') as file:
            content = file.read().strip()
            if content:
                parts = content.split(' ')
                if len(parts) == 2:
                    latest_date, latest_index = parts[0], int(parts[1])
    else:
        with open(path_latest_index, 'a') as file:
            file.write(f"{latest_date} {latest_index}")
        return latest_date, latest_index

    while True:
        if get_date(latest_index + 1) in ['0', 'NA']:
            break
        latest_date = get_date(latest_index + 1)
        latest_index += 1

    with open(path_latest_index, 'w') as file:
        file.write(f"{latest_date} {latest_index}")

    return latest_date, latest_index


def find_index(date):
    # print(date)
    latest_index = 5523
    root_date = datetime(2023, 10, 6)
    count_index = (root_date - date).days
    for d in range(1, abs(count_index)+1):
        if get_date(latest_index + d) == date.strftime('%Y%m%d'):
            return latest_index + d
        if get_date(latest_index - d) == date.strftime('%Y%m%d'):
            return latest_index - d

    return None

