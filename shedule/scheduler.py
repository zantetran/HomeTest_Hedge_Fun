import os.path
from datetime import timedelta, datetime

from data_ingestion.downloader import downloader
from data_ingestion.index_downloader import get_latest_index, add_table, find_index
import logging.config

import config

logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def daily_download_files():
    """
    This function is responsible for managing the daily download of files. It relies on the `get_latest_index` function
    to determine the last downloaded file's date and index.

    If the `get_latest_index` function returns a valid result (date and index), it checks if a file with the same date
    exists in the 'DATA_DOWNLOADED_DIR' directory. If it does, it logs a message indicating that the file has already
    been downloaded. Otherwise, it calls the 'downloader' function to download the file for the last recorded date and index.

    Note:
    - It assumes that the 'get_latest_index' function returns a tuple with two elements: the last date ('last_day') and the
      last index ('last_index').
    - It assumes that the 'DATA_DOWNLOADED_DIR' directory is properly configured with the path to the downloaded files.
    - The 'downloader' function is expected to be defined elsewhere in the code.

    """
    last_day, last_index = get_latest_index()
    if os.path.exists(f"{config.DATA_DOWNLOADED_DIR}/{last_day}"):
        logging.info(f"File at {last_day} downloaded")
    else:
        add_table(last_index)
        downloader(event_date=last_day, index=last_index)


def recovery(start_date, end_date):
    """
    This function facilitates a recovery process for a specified date range. It attempts to retrieve data for each day
    within the given date range using an index table and a downloader function.

    Args:
    start_date (str): The start date in 'YYYY-MM-DD' format for the recovery process.
    end_date (str): The end date in 'YYYY-MM-DD' format for the recovery process.

    Returns:
    None

    Description:
    - The function logs the start and end dates of the recovery process using the 'logger.info' method.
    - It opens an index table file located at 'index_table/index_table.txt' to retrieve data for each day within the
      specified date range.
    - For each day in the date range (inclusive of both start_date and end_date):
        - It converts the end_date to the 'YYYYMMDD' format using the 'datetime' module.
        - It calls the 'downloader' function with the date in 'YYYYMMDD' format and the corresponding index from the index table.
        - It decrements the end_date by one day to move to the previous day.
    - If an exception occurs during this process, it logs an error message indicating the date that caused the error and
      the exception details.
    """
    logger.info(f"Retrival data from {start_date} to {end_date}")
    with open(f'{config.INDEX_TABLES}/index_table.txt', 'r') as index_table:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        date_download = datetime.strptime(end_date, '%Y-%m-%d')
        index_date = eval(index_table.read())
        while start_date <= date_download:
            date_retrival = date_download.strftime('%Y%m%d')
            if date_retrival in index_date:
                downloader(date_retrival, index_date[date_retrival])
            else:
                if find_index(date_download):
                    downloader(date_retrival, find_index(date_download))
            date_download = date_download - timedelta(days=1)
