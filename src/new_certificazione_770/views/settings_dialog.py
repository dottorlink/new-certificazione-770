# -*- coding: utf-8 -*-
"""
_Description_
"""
# Built-in/Generic Imports

# Libs
import tkinter as tk
import tkinter.ttk as ttk

# Own modules
try:
    from models import Setting
except:
    from new_certificazione_770.models import Setting

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

        self.fields_list = Setting.model_json_schema(mode="serialization")["properties"]

        scroll_frm = ScrolledFrame(
            master=body_frm,
            autohide=True,
            width=500,
            height=400,
            padding=10,
        )
        scroll_frm.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        self.entry_by_fields(master=scroll_frm, fields_list=self.fields_list)

        data = self._args.get("data", None)
        if data:
            for key, val in data.items():
                self.setvar(name=key, value=(val if val else ""))

        self.update_idletasks()
