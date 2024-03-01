import logging.config
import config
import os
import requests
import sys
from tqdm import tqdm

logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def _map_filename(data_type, event_date):
    """
       Map a data type to a corresponding file name based on the provided datatype and date.

        Args:
            event_date: date of event (str)
        Returns:
            The mapped file name, or the original datatype if no mapping is found.
       """
    file_mapping = {
        'WEBPXTICK_DT.zip': f'WEBPXTICK_DT-{event_date}.zip',
        'TC.txt': f'TC_{event_date}.txt'
    }
    return file_mapping.get(data_type, data_type)


def _create_folder(event_date):
    """
    Create a folder for storing downloaded data.

    Parameters:
        event_date (str): The date of the event for which data is being downloaded.

    Returns:
        None
    """
    os.makedirs(f"{config.DATA_DOWNLOADED_DIR}/{event_date}", exist_ok=True)
    os.makedirs(f"{config.INDEX_TABLES}", exist_ok=True)


def _log_chunk_records(bytes_so_far, total_size, filename):
    """
    Log the progress of a download.

    This function logs the download progress, including the number of bytes downloaded,
    the total size of the file, and the download percentage.

    Args:
        bytes_so_far (int): The number of bytes downloaded so far.
        total_size (int): The total size of the file being downloaded.
        filename (str): The name of the file being downloaded.
    Returns:
        None
    """
    percent = round(100 * bytes_so_far / total_size, 2)
    log_message = f"{filename} Downloaded {bytes_so_far} of {total_size} bytes {percent}%"

    if bytes_so_far >= total_size:
        log_message += '\n'
    sys.stdout.write('\r')
    sys.stdout.write(log_message)


def downloader(event_date, index, chunk_size=10000):
    """
    Download data for a given event date.

    This function downloads data for a specific event date from a URL
    and stores it in a folder.

    Parameters:
        event_date (str): The date of the event for which data is being downloaded.
        index (int): The index of the data.
        chunk_size (int, optional): The size of download chunks (default is 10000).

    Returns:
        None
    """
    if os.path.exists(f"{config.DATA_DOWNLOADED_DIR}/{event_date}"):
        logging.info(f"File at {event_date} downloaded")
    else:
        logging.info(f'Downloading at {event_date}')
        _create_folder(event_date=event_date)

        for data_type in config.DATA_TYPES:
            url = 'https://links.sgx.com/1.0.0/derivatives-historical/' + str(index) + '/' + data_type
            try:
                response = requests.get(url, stream=True)
                content_size = int(response.headers['content-length'])
                bytes_so_far = 0
                file_name = _map_filename(data_type=data_type, event_date=event_date)
                with open(f"{config.DATA_DOWNLOADED_DIR}/{event_date}/{file_name}", "wb") as file:
                    with tqdm(total=content_size // chunk_size, unit=' chunks') as pbar:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                file.write(chunk)
                                bytes_so_far += len(chunk)
                                _log_chunk_records(bytes_so_far, content_size, file_name)
                                pbar.update(1)
                                pbar.set_description(f"Downloaded with chunk_size = {chunk_size}:"
                                                     f" {bytes_so_far}/{content_size} bytes")
                                pbar.set_postfix({"File Name": file_name})

            except Exception as e:
                logging.warning(f'{event_date} download failed ' + str(e))
                with open(f'{config.INDEX_TABLES}/recovery.txt', 'a') as file:
                    file.write(str(event_date) + ',')

