from custom_logger import CustomLogger

logger_class = CustomLogger

logconfig_dict = {
    "version": 1,
    "handlers": {
        "access_200_file": {
            "class": "logging.FileHandler",
            "filename": "access_200.log",
            "formatter": "generic",
        },
        "access_other_file": {
            "class": "logging.FileHandler",
            "filename": "access_other.log",
            "formatter": "generic",
        },
        "access_extra_file": {
            "class": "logging.FileHandler",
            "filename": "access_extra.log",
            "formatter": "generic",
        },
    },
    "root": {
        "handlers": ["access_extra_file"],
    },
    "loggers": {
        "gunicorn.access.200": {
            "handlers": ["access_200_file"],
            "level": "INFO",
        },
        "gunicorn.access.other": {
            "handlers": ["access_other_file"],
            "level": "INFO",
        },
    },
}