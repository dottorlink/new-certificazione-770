# -*- coding: utf-8 -*-
"""
Import Dialog
"""

# Built-in/Generic Imports
import csv
import logging
import os
import tempfile
import tkinter as tk
from queue import Queue
from threading import Event
from tkinter import filedialog, messagebox, ttk
from typing import Any

# Libs
import pandas

# Own modules
from controllers import Controller, ResultThread
from helpers import MSG_ERROR_TEMPLATE, MSG_SUCCESS_TEMPLATE, MSG_WARNING_TEMPLATE
from models import Distributor, Invoice

from .dialog import BaseDialog

# Constants
VAR_FILE_PATH = "file_path"
VAR_MESSAGE = "message"
VAR_IMPORT_TYPE = "import_type"
VAR_CHECK_DELETE = "delete"


BTN_CONTROL = "Control"
BTN_IMPORT_EXCEL = "Import"

THREAD_IMPORT_DATA = "Import Data"
THREAD_CONTROL_EXCEL = "Control excel file"

REPORT_TEMPLATE = """
Final report
------------
- Inserted: {:,d}
- Updated: {:,d}
- Error: {:,d}
- Total: {:,d}
"""

DISTRIBUTOR_FIELDS_LIST = [
    ("IdDistributore", str, "number"),
    ("Nome", str, "name"),
    ("Cognome", str, "last_name"),
    ("Sesso", str, "gender"),
    ("PartitaIVA", str, "vat_number"),
    ("CodiceFiscale", str, "fiscal_code"),
    ("CittaDiNascita", str, "birth_city"),
    ("ProvinciaDiNascita", str, "birth_province"),
    ("DataDiNascita", str, "birth_date"),
    ("CittaDiResidenza", str, "residential_city"),
    ("ProvinciaDiResidenza", str, "residential_province"),
    ("CAPDiResidenza", str, "residential_zip_code"),
    ("IndirizzoDiResidenza", str, "residential_address"),
]

INVOICE_FIELDS_LIST = [
    ("Year", int, "year"),
    ("MbType", str, "mb_type"),
    ("InvoiceDate", str, "invoice_date"),
    ("InvoiceNumber", str, "number"),
    ("DistributorID", str, "distributor_number"),
    ("TaxableAmount", float, "taxable_amount"),
    ("VATAmount", float, "vat_amount"),
    ("INPSAmount", float, "inps_amount"),
    ("RitAmount", float, "rit_amount"),
    ("TotalAmount", float, "total_amount"),
    ("AliquotaIva", str, "aliquota_iva"),
]


