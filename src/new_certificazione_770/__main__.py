# -*- coding: utf-8 -*-
"""
description

@File: main.py
@Date: 2024-08-14
"""

# Built-in/Generic Imports

# Libs
import os
import platform
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

# Modules
import sv_ttk
import darkdetect

from .controllers.controller import Controller
from .helpers import (
    DEFAULT_COMPANY,
    DEFAULT_SETTINGS,
    EXPORT_CODE_ENTE_PREV,
    EXPORT_DENOM_ENTE_PREV,
    MSG_ERROR_TEMPLATE,
    MSG_SUCCESS_TEMPLATE,
    executable_path,
    resource_path,
)
from .models.base_models import Company, Distributor, Setting
from .views.company_dialog import CompanyDialog
from .views.distributor_dialog import DistributorDialog
from .views.export_dialogs import ExportDialog
from .views.import_dialogs import ImportDialog
from .views.settings_dialog import SettingsDialog
from .views.widgets import Tableview

# Own modules


# Constants
__package__ = "new-certificazione-770"
__version__ = "1.0.0"
__author__ = "@Dottorlink"
__copyright__ = "Copyright 2024, Dottorlink"
__license__ = "GPL"
__email__ = "dottorlink@gmail.com"
__status__ = "Development"

EXE_PATH = executable_path()
RES_PATH = resource_path()

# Button Constants
BTN_ABOUT = f"About {__package__}"
BTN_COMPANY = "Company"
BTN_EXIT = "Exit"
BTN_EXPORT = "Export"
BTN_HELP = "Show help"
BTN_IMPORT = "Import"
BTN_SETTINGS = "Settings"
BTN_SHOW_LOG = "Show log"
BTN_USER_ADD = "Add"
BTN_USER_DELETE = "Delete"
BTN_USER_EDIT = "Edit"
BTN_USER_REFRESH = "Refresh"

# Theme Button
BTN_TOGGLE_THEME = "Toggle Theme"

# Var constants
VAR_STATUS_BAR = "status_bar"
VAR_SEARCH = "search_text"


