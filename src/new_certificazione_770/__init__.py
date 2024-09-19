# SPDX-FileCopyrightText: 2024-present Dottorlink <dottorlink@gmail.com>
#
# SPDX-License-Identifier: MIT

__version__ = version = "0.2.0"
__package__ = package = "new-certificazione-770"

__description__ = description = (
    "Python EXE application for Certificazioni 770 for company Herbalife S.p.A. to create output file for INPS fiscal application."
)
__author__ = author = "Dottorlink"
__email__ = email = "dottorlink@gmail.com"
__copyright__ = copyright = "Copyright 2024, Dottorlink"
__license__ = license = "MIT"
__status__ = "Development"

LOG_FILE_NAME = f"{package}.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["stdout", "file"]},
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "level": "INFO",
            "filename": LOG_FILE_NAME,
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 500000,
            "backupCount": 3,
        },
    },
    "formatters": {
        "detailed": {
            "class": "logging.Formatter",
            "format": "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
        "simple": {
            "class": "logging.Formatter",
            "format": "%(module)s - %(levelname)s - %(funcName)s - %(message)s",
        },
    },
}
