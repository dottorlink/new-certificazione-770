# -*- coding: utf-8 -*-
"""
Import Dialog
"""

# Built-in/Generic Imports
import datetime
import logging
import os
from queue import Queue
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from threading import Event

# Libs
from tkcalendar import DateEntry

# Own modules
from ..controllers.result_thread import ResultThread
from ..controllers.controller import Controller
from ..models.dat_model import DATFile
from ..helpers import MSG_ERROR_TEMPLATE, MSG_WARNING_TEMPLATE, MSG_SUCCESS_TEMPLATE
from ..views.dialog import BaseDialog

# Constants
VAR_EXPORT_FOLDER = "export_folder"
VAR_MESSAGE = "message"
VAR_EXPORT_TYPE = "export_type"
VAR_EXPORT_LIMIT = "export_limit"
VAR_EXPORT_YEAR = "export_year"
VAR_SIGNATURE_DATE = "signature_date"

OPT_YEARS_LIST = "years"

BTN_EXPORT = "Export"

EXPORT_TYPE_DAT = "Export DAT"
EXPORT_TYPE_GUFANA = "Export GUFANA"

THREAD_EXPORT_DAT = EXPORT_TYPE_DAT
THREAD_EXPORT_GUFANA = EXPORT_TYPE_GUFANA

REPORT_TEMPLATE = """
Final report
------------
- Exported: {:,d}
- Total: {:,d}
"""