class ImportDialog(BaseDialog):
    """Import dialog class

    Args:
        BaseDialog (_type_): base dialog
    """

    def __init__(self, parent=None, title="", **kwargs):
        self._event: Event | None = None
        self._queue: Queue | None = None
        self._data_frame = None
        self._controller: Controller | None = None
        super().__init__(parent=parent, title=title, **kwargs)

    def body(self, master):
        body_frm = ttk.Frame(master=master, padding=10, width=200)
        body_frm.pack(fill=tk.BOTH, expand=tk.Y)

        # Header
        self.headerbox(master=body_frm, default="import")

        # Subtitle
        self.label_frm = ttk.LabelFrame(
            master=body_frm,
            text="Complete the form to begin your import process",
            padding=5,
        )
        self.label_frm.pack(side=tk.TOP, expand=tk.Y, fill=tk.X)

        # File Path
        frm = ttk.Frame(master=self.label_frm, padding=5)
        frm.pack(side=tk.TOP, expand=tk.Y, fill=tk.X)
        lbl = ttk.Label(master=frm, padding=5, text="Import file path:")
        lbl.pack(side=tk.TOP, expand=tk.Y, fill=tk.X)
        self.setvar(VAR_FILE_PATH, "")
        ent = ttk.Entry(master=frm, textvariable=VAR_FILE_PATH, state="readonly")
        ent.bind(sequence="<Return>", func=self.browse)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=tk.Y, padx=5)
        self.browse_btn = ttk.Button(master=frm, text="Browse", command=self.browse)
        self.browse_btn.pack(side=tk.RIGHT, padx=5)

        # Import type
        frm = ttk.Frame(master=self.label_frm, padding=5)
        frm.pack(side=tk.TOP, expand=tk.Y, fill=tk.X)
        lbl = ttk.Label(master=frm, padding=5, text="Import type:", width=20)
        lbl.pack(side=tk.LEFT)
        options = [Distributor.__name__, Invoice.__name__]
        self.setvar(name=VAR_IMPORT_TYPE, value=options[1])
        ent = ttk.Combobox(
            master=frm, textvariable=VAR_IMPORT_TYPE, state="readonly", values=options
        )
        ent.bind(sequence="<<ComboboxSelected>>", func=self.select_import_type)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=tk.Y, padx=5)
        self.import_type_opt = ent

        # check delete table
        frm = ttk.Frame(master=self.label_frm, padding=5)
        frm.pack(side=tk.TOP, expand=tk.Y, fill=tk.X)
        # lbl = ttk.Label(
        #     master=frm, padding=5, text="Delete table before import", width=20
        # )
        # lbl.pack(side=tk.LEFT)
        self.setvar(name=VAR_CHECK_DELETE, value=True)
        ent = ttk.Checkbutton(
            master=frm,
            variable=VAR_CHECK_DELETE,
            text="Delete table before import",
            padding=10,
            style="Switch.TCheckbutton",
            onvalue=True,
            offvalue=False,
        )
        ent.pack(side=tk.LEFT, fill=tk.X, expand=tk.Y, padx=5)

        # Message frame
        frm = ttk.Frame(master=body_frm, padding=5)
        frm.pack(side=tk.TOP, fill=tk.X, expand=tk.Y)
        self.setvar(name=VAR_MESSAGE, value="Choose excel file")
        lbl = ttk.Label(master=frm, textvariable=VAR_MESSAGE)
        lbl.pack(side=tk.LEFT, fill=tk.X, expand=tk.Y, padx=5)
        self.action_btn = ttk.Button(
            master=frm,
            text=BTN_CONTROL,
            command=self.control_excel_file,
            state=tk.DISABLED,
            style="Accent.TButton",
        )
        self.action_btn.pack(side=tk.RIGHT, padx=5)

        self.progress_bar = ttk.Progressbar(master=body_frm, mode="indeterminate")
        self.progress_bar.pack(side=tk.TOP, fill=tk.X, expand=tk.Y, pady=5)

        self.treeview = ttk.Treeview(
            master=body_frm,
            show="tree",
            height=5,
            columns=["Message"],
        )
        self.treeview.column(column="#0", width=150, anchor="w")
        self.treeview.column(column="Message", width=250, anchor="w", stretch=True)
        self.treeview.pack(side=tk.TOP, fill=tk.X, expand=tk.Y, pady=5)

        self.resizable(0, 0)

    def buttonbox(self):
        """Button box"""
        box = ttk.Frame(master=self)

        w = ttk.Button(box, text="Cancel", width=20, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind(sequence="<Escape>", func=self.cancel)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        ttk.Separator(self).pack(fill=tk.X)
        box.pack(side=tk.BOTTOM)

    def cancel(self, event=None) -> None:
        if self._event is not None:
            msg = "There is a process that is running.\n\nDo you want to stop it?"
            ask = messagebox.askyesno(
                message=msg, title="Stop process?", default="no", parent=self
            )
            if ask:
                self._event.set()
            return
        return super().cancel()

    def browse(self):
        """Browse action

        Args:
            event (_type_, optional): _description_. Defaults to None.
        """
        _action = "Choose file"
        logging.debug(msg=_action)
        self.treeview.delete(*self.treeview.get_children())
        self.action_btn.config(state=tk.DISABLED, text=BTN_CONTROL)
        self.setvar(name=VAR_FILE_PATH, value="")
        self.setvar(name=VAR_MESSAGE, value=f"{_action}...")
        self._data_frame = None
        excel_file_path = filedialog.askopenfilename(
            parent=self,
            filetypes=[
                ("Excel file (*.xls, *.xlsx, *.xlsm)", "*.xls *.xlsx *.xlsm"),
                ("All file (*.*)", "*.*"),
            ],
            title="Chose an excel file to import",
        )
        if excel_file_path:
            _item = "file"
            f_path, f_name = os.path.split(excel_file_path)
            logging.info(msg=f"{_action}: {f_path=}, {f_name=}")
            self.setvar(name=VAR_FILE_PATH, value=excel_file_path)
            self.setvar(name=VAR_MESSAGE, value="Ready to control")
            if self.treeview.exists(item=_item):
                self.treeview.delete(_item)
            self.treeview.insert(
                parent="",
                index="end",
                iid=_item,
                text=_action,
                values=("Success"),
                open=True,
            )
            self.treeview.insert(
                parent=_item, index="end", text="Path", values=(f_path)
            )
            iid = self.treeview.insert(
                parent=_item, index="end", text="Name", values=(f_name)
            )
            self.treeview.see(item=iid)
            self.treeview.selection_set(_item)
            self.action_btn.config(
                state=tk.NORMAL,
                text=BTN_CONTROL,
                command=self.control_excel_file,
            )
        else:
            self.setvar(name=VAR_MESSAGE, value="Choose a file")

    def control_excel_file(self) -> None:
        """Control excel file action"""
        _excel_file = self.getvar(name=VAR_FILE_PATH)
        _action = THREAD_CONTROL_EXCEL
        logging.debug(msg=_action)
        if _excel_file is None:
            logging.warning(msg=f"{_action}: no file choose")
            msg = MSG_WARNING_TEMPLATE.format(_action, "No file choose")
            messagebox.showwarning(title=_action, message=msg, parent=self)
            return

        _model = self.getvar(name=VAR_IMPORT_TYPE)

        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start()
        self.action_btn.config(state=tk.DISABLED)
        self.set_frame_state(self.label_frm, tk.DISABLED)

        _item = "control"
        self.setvar(name=VAR_MESSAGE, value=f"{_action}... Running")
        if self.treeview.exists(item=_item):
            self.treeview.delete(_item)
        self.treeview.insert(
            parent="", index="end", iid=_item, text=_action, values=("Running")
        )
        self.treeview.see(item=_item)
        self.treeview.selection_set(_item)

        _action = f"Start thread {THREAD_CONTROL_EXCEL}"
        logging.debug(msg=_action)
        self._event = Event()
        _thread = ResultThread(
            name=THREAD_CONTROL_EXCEL,
            target=_thread_control_excel_file,
            args=(_excel_file, _model, self._event),
        )
        _thread.start()
        self.after(ms=200, func=lambda t=_thread: self.monitor_thread(thread=t))

    def import_excel_file_data(self):
        """Import excel file data process"""
        if self._data_frame is None:
            return

        if self._controller is None:
            # Check Controller
            _action = "Check Controller"
            logging.debug(msg=_action)
            self._controller = self._args.get("controller", None)
            if self._controller is None:
                logging.error(msg=f"{_action}: No controller passed to dialog")
                msg = MSG_ERROR_TEMPLATE.format(
                    _action, "No controller passed to dialog"
                )
                messagebox.showerror(title=_action, message=msg, parent=self)
                return

        self.update_idletasks()
        self.action_btn.config(state=tk.DISABLED)
        self.set_frame_state(self.label_frm, tk.DISABLED)
        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start()

        # Import data
        _action = THREAD_IMPORT_DATA
        logging.debug(msg=_action)
        _item = "import"
        self.browse_btn.config(state=tk.DISABLED)
        if self.treeview.exists(item=_item):
            self.treeview.delete(_item)
        self.treeview.insert(
            parent="",
            index="end",
            iid=_item,
            text=_action,
            values=("Running"),
            open=True,
        )
        self.treeview.see(item=_item)
        self.treeview.selection_set(_item)

        # Delete table
        _model = self.getvar(name=VAR_IMPORT_TYPE)
        if self.getvar(name=VAR_CHECK_DELETE) == 1:
            _action = "Delete table"
            logging.debug(msg=_action)
            iid = self.treeview.insert(
                parent=_item, index="end", text=_action, values=("Running")
            )
            self.treeview.see(item=iid)
            msg = f"Do you really want to delete all records in table {_model}?"
            ask = messagebox.askyesnocancel(
                title=_action, message=msg, default="no", parent=self
            )
            if ask is None:
                logging.warning(msg=f"{_action}: cancel")
                self.treeview.item(item=iid, values=("Cancel"))
                self.treeview.item(item=_item, values=("Cancel"))
                self.progress_bar.stop()
                self.action_btn.config(state=tk.NORMAL)
                self.set_frame_state(self.label_frm, tk.NORMAL)
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Cancel")
                return
            if ask:
                try:
                    self._controller.delete_table(model=_model)
                    self.setvar(name=VAR_MESSAGE, value=f"{_action}... Success")
                    self.treeview.item(item=iid, values=("Success"))
                    msg = MSG_SUCCESS_TEMPLATE.format(_action)
                    logging.info(msg=msg)
                except Exception as e:
                    logging.exception(msg=_action)
                    self.progress_bar.stop()
                    self.browse_btn.config(state=tk.NORMAL)
                    self.set_frame_state(self.label_frm, tk.NORMAL)
                    self.setvar(name=VAR_MESSAGE, value=f"{_action}... Error")
                    self.treeview.item(item=_item, values=("Error"))
                    self.treeview.item(item=iid, values=(str(e)))
                    msg = MSG_ERROR_TEMPLATE.format(_action, str(e))
                    messagebox.showerror(title=_action, message=msg, parent=self)
                    return
            else:
                logging.warning(msg=f"{_action}: bypass by user")
                self.treeview.item(item=iid, values=("Bypass"))

        # Add data to queue
        try:
            _action = "Add data to queue"
            logging.debug(msg=_action)
            iid = self.treeview.insert(
                parent=_item, index="end", text=_action, values=("Running")
            )
            self.treeview.see(item=iid)
            _model = self.getvar(name=VAR_IMPORT_TYPE)
            self._queue = _add_item_to_queue(model=_model, in_data=self._data_frame)
            total = self._queue.maxsize
            self.setvar(name=VAR_MESSAGE, value=f"{_action}... Success")
            self.treeview.item(item=iid, values=(f"{total:,d} record(s)"))
            msg = MSG_SUCCESS_TEMPLATE.format(_action)
            logging.info(msg=f"{msg}: records={total:,d}")
        except Exception as e:
            logging.exception(msg=_action)
            self.progress_bar.stop()
            self.action_btn.config(state=tk.NORMAL)
            self.set_frame_state(self.label_frm, tk.NORMAL)
            self.setvar(name=VAR_MESSAGE, value=f"{_action}... Error")
            self.treeview.item(item=_item, values=("Error"))
            self.treeview.item(item=iid, values=(str(e)))
            msg = MSG_ERROR_TEMPLATE.format(_action, str(e))
            messagebox.showerror(title=_action, message=msg, parent=self)
            return

        # Start thread
        _action = f"Start thread {THREAD_IMPORT_DATA}"
        logging.debug(msg=_action)
        self.progress_bar.stop()
        self.progress_bar.config(mode="determinate", value=0, maximum=total)
        self._event = Event()
        _thread = ResultThread(
            name=THREAD_IMPORT_DATA,
            target=_thread_import_data_on_db,
            args=(self._controller, _model, self._queue, self._event),
        )
        _thread.start()
        self.after(ms=200, func=lambda t=_thread: self.monitor_thread(thread=t))

    def select_import_type(self, event=None):
        """Change import type selection event

        Args:
            event (_type_, optional): _description_. Defaults to None.
        """
        if self.getvar(name=VAR_IMPORT_TYPE) == Invoice.__name__:
            self.setvar(name=VAR_CHECK_DELETE, value=True)
        # Change action button
        self.action_btn.config(
            text=BTN_CONTROL,
            command=self.control_excel_file,
        )

    def monitor_thread(self, thread: ResultThread) -> None:
        if thread.is_alive():
            if thread.name == THREAD_IMPORT_DATA:
                _total = self._queue.maxsize
                _ind = _total - self._queue.unfinished_tasks
                _msg = f"{THREAD_IMPORT_DATA} processing record {_ind:,d} of {_total:,d}..."
                self.setvar(
                    name=VAR_MESSAGE,
                    value=_msg,
                )
                self.progress_bar.config(value=_ind)

            self.after(ms=100, func=lambda: self.monitor_thread(thread=thread))
            return

        _action = thread.name
        logging.debug(msg=f"Thread {_action} terminated")
        self.progress_bar.stop()
        self._event = None
        self.action_btn.config(state=tk.NORMAL)
        self.set_frame_state(self.label_frm, tk.NORMAL)
        if thread.name == THREAD_CONTROL_EXCEL:
            _item = "control"
            res_code, res_msg, res_data = thread.result
            if res_code < 0:
                logging.error(msg=f"{_action}: {res_code=}, {res_msg=}")
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Error!")
                self.treeview.item(item=_item, values=("Error"))
                msg = MSG_ERROR_TEMPLATE.format(_action, res_msg)
                messagebox.showerror(title=_action, message=msg, parent=self)
                return
            elif res_code > 0:
                logging.warning(msg=f"{_action}: {res_code=}, {res_msg=}")
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Warning!")
                self.treeview.item(item=_item, values=("Warning"))
                msg = MSG_WARNING_TEMPLATE.format(_action, res_msg)
                messagebox.showwarning(title=_action, message=msg, parent=self)
                return
            else:
                self._data_frame = res_data
                self.setvar(name=VAR_MESSAGE, value="Click on Import")
                iid = self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Records",
                    values=(f"{len(self._data_frame):,d}"),
                )
                iid = self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Columns",
                    values=(f"{len(self._data_frame.columns):,d}"),
                )
                self.treeview.see(item=iid)
                self.treeview.item(item=_item, values=("Success"))
                self.action_btn.config(
                    text=BTN_IMPORT_EXCEL, command=self.import_excel_file_data
                )
                self.action_btn.focus_set()
                msg = MSG_SUCCESS_TEMPLATE.format(_action)
                logging.info(msg=f"{msg}: records={len(self._data_frame):,d}")
                return

        elif thread.name == THREAD_IMPORT_DATA:
            _item = "import"
            res_code, res_msg, res_data, res_file_name = thread.result
            if res_code < 0:
                logging.error(msg=f"{_action}: {res_code=}, {res_msg=}")
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Error!")
                self.treeview.item(item=_item, values=("Error"))
                msg = MSG_ERROR_TEMPLATE.format(_action, res_msg)
                messagebox.showerror(title=_action, message=msg, parent=self)
                return
            elif res_code > 0:
                logging.warning(msg=f"{_action}: {res_code=}, {res_msg=}")
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Warning!")
                self.treeview.item(item=_item, values=("Warning"))
                msg = MSG_WARNING_TEMPLATE.format(_action, res_msg)
            else:
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Success!")
                self.treeview.item(item=_item, values=("Success"))
                msg = MSG_SUCCESS_TEMPLATE.format(_action, res_msg)
                logging.info(msg=msg)

            self.treeview.see(item=_item)
            if res_data:
                _total = self._queue.maxsize
                msg += REPORT_TEMPLATE.format(
                    res_data[0], res_data[1], res_data[2], _total
                )
                self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Total",
                    values=(f"{_total:,d}"),
                )
                self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Inserted",
                    values=(f"{res_data[0]:,d}"),
                )
                self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Updated",
                    values=(f"{res_data[1]:,d}"),
                )
                iid = self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Error",
                    values=(f"{res_data[2]:,d}"),
                )
                self.treeview.item(item=_item, open=True)
                self.treeview.see(item=iid)
                self.treeview.selection_set(_item)
                logging.info(msg=f"{_action}: {res_data=}")
            if res_file_name and int(res_data[2]) > 0:
                logging.info(msg=f"{_action}: {res_file_name=}")
                msg += (
                    "\n\nSome records were not entered due to an error."
                    "\nDo you want to open the temporary excel file with errors?"
                )
                ask = messagebox.askyesno(title=_action, message=msg, parent=self)
                if ask:
                    os.startfile(filepath=f"{res_file_name}")
            else:
                messagebox.showinfo(title=_action, message=msg, parent=self)
            self.result = "Ok"
            return


