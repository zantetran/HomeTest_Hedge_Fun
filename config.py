LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(filename)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file_handler': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',  # Sử dụng FileHandler để lưu log vào file
            'filename': 'download.log',  # Tên tệp log
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'gensim': {
            'handlers': ['default'],
            'level': 'ERROR',
            'propagate': False
        },
        'apscheduler': {
            'handlers': ['default'],
            'level': 'ERROR',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default', 'file_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
DATA_DOWNLOADED_DIR = 'files'
DATA_TYPES = ['TC.txt', 'TickData_structure.dat', 'TC_structure.dat', 'WEBPXTICK_DT.zip']
INDEX_TABLES = 'index_tables'