class ExportDialog(BaseDialog):
    def __init__(self, parent=None, title="", **kwargs):
        self._event: Event | None = None
        self._queue: Queue | None = None
        self._data_frame = None
        self._controller: Controller | None = None
        super().__init__(parent=parent, title=title, **kwargs)

    def body(self, master):
        body_frm = ttk.Frame(master=master, padding=10)
        body_frm.pack(fill=tk.BOTH, expand=tk.YES)

        # Header
        self.headerbox(master=body_frm, default="export")

        # Subtitle
        _txt = "Complete the form to begin your export process"
        lbl = ttk.Label(
            master=body_frm, text=_txt, font=("TkDefaultFont", 9, "bold"), padding=10
        )
        lbl.pack(side=tk.TOP, expand=1, fill=tk.X)

        # Export folder
        _ind = 1
        frm = ttk.LabelFrame(master=body_frm, padding=5, text=f"{_ind}. Export folder:")
        frm.pack(
            side=tk.TOP,
            fill=tk.X,
        )
        var = tk.StringVar(master=self, name=VAR_EXPORT_FOLDER, value="")
        ent = ttk.Entry(master=frm, textvariable=var, state="readonly")
        ent.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=5)
        ent.bind(sequence="<Return>", func=self.browse)
        btn = ttk.Button(master=frm, image="folder", command=self.browse)
        btn.pack(side=tk.RIGHT, padx=5)
        btn.focus_set()

        # Export type
        _ind += 1
        frm = ttk.LabelFrame(master=body_frm, padding=5, text=f"{_ind} Export type:")
        frm.pack(side=tk.TOP, fill=tk.X)
        options = [EXPORT_TYPE_DAT]
        ent = ttk.Combobox(
            master=frm, textvariable=VAR_EXPORT_TYPE, state="readonly", values=options
        )
        self.setvar(name=VAR_EXPORT_TYPE, value=options[0])
        ent.pack(side=tk.TOP, fill=tk.X)

        # Export year
        _ind += 1
        frm = ttk.LabelFrame(master=body_frm, padding=5, text=f"{_ind}. Export year:")
        frm.pack(side=tk.TOP, fill=tk.X)
        options = self._args.get(OPT_YEARS_LIST, [2024])
        ent = ttk.Combobox(
            master=frm, textvariable=VAR_EXPORT_YEAR, state="readonly", values=options
        )
        self.setvar(name=VAR_EXPORT_YEAR, value=options[0])
        ent.pack(side=tk.TOP, fill=tk.X)

        # Export signature date
        _ind += 1
        frm = ttk.LabelFrame(
            master=body_frm, padding=5, text=f"{_ind}. Export signature date:"
        )
        frm.pack(side=tk.TOP, fill=tk.X)
        ent = DateEntry(
            master=frm,
            selectmode="day",
            date_pattern="yyyy-MM-dd",
            locale="it_IT",
            textvariable=VAR_SIGNATURE_DATE,
        )
        self.setvar(name=VAR_SIGNATURE_DATE, value=datetime.date.today().isoformat())
        ent.pack(side=tk.TOP, fill=tk.X)

        # Export record limit
        _ind += 1
        frm = ttk.LabelFrame(
            master=body_frm, padding=5, text=f"{_ind}. Export record limit:"
        )
        frm.pack(side=tk.TOP, fill=tk.X)
        options = ["All", "1000", "100", "10", "5"]
        ent = ttk.Combobox(
            master=frm,
            state="readonly",
            values=options,
            textvariable=VAR_EXPORT_LIMIT,
        )
        self.setvar(name=VAR_EXPORT_LIMIT, value=options[0])
        ent.pack(side=tk.TOP, fill=tk.X)

        # Message frame
        _ind += 1
        frm = ttk.LabelFrame(
            master=body_frm, padding=5, text=f"{_ind}. Click to export:"
        )
        frm.pack(side=tk.TOP, fill=tk.X)
        row = ttk.Frame(master=frm)
        row.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        lbl = ttk.Label(
            master=row, textvariable=VAR_MESSAGE, text="Choose a file", width=50
        )
        self.setvar(name=VAR_MESSAGE, value="Choose a folder")
        lbl.pack(side=tk.LEFT, fill=tk.X, padx=5)
        self.action_btn = ttk.Button(
            master=row,
            text=BTN_EXPORT,
            command=self.export,
            state=tk.DISABLED,
            style="Accent.TButton",
        )
        self.action_btn.pack(side=tk.RIGHT, padx=5)

        self.progress_bar = ttk.Progressbar(master=frm, mode="indeterminate")
        self.progress_bar.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.treeview = ttk.Treeview(
            master=frm,
            show="tree",
            height=5,
            columns=["Message"],
        )
        self.treeview.column(column="#0", width=150, anchor="w")
        self.treeview.column(column="Message", width=200, anchor="w", stretch=True)
        self.treeview.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.resizable(0, 0)

    def buttonbox(self):
        """Button box"""
        box = ttk.Frame(master=self)

        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind(sequence="<Escape>", func=self.cancel)

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

    def browse(self, event=None):
        self.treeview.delete(*self.treeview.get_children())
        self.action_btn.config(state=tk.DISABLED, text=BTN_EXPORT)

        self.setvar(name=VAR_EXPORT_FOLDER, value="")
        self.setvar(name=VAR_MESSAGE, value="Choose a folder")
        self._queue = None
        folder = filedialog.askdirectory(
            parent=self,
            mustexist=True,
            title="Chose a folder to export",
        )
        if folder:
            _action = "Choose folder"
            logging.info(msg=f"{_action}: {folder=}")
            _item = "folder"
            self.treeview.delete(*self.treeview.get_children())
            self.setvar(name=VAR_EXPORT_FOLDER, value=folder)
            self.setvar(name=VAR_MESSAGE, value="Ready to export")
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
            iid = self.treeview.insert(
                parent=_item, index="end", text="Path", values=(folder)
            )
            self.treeview.see(item=iid)
            self.treeview.selection_set(_item)
            self.action_btn.config(state=tk.NORMAL)
            self.action_btn.focus_set()

    def export(self) -> None:
        _action = "Check Controller"
        logging.debug(msg=_action)
        if self._controller is None:
            _controller = self._args.get("controller", None)
            if _controller is None:
                msg = MSG_ERROR_TEMPLATE.format(
                    _action, "No controller passed to dialog"
                )
                messagebox.showerror(title=_action, message=msg, parent=self)
                return

            self._controller = _controller

        _folder = self.getvar(name=VAR_EXPORT_FOLDER)
        if _folder is None:
            logging.warning(msg="No folder choose")
            msg = MSG_WARNING_TEMPLATE.format(_action, "No folder choose")
            messagebox.showwarning(title=_action, message=msg, parent=self)
            return

        self.progress_bar.config(mode="indeterminate", value=0)
        self.progress_bar.start()
        self.action_btn.config(state=tk.DISABLED)

        _action = BTN_EXPORT
        _item = "export"
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
        self.setvar(name=VAR_MESSAGE, value=f"{_action}... Running")

        # Get data from database
        try:
            _action = "Get data from database"
            iid = self.treeview.insert(
                parent=_item, index="end", text=_action, values=("Running")
            )
            self.treeview.see(item=iid)
            self.setvar(name=VAR_MESSAGE, value=f"{_action}... Running")

            # Arguments
            export_year = self.getvar(name=VAR_EXPORT_YEAR)
            export_limit = self.getvar(name=VAR_EXPORT_LIMIT)
            if export_limit == "All":
                export_limit = None
            else:
                export_limit = int(export_limit)
            logging.debug(msg=f"{_action}: {export_year=}, {export_limit=}")

            data = self._controller.get_data_for_export_dat(
                year=export_year, limit=export_limit
            )
            if data is None:
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Warning")
                self.treeview.item(item=_item, values="Warning")
                msg = f"No data found for {export_year=}, {export_limit=}"
                logging.warning(msg=f"{_action}: {msg}")
                self.treeview.item(item=iid, values=(msg))
                msg = MSG_WARNING_TEMPLATE.format(_action, msg)
                messagebox.showwarning(title=_action, message=msg, parent=self)
                return

            msg = MSG_SUCCESS_TEMPLATE.format(_action)
            self.treeview.item(item=iid, values=(f"{len(data):,d}"))
            logging.info(msg=f"{msg}: records={len(data):,d}")
        except Exception as e:
            logging.exception(msg=_action)
            self.progress_bar.stop()
            self.action_btn.config(state=tk.NORMAL)
            self.setvar(name=VAR_MESSAGE, value=f"{_action}... Error")
            self.treeview.item(item=_item, values=("Error"))
            self.treeview.item(item=iid, values=(str(e)))
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)
            return

        # Add data to queue
        try:
            _action = "Add data to queue"
            logging.debug(msg=_action)
            self.setvar(name=VAR_MESSAGE, value=f"{_action}... Running")
            iid = self.treeview.insert(
                parent=_item, index="end", text=_action, values=("Running")
            )
            self.treeview.see(item=iid)
            total = len(data)
            self._queue = Queue(maxsize=total)
            for item in data:
                self._queue.put(item=item)
            self.setvar(name=VAR_MESSAGE, value=f"{_action}... Success")
            msg = MSG_SUCCESS_TEMPLATE.format(_action)
            self.treeview.item(item=iid, values=(f"{total:,d}"))
            logging.info(msg=f"{msg}: records={total:,d}")
        except Exception as e:
            logging.exception(msg=_action)
            self.progress_bar.stop()
            self.action_btn.config(state=tk.NORMAL)
            self.setvar(name=VAR_MESSAGE, value=f"{_action}... Error")
            self.treeview.item(item=_item, values="Error")
            self.treeview.item(item=iid, values=(str(e)))
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)
            return

        # Export
        _action = BTN_EXPORT
        logging.debug(msg=_action)
        self.setvar(name=VAR_MESSAGE, value=f"{_action}... Running")

        self.progress_bar.stop()
        self.progress_bar.config(mode="determinate", value=0, maximum=total)

        export_folder = self.getvar(name=VAR_EXPORT_FOLDER)
        export_type = self.getvar(name=VAR_EXPORT_TYPE)
        export_signature_date = self.getvar(name=VAR_SIGNATURE_DATE)
        export_code_ente_prev = self._args.get("code_ente_prev", "")
        export_denom_ente_prev = self._args.get("denom_ente_prev", "")

        _action = f"Start thread {THREAD_EXPORT_DAT}"
        logging.debug(msg=_action)
        self._event = Event()
        _thread = ResultThread(
            name=THREAD_EXPORT_DAT,
            target=thread_export_data,
            args=(
                export_folder,
                export_code_ente_prev,
                export_denom_ente_prev,
                export_signature_date,
                export_type,
                self._queue,
                self._event,
            ),
        )
        _thread.start()
        self.after(ms=200, func=lambda t=_thread: self.monitor_thread(thread=t))

    def monitor_thread(self, thread: ResultThread) -> None:
        if thread.is_alive():
            if thread.name == THREAD_EXPORT_DAT:
                _total = self._queue.maxsize
                _ind = _total - self._queue.unfinished_tasks
                self.setvar(
                    name=VAR_MESSAGE,
                    value=f"{THREAD_EXPORT_DAT} processing record {_ind} of {_total}...",
                )
                self.progress_bar.config(value=_ind)
            self.after(ms=200, func=lambda: self.monitor_thread(thread=thread))
            return

        _action = thread.name
        logging.debug(msg=f"Thread {_action} terminated")
        self._event = None
        if thread.name == THREAD_EXPORT_GUFANA:
            # TODO
            return

        if thread.name == THREAD_EXPORT_DAT:
            _item = "export"
            res_code, res_msg, res_data, res_file_name = thread.result
            if res_code < 0:
                logging.error(msg=f"{_action}: {res_code=}, {res_msg=}")
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Error!")
                self.treeview.item(item=_item, values=("Error"))
                msg = MSG_ERROR_TEMPLATE.format(_action, res_msg)
                messagebox.showerror(title=_action, message=msg, parent=self)
                self.result = None
                return
            elif res_code > 0:
                logging.warning(msg=f"{_action}: {res_code=}, {res_msg=}")
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Warning!")
                self.treeview.item(item=_item, values=("Warning"))
                msg = MSG_WARNING_TEMPLATE.format(_action, res_msg)
            else:
                self._data_frame = res_data
                self.setvar(name=VAR_MESSAGE, value=f"{_action}... Success!")
                self.treeview.item(item=_item, values=("Success"))
                msg = MSG_SUCCESS_TEMPLATE.format(_action)
                logging.info(msg=msg)

            if res_data:
                _total = self._queue.maxsize
                msg += REPORT_TEMPLATE.format(res_data, _total)
                iid = self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Total",
                    values=(_total),
                )
                iid = self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Exported",
                    values=(f"{res_data:,d}"),
                )
                self.treeview.see(item=iid)
                self.treeview.selection_set(_item)
            if res_file_name:
                logging.info(msg=f"{_action}: {res_file_name=}")
                f_path, f_name = os.path.split(res_file_name)
                iid = self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Report File Path",
                    values=(f_path),
                )
                iid = self.treeview.insert(
                    parent=_item,
                    index="end",
                    text="Report File Name",
                    values=(f_name),
                )
                self.treeview.see(item=iid)
                self.treeview.selection_set(_item)
                msg += "\n\nDo you want to open report file?"
                ask = messagebox.askyesno(title=_action, message=msg, parent=self)
                if ask:
                    os.startfile(filepath=f"{res_file_name}")
            else:
                messagebox.showinfo(title=_action, message=msg, parent=self)
            self.result = "Ok"