def _add_item_to_queue(model: str, in_data: Any):
    _queue: Queue
    if model == Distributor.__name__:
        columns_map = [(v[0], v[2]) for v in DISTRIBUTOR_FIELDS_LIST]
    elif model == Invoice.__name__:
        columns_map = [(v[0], v[2]) for v in INVOICE_FIELDS_LIST]
    else:
        raise TypeError(f"Unknown model: {model=}")

    _result_dict = in_data.to_dict(orient="records")
    _queue = Queue(maxsize=len(_result_dict))
    for row in _result_dict:
        _item = {new: row[old] for old, new in columns_map}
        _queue.put(item=_item, block=False)
    return _queue


def _thread_control_excel_file(excel_file: str, model: str, event: Event):
    # Initialize
    try:
        _exit: int = 0
        _msg: str = "OK"
        _data_frame = None
        _action = "Check model"
        if model == Distributor.__name__:
            data_type = {v[0]: v[1] for v in DISTRIBUTOR_FIELDS_LIST}
            columns = [v[0] for v in DISTRIBUTOR_FIELDS_LIST]
        elif model == Invoice.__name__:
            data_type = {v[0]: v[1] for v in INVOICE_FIELDS_LIST}
            columns = [v[0] for v in INVOICE_FIELDS_LIST]
        else:
            _exit = 2
            _msg = f"Unknown model: {model=}"
            return (_exit, _msg, None)

        # ---
        _step = 0
        while event.is_set() is False:
            if _step == 0:
                _action = "Open Excel file"
                with pandas.ExcelFile(excel_file) as f_xls:
                    _data_frame = pandas.read_excel(
                        io=f_xls, dtype=data_type, na_filter=False
                    )
                _step += 1
                continue
            elif _step == 1:
                _action = "Check Data frame"
                if _data_frame.empty or _data_frame is None:
                    _exit = 1
                    _msg = "Data frame is EMPTY"
                    break
                _step += 1
                continue
            elif _step == 2:
                _action = "Check correct columns"
                if not set(columns).issubset(_data_frame.columns):
                    missing_columns = set(columns) - set(_data_frame.columns)
                    _msg = f"For excel file missing required columns: {", ".join(missing_columns)}"
                    _exit = 2
                    break
                _step += 1
                continue
            else:
                _action = "Adjust data frame data"
                _data_frame = _data_frame.replace(to_replace={pandas.NaT: None})
                _data_frame = _data_frame.map(
                    func=lambda x: x.upper()
                    if pandas.notnull(x) and type(x) is str
                    else x
                )
                if model == Distributor.__name__:
                    _data_frame["DataDiNascita"] = pandas.to_datetime(
                        arg=_data_frame["DataDiNascita"], format="mixed"
                    ).dt.date
                else:
                    _data_frame["InvoiceDate"] = pandas.to_datetime(
                        arg=_data_frame["InvoiceDate"], format="mixed"
                    ).dt.date
                break
        else:
            if event.is_set() is True:
                _exit = 1
                _data_frame = None
                _msg = "Thread stopped by user"

        return (_exit, _msg, _data_frame)
    except Exception as e:
        _msg = f"{_action}: {str(e)}"
        _exit = -1
        return (_exit, _msg, _data_frame)