class MainApp(tk.Frame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.pack(fill=tk.BOTH, expand=tk.YES)
        self.body_frm = ttk.Frame(master=self)
        self.body_frm.pack(fill=tk.BOTH, expand=tk.YES, side=tk.TOP)

        self.controller: Controller = None
        self.settings: dict = None

        try:
            _action = "Load images from assets folders"
            self._load_images()

            _action = "Draw application"
            self.create_menu_bar()
            self.create_status_bar()
            self.create_button_bar()
            self.create_left_panel()
            self.create_right_panel()
        except Exception as e:
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)
            self.master.quit()

        self.master.after(ms=200, func=self._initialize)

    def _load_images(self) -> None:
        """Load images from assets folders"""
        self.photo_images = []
        image_files = {
            "import": "icons8-import-24.png",
            "export": "icons8-export-24.png",
            "company": "icons8-company-24.png",
            "user-add": "icons8-add-user-male-24.png",
            "user-edit": "icons8-edit-user-24.png",
            "user-delete": "icons8-delete-user-24.png",
            "user": "icons8-user-24.png",
            "exit": "icons8-exit-24.png",
            "logo": "logo.png",
            "logo-small": "logo-small.png",
            "search": "icons8-search-24.png",
            "settings": "icons8-settings-24.png",
            "refresh": "icons8-refresh-24.png",
            "folder": "icons8-folder-24.png",
        }
        _img_path = os.path.join(RES_PATH, "assets")
        for key, val in image_files.items():
            _path = os.path.join(_img_path, val)
            self.photo_images.append(tk.PhotoImage(master=self, name=key, file=_path))

    def _initialize(self) -> None:
        try:
            if self.controller is None:
                _db_path = os.path.join(EXE_PATH, f"{__package__}.db")
                _action = f"Open/create database {_db_path}"
                self.controller = Controller(db_path=_db_path, echo=False)

            if self.settings is None:
                _action = "Get Settings from database"
                self._get_settings()
            _action = "Refresh treeview"
            self.treeview_refresh()
        except Exception as e:
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)
            self.master.quit()

    def create_menu_bar(self) -> None:
        menu_items = {
            "File": [
                BTN_IMPORT,
                BTN_EXPORT,
                "---",
                BTN_EXIT,
            ],
            "Edit": [
                BTN_USER_ADD,
                BTN_USER_EDIT,
                BTN_USER_DELETE,
                "---",
                BTN_USER_REFRESH,
            ],
            "View": [
                BTN_COMPANY,
                "---",
                BTN_TOGGLE_THEME,
                "---",
                BTN_SETTINGS,
            ],
            "Help": [
                # BTN_HELP,
                #  "---", BTN_SHOW_LOG,
                # "---",
                BTN_ABOUT,
            ],
        }
        self.master.option_add(pattern="*tearOff", value=False)
        menu_bar = tk.Menu(master=self.master)
        for key, val in menu_items.items():
            mnu = tk.Menu(master=self.master)
            for item in val:
                if item == "---":
                    mnu.add_separator()
                    continue
                mnu.add_command(
                    label=item, command=lambda a=item: self.on_action(action=a)
                )
            menu_bar.add_cascade(label=key, menu=mnu)
        self.master.configure(menu=menu_bar)

    def create_left_panel(self):
        left_panel_frm = ttk.Frame(master=self.body_frm, style="Card.TFrame")
        left_panel_frm.pack(side=tk.LEFT, fill=tk.Y)
        buttons_list = {
            BTN_IMPORT: "import",
            BTN_EXPORT: "export",
            BTN_COMPANY: "company",
            "---": "",
            BTN_USER_ADD: "user-add",
            BTN_USER_EDIT: "user-edit",
            BTN_USER_DELETE: "user-delete",
            BTN_USER_REFRESH: "refresh",
            "bottom": "",
            BTN_EXIT: "exit",
            BTN_SETTINGS: "settings",
        }
        _side = tk.TOP
        for key, val in buttons_list.items():
            if key == "---":
                sep = ttk.Separator(left_panel_frm, orient="horizontal")
                sep.pack(side=tk.TOP, fill=tk.X, pady=10)
                continue
            if key == "bottom":
                _side = tk.BOTTOM
                sep = ttk.Separator(left_panel_frm, orient="horizontal")
                sep.pack(side=tk.TOP, fill=tk.X, pady=10)
                continue
            btn = ttk.Button(
                master=left_panel_frm,
                text=key,
                image=val,
                compound=tk.TOP,
                command=lambda a=key: self.on_action(action=a),
                width=8,
            )
            btn.pack(side=_side, ipadx=5, ipady=5, padx=0, pady=1)
        sb = ttk.Separator(master=self.body_frm, orient=tk.VERTICAL)
        sb.pack(side=tk.LEFT, fill=tk.Y)

    def create_button_bar(self) -> None:
        pass

    def create_right_panel(self):
        right_panel_frm = ttk.Frame(self.body_frm, padding=5, border=1)
        right_panel_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        # Treeview
        tree_view_frm = ttk.Frame(master=right_panel_frm)
        tree_view_frm.pack(fill=tk.BOTH, expand=tk.YES)

        # Treeview fields
        self.fields_list = Distributor.model_json_schema(mode="serialization")[
            "properties"
        ]
        columns_list = [
            {
                "text": val.get("title", str(key).replace("_", " ").title()),
                "anchor": tk.W,
                "stretch": True,
            }
            for key, val in self.fields_list.items()
        ]

        self.treeview = Tableview(
            master=tree_view_frm,
            searchable=True,
            autoalign=True,
            pagesize=100,
            coldata=columns_list,
            paginated=True,
        )
        self.treeview.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        # Treeview bind
        self.treeview.view.bind(
            sequence="<<TreeviewSelect>>", func=self.treeview_select
        )
        self.treeview.view.bind(sequence="<<Focus>>", func=self.treeview_select)
        self.treeview.view.bind(sequence="<<Activate>>", func=self.treeview_select)
        self.treeview.view.bind(sequence="<<Backspace>>", func=self.show_user_delete)
        self.treeview.view.bind(sequence="<Double-1>", func=self.treeview_edit)

    def create_status_bar(self) -> None:
        """Create StatusBar frame."""
        status_bar_frm = ttk.Frame(master=self, border=1, height=50, relief=tk.SUNKEN)
        status_bar_frm.pack(fill=tk.X, side=tk.BOTTOM)
        lbl = ttk.Label(
            master=status_bar_frm,
            padding=5,
            textvariable=VAR_STATUS_BAR,
        )
        self.setvar(name=VAR_STATUS_BAR, value="Ready")
        lbl.pack(anchor=tk.W, fill=tk.X)

    # Actions
    def on_action(self, action: str, event=None) -> None:
        if action == BTN_EXIT:
            self.on_close()
        elif action == BTN_IMPORT:
            self.show_import()
        elif action == BTN_EXPORT:
            self.show_export()
        elif action == BTN_USER_ADD:
            self.show_user_add()
        elif action == BTN_USER_EDIT:
            self.show_user_edit()
        elif action == BTN_USER_DELETE:
            self.show_user_delete()
        elif action == BTN_USER_REFRESH:
            self.treeview_refresh()
        elif action == BTN_COMPANY:
            self.show_company()
        elif action == BTN_ABOUT:
            self.show_about()
        elif action == BTN_SETTINGS:
            self.show_settings()
        elif action == BTN_TOGGLE_THEME:
            self.toggle_theme()
        else:
            print(f"Action {action} not implemented yet!")

    def on_close(self):
        self.master.quit()

    # Treeview action
    def treeview_refresh(self) -> None:
        try:
            self.update_idletasks()
            _action = "Get all distributors from database"
            self.setvar(name=VAR_STATUS_BAR, value=_action)
            self.configure(cursor="wait")
            _distribution_list = self.controller.get_all_distributors()
            if _distribution_list is None or len(_distribution_list) == 0:
                self.configure(cursor="")
                msg = "No data found for distributors on database!"
                msg += (
                    f"\n\nClick on button [{BTN_IMPORT}] to import new distributors from excel file"
                    f" or click on menu item [{BTN_USER_ADD}] to add new distributor"
                )
                messagebox.showwarning(title=_action, message=msg, parent=self.master)
                return

            _action = "Add distributors data on treeview"
            _row_data = [
                list(
                    dict(
                        map(lambda k: (k, row[k] if row[k] else ""), self.fields_list)
                    ).values()
                )
                for row in _distribution_list
            ]

            self.treeview.delete_rows()
            self.treeview.insert_rows(index="end", rowdata=_row_data)
            self.treeview.load_table_data(clear_filters=True)
            self.treeview.focus_set()
            self.configure(cursor="")
            self.update_idletasks()
        except Exception as e:
            self.configure(cursor="")
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)

    def treeview_select(self, event=None) -> None:
        """Show info when user select something in treeview"""
        rec_from = (
            1 + (self.treeview._pageindex.get() - 1) * self.treeview._pagesize.get()
        )
        if self.treeview._pageindex.get() == self.treeview._pagelimit.get():
            if self.treeview.is_filtered:
                rec_to = len(self.treeview.tablerows_filtered)
            else:
                rec_to = len(self.treeview.tablerows)
        else:
            rec_to = (self.treeview._pageindex.get()) * self.treeview._pagesize.get()
        selected = len(self.treeview.view.selection())

        if self.treeview.is_filtered:
            total = len(self.treeview.tablerows_filtered)
            msg = f"Filtered record #{rec_from:,d}-{rec_to} of {total:,d}"
        else:
            total = len(self.treeview.tablerows)
            msg = f"Record #{rec_from:,d}-{rec_to:,d} of #{total:,d}"
        if selected > 1:
            msg += f" (Selected #{selected:,d} records)"
        self.setvar(name=VAR_STATUS_BAR, value=msg)

    def treeview_sort(self, column, descending):
        data = [
            (self.treeview.set(item, column), item)
            for item in self.treeview.get_children()
        ]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
            self.treeview.move(item=item, parent="", index=index)
        self.treeview.heading(
            column=column,
            command=lambda c=column: self.treeview_sort(
                column=c, descending=not descending
            ),
        )

    def treeview_edit(self, event):
        """On treeview double button"""
        self.on_action(action=BTN_USER_EDIT)

    # Show dialogs
    def show_import(self):
        try:
            _action = "Show dialog"
            _options = {"controller": self.controller}
            dlg = ImportDialog(parent=self.master, title=BTN_IMPORT, **_options)
            result = dlg.result
            if result:
                self.treeview_refresh()
        except Exception as e:
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)

    def show_export(self):
        try:
            _action = "Get years from Invoices on database"
            _years = self.controller.get_years_from_invoices()
            if len(_years) == 0:
                msg = "No valid Years found on database in table Invoices!"
                msg += f"\n\nTry to import Invoices with [{BTN_IMPORT}] button"
                messagebox.showwarning(
                    title=BTN_EXPORT,
                    message=msg,
                    parent=self.master,
                )
                return

            if self.settings is None:
                _action = "Get Settings from database"
                self._get_settings()

            _code_ente_prev = self.settings.get("code_ente_prev", EXPORT_CODE_ENTE_PREV)
            _denom_ente_prev = self.settings.get(
                "denom_ente_prev", EXPORT_DENOM_ENTE_PREV
            )

            _action = "Show dialog"
            _options = {
                "code_ente_prev": _code_ente_prev,
                "denom_ente_prev": _denom_ente_prev,
                "years": _years,
                "controller": self.controller,
            }
            ExportDialog(parent=self.master, title=BTN_EXPORT, **_options)
            self.treeview.focus_set()
        except Exception as e:
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)
            return

    def show_user_add(self):
        try:
            _action = "Show dialog"
            _args = {"image": "user-add", "model": Distributor}
            dlg = DistributorDialog(parent=self.master, title=BTN_USER_ADD, **_args)
            result = dlg.result
            if result:
                _action = "Insert distributor"
                record, _ = self.controller.update_distributor(record=result)
                values = list(
                    dict(
                        map(
                            lambda k: (k, record[k] if record[k] else ""),
                            self.fields_list,
                        )
                    ).values()
                )
                _item = self.treeview.insert_row(index="end", values=values)
                _iid = _item.iid
                id = record.get("id", 0)
                msg = f"{_action} success for id={id}"
                messagebox.showinfo(title=_action, message=msg, parent=self.master)

            self.treeview.focus_set()
        except Exception as e:
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)
            return

    def show_company(self):
        try:
            _action = "Get Company info from database"
            _data = self.controller.get_company()

            if _data is None:
                _data = DEFAULT_COMPANY

            _action = "Show dialog"
            _args = {"image": "company", "data": _data, "model": Company}
            dlg = CompanyDialog(parent=self.master, title=BTN_COMPANY, **_args)
            result = dlg.result
            if result:
                if result == _data:
                    return
                _action = "Update company on database"
                result, _ = self.controller.update_company(record=result)
                msg = MSG_SUCCESS_TEMPLATE.format(_action)
                messagebox.showinfo(title=_action, message=msg, parent=self.master)
            self.treeview.focus()
        except Exception as e:
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)
            return

    def show_user_edit(self):
        try:
            _selected = self.treeview.get_rows(selected=True)
            if not _selected or len(_selected) == 0:
                return
            id = _selected[0].values[0]
            _action = f"Get distributor from database: {id=}"
            distributor = self.controller.get_distributor_by_id(id)

            if distributor is None:
                msg = f"No distributor found on database for {id=}!"
                messagebox.showwarning(
                    title=BTN_USER_EDIT, message=msg, parent=self.master
                )
                return

            _action = "Show dialog"
            _args = {
                "image": "user-edit",
                "data": distributor,
                "model": Distributor,
            }
            dlg = DistributorDialog(parent=self.master, title=BTN_USER_EDIT, **_args)
            result = dlg.result
            if result:
                if result == distributor:
                    return

                _action = "Update distributor"
                record, _ = self.controller.update_distributor(record=result)
                values = list(
                    dict(
                        map(
                            lambda k: (k, record[k] if record[k] else ""),
                            self.fields_list,
                        )
                    ).values()
                )
                item = _selected[0]
                item.values = values
                item.refresh()
                msg = f"{_action} success for {id=}"
                messagebox.showinfo(title=_action, message=msg, parent=self.master)
            self.treeview.focus_set()
        except Exception as e:
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)

    def show_about(self) -> None:
        """Show about dialog"""
        try:
            _action = "Show about dialog"
            uname = platform.uname()
            title = f"About {__package__}"
            msg = (
                f"Name: {__package__}"
                f"\n\nVersion: {__version__}"
                f"\n\nAuthor: {__author__}: {__email__}"
                f"\n\n\nPython version: {platform.python_version()}"
                f"\nOS: {uname.system} {uname.release} v.{uname.version}"
                f"\nMachine: {uname.machine}"
            )
            messagebox.showinfo(title=title, message=msg, parent=self.master)
        except Exception as e:
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)

    def show_settings(self):
        try:
            if self.settings is None:
                _action = "Get Settings from database"
                self._get_settings()

            _action = "Show dialog"
            _args = {
                "image": "settings",
                "data": self.settings,
                "model": Setting,
            }
            dlg = SettingsDialog(parent=self.master, title=BTN_SETTINGS, **_args)
            result = dlg.result
            if result:
                if result == self.settings:
                    return
                _action = "Update settings on database"
                record, _ = self.controller.update_settings(record=result)
                self.settings = record
                msg = MSG_SUCCESS_TEMPLATE.format(_action)
                messagebox.showinfo(title=_action, message=msg, parent=self.master)
            self.treeview.focus_set()
        except Exception as e:
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)

    def show_user_delete(self):
        """Show user delete"""
        try:
            _selected = self.treeview.get_rows(selected=True)
            if not _selected or len(_selected) == 0:
                return

            _action = "Ask delete distributor"
            total = len(_selected)
            if total == 1:
                id = int(_selected[0].values[0])
                number = _selected[0].values[1]
                msg = f"Do you really want delete record with {id=} and {number=}?"
            else:
                msg = f"Do you really want delete all {total:d} selected records?"

            ask = messagebox.askyesno(
                title=_action, message=msg, parent=self, default="no"
            )
            if not ask:
                return

            _action = "Delete distributor"
            self.master.config(cursor="watch")
            _ids = [item.values[0] for item in _selected]
            _iids = [item.iid for item in _selected]
            self.controller.delete_distributor_by_id(ids=_ids)
            self.treeview.delete_rows(iids=_iids)
            self.master.config(cursor="")
            msg = MSG_SUCCESS_TEMPLATE.format(_action)
            messagebox.showinfo(title=_action, message=msg, parent=self.master)
            self.treeview.focus_set()
        except Exception as e:
            self.master.config(cursor="")
            msg = MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self.master)

    def toggle_theme(self) -> None:
        if sv_ttk.get_theme() == "dark":
            sv_ttk.use_light_theme()
        elif sv_ttk.get_theme() == "light":
            sv_ttk.use_dark_theme()
        else:
            print("Not Sun Valley theme")
            pass

    def _get_settings(self) -> None:
        if self.settings is None:
            _data = self.controller.get_settings()
            if _data is None:
                _data = DEFAULT_SETTINGS
            self.settings = _data


def main() -> None:
    """Main function"""
    root = tk.Tk()
    sv_ttk.set_theme(theme=darkdetect.theme(), root=root)
    root.title(f"{__package__} v.{__version__}")
    root.geometry("{}x{}".format(1000, 800))
    root.minsize(width=800, height=800)
    root.iconbitmap(bitmap=os.path.join(RES_PATH, "main.ico"))
    MainApp(master=root)
    root.mainloop()


if __name__ == "__main__":
    main()