def thread_export_data(
    path: str,
    code_ente_prev: str,
    denom_ente_prev: str,
    signature_date: str,
    export_type: str,
    queue: Queue,
    event: Event,
):
    """Write CSV DAT file

    Args:
        path (str): data path for CSV file
        code_ente_prev (str): "codice ente previdenziale" constant to write in CSV
        denom_ente_prev (str): "denominazione ente previdenziale" constant to write in CSV
        signature_date (str): "data firma" constant to write in CSV
        queue (Queue): input queue for item to write in CSV
        event (Event): break control event

    Returns:
        dict[str, Any]: return a dictionary with fields
            {
                "exit_code": int (0 success, >0 warning, <0 error),
                "message": str "OK" | error message,
                "data": list(int) | None
            }
    """
    _dat_csv = None
    _records = 0
    _exit = 0
    _msg = "OK"
    try:
        # Open CSV file
        _action = "Open CSV DAT File"
        _dat_csv = DATFile(
            path=path,
            code_ente_prev=code_ente_prev,
            denom_ente_prev=denom_ente_prev,
            data_firma=signature_date,
        )
        _dat_csv.start()

        while not queue.empty():
            if event.is_set():
                _msg = "Thread stopped by user"
                _exit = 1
                break

            _action = "Read item from queue"
            item = queue.get()

            _action = "Write record on CSV"
            _dat_csv.write_record(data=item)
            _records += 1
            queue.task_done()

        return (_exit, _msg, _records, (_dat_csv.file_name if _dat_csv else None))
    except ValueError as e:
        _exit = 1
        return (_exit, str(e), _records, (_dat_csv.file_name if _dat_csv else None))
    except Exception as e:
        _exit = -1
        _msg = f"{_action}: {str(e)}"
        return (_exit, _msg, _records, (_dat_csv.file_name if _dat_csv else None))
