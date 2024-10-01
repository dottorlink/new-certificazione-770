# SPDX-FileCopyrightText: 2024-present Dottorlink <dottorlink@gmail.com>
#
# SPDX-License-Identifier: MIT

from . import (
    __author__,
    __copyright__,
    __description__,
    __email__,
    __license__,
    __package__,
    __version__,
)

VERSION = __version__
PACKAGE = __package__

DESCRIPTION = __description__
AUTHOR = __author__
EMAIL = __email__
COPYRIGHT = __copyright__
LICENSE = __license__

LICENSE_FILE_NAME = "LICENSE"

LOG_FILE_NAME = f"{PACKAGE}.log"

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
