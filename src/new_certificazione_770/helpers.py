# -*- coding: utf-8 -*-
# Built-in/Generic Imports
import os
import sys
from ctypes import WinDLL

# Libs

# Own modules

# Constants
MSG_ERROR_TEMPLATE = """Something goes wrong during {}:
Error:\n{}"""

MSG_WARNING_TEMPLATE = """Process {} terminate with warning:
Message:\n{}"""

MSG_SUCCESS_TEMPLATE = """Process {} terminate with success"""


def executable_path() -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, "frozen", False):
        # Running as bundled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running in development
        base_path = os.path.abspath(os.path.dirname(__file__))

    return base_path


def resource_path() -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, "frozen", False):
        # Running as bundled executable
        base_path = sys._MEIPASS
    else:
        # Running in development
        base_path = os.path.abspath(os.path.dirname(__file__))

    return base_path


EXPORT_CODE_ENTE_PREV = "80078750587"
EXPORT_DENOM_ENTE_PREV = "INPS"

DEFAULT_SETTINGS = {
    "code_ente_prev": EXPORT_CODE_ENTE_PREV,
    "denom_ente_prev": EXPORT_DENOM_ENTE_PREV,
}

DEFAULT_COMPANY = {
    "fiscal_code": "04366341008",
    "company_name": "HERBALIFE ITALIA SPA",
    "company_city": "ROMA",
    "company_province": "RM",
    "company_zip_code": "00144",
    "company_address": "VIA AMSTERDAM, 125",
    "forniture_code": "CUR24",
    "activity_code": "479910",
    "activity_type": "01",
}


def instance_check(app_name: str):
    u32dll = WinDLL("user32")
    # get the handle of any window matching app_name
    hwnd = u32dll.FindWindowW(None, app_name)
    if hwnd:  # if a matching window exists...
        # focus the existing window
        u32dll.ShowWindow(hwnd, 5)
        u32dll.SetForegroundWindow(hwnd)
        # bail
    return True