def _thread_import_data_on_db(
    controller: Controller, model: str, queue: Queue, event: Event
):
    try:
        # Initialize
        _inserted: int = 0
        _updated: int = 0
        _error: int = 0
        _records = [_inserted, _updated, _error]
        _csv_fd = None
        _msg: int = "OK"
        _exit: int = 0

        # Open csv file
        _action = "Open csv file"
        with tempfile.NamedTemporaryFile(
            mode="wt",
            encoding="utf-8",
            newline="",
            delete=False,
            suffix=".csv",
            delete_on_close=True,
        ) as _temp_fd:
            _csv_fd = csv.writer(
                _temp_fd, delimiter=",", quoting=csv.QUOTE_MINIMAL, lineterminator="\n"
            )
            # Loop queue
            while not queue.empty():
                if event.is_set():
                    _exit = 1
                    _msg = "Thread stopped by user"
                    break

                _action = "Get item from queue"
                item = queue.get()

                try:
                    _action = "Import_data"
                    _, is_updated = controller.import_data(data=item, model=model)
                    # Update the counters based on the return value of the controller method
                    if is_updated is True:
                        _updated += 1
                    else:
                        _inserted += 1
                except Exception as e:
                    if _error == 0:
                        field_names = list(item.keys())
                        field_names.append("Error")
                        _csv_fd.writerow(field_names)
                    _error += 1
                    if item is not None:
                        _values = list(item.values())
                        _values.append(str(e))
                        _csv_fd.writerow(_values)
                finally:
                    queue.task_done()
                    _records = [_inserted, _updated, _error]

            if _error == 0 and _temp_fd:
                _temp_fd.close()
            return (
                _exit,
                _msg,
                _records,
                (_temp_fd.name if _temp_fd and _error > 0 else None),
            )

    except Exception as e:
        if _error == 0 and _temp_fd:
            _temp_fd.close()
        _msg = f"{_action}: {str(e)}"
        _exit = -1
        return (_exit, _msg, _records, (_temp_fd.name if _temp_fd else None))
