# -*- coding: utf-8 -*-
"""
_Description_
"""
# Built-in/Generic Imports

# Libs
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# Own modules
from .dialog import BaseDialog
from .widgets import ScrolledFrame

# Constants
#


class SettingsDialog(BaseDialog):
    def __init__(self, parent=None, title="", **kwargs):
        super().__init__(parent=parent, title=title, **kwargs)

    def body(self, master):
        self.resizable(0, 0)
        body_frm = ttk.Frame(master=master, padding=10)
        body_frm.pack(fill=tk.BOTH, expand=tk.YES)

        # Header
        self.headerbox(master=body_frm, default="company")

        _txt = "Complete the following form with the setting's information"
        lbl = ttk.Label(
            master=body_frm,
            text=_txt,
            font=("TkDefaultFont", 9, "bold"),
            padding=10,
        )
        lbl.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)

        self.fields_list = {}
        scroll_frm = ScrolledFrame(
            master=body_frm,
            autohide=True,
            width=400,
            height=300,
            padding=10,
        )
        scroll_frm.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.settings = self._args.get("settings", None)

        for item in self.settings:
            text = item.get("title")
            name = item.get("name")
            value = item.get("value", "")
            lbl = ttk.Label(master=scroll_frm, text=text)
            lbl.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
            _ent = ttk.Entry(master=scroll_frm, textvariable=name)
            _ent.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx=(0, 5), pady=(0, 5))
            self.setvar(name=name, value=value)
            self.fields_list[name] = item

        self.update_idletasks()

    def validate(self) -> bool:
        self.result = None
        for key in self.fields_list.keys():
            try:
                val = self.getvar(name=key)
            except Exception as e:
                msg = "Invalid data!\nError:"
                msg += f"\n - Field {key} is invalid: {e}"
                msg += "\n\nControl field values and retry"
                messagebox.showerror(title="Validate data", message=msg, parent=self)
                self.result = None
                return False

            if val is None or val == "":
                msg = "Invalid data!\nError:"
                msg += f"\n - Field {key} is invalid: null value"
                msg += "\n\nControl field values and retry"
                messagebox.showerror(title="Validate data", message=msg, parent=self)
                self.result = None
                return False
            else:
                self.fields_list[key]["value"] = val

        self.result = list(self.fields_list.values())
        return True
