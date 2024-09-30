# -*- coding: utf-8 -*-
"""
Main module

@File: main.py
@Date: 2024-08-14
"""

# Built-in/Generic Imports

# Libs
import logging
import logging.config
import os
import platform
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# Modules
import darkdetect
import pywinstyles
import sv_ttk

# OWN Modules
try:
    import config as config
    import controllers as controllers
    import helpers as helpers
    import models as models
    import views as views
except:  # noqa: E722
    import new_certificazione_770.config as config
    import new_certificazione_770.controllers as controllers
    import new_certificazione_770.helpers as helpers
    import new_certificazione_770.models as models
    import new_certificazione_770.views as views


# Constants
EXE_PATH = helpers.executable_path()
RES_PATH = helpers.resource_path()

# Button Constants
BTN_ABOUT = f"About {config.PACKAGE}"
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


class MainWindow(ttk.Frame):
    """Main Tk Window

    Args:
        tk (_type_): _description_
    """

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master=master, *args, **kwargs)
        self.master = master
        self.pack(fill=tk.BOTH, expand=tk.YES)

        self.version = config.VERSION

        self.controller: controllers.Controller = None
        self.settings: dict = None

        try:
            _action = "Load images from assets folders"
            logging.debug(msg=_action)
            self._load_images()

            _action = "Draw application"
            logging.debug(msg=_action)
            self.create_menu_bar(master=self.master)
            self.create_status_bar()
            self.create_button_bar()
            self.create_left_panel()
            self.create_right_panel()

        except Exception as e:
            logging.exception(msg=_action)
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)
            self.master.on_close()
            return

        self.after(ms=200, func=self._initialize)

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
                db_path = os.path.join(EXE_PATH, f"{config.PACKAGE}.db")
                _action = f"Open/create database: {db_path=}"
                logging.debug(msg=_action)
                self.controller = controllers.Controller(db_path=db_path, echo=False)

            if self.settings is None:
                self.settings = self._get_settings()

            _action = "Refresh treeview"
            logging.debug(msg=_action)
            self.treeview_refresh()
        except Exception as e:
            logging.exception(msg=_action)
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)
            self.master.on_close()

    def create_menu_bar(self, master) -> None:
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
        master.option_add(pattern="*tearOff", value=False)
        menu_bar = tk.Menu(master=master)
        for key, val in menu_items.items():
            mnu = tk.Menu(menu_bar, tearoff=0)
            for item in val:
                if item == "---":
                    mnu.add_separator()
                    continue
                mnu.add_command(
                    label=item, command=lambda a=item: self.on_action(action=a)
                )
            menu_bar.add_cascade(label=key, menu=mnu)
        master.configure(menu=menu_bar)

    def create_left_panel(self):
        left_panel_frm = ttk.Frame(master=self, style="Card.TFrame")
        left_panel_frm.pack(side=tk.LEFT, fill=tk.Y)

        lbl = ttk.Label(master=left_panel_frm, image="logo-small", anchor="center")
        lbl.pack(side=tk.TOP, fill=tk.X, pady=5)

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
        sb = ttk.Separator(master=self, orient=tk.VERTICAL)
        sb.pack(side=tk.LEFT, fill=tk.Y)

    def create_button_bar(self) -> None:
        pass

    def create_right_panel(self):
        right_panel_frm = ttk.Frame(self, padding=5, border=1)
        right_panel_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        # Treeview
        tree_view_frm = ttk.Frame(master=right_panel_frm)
        tree_view_frm.pack(fill=tk.BOTH, expand=tk.YES)

        # Treeview fields
        self.fields_list = models.Distributor.model_json_schema(mode="serialization")[
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

        self.treeview = views.Tableview(
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
        self.treeview.view.bind(sequence="<ButtonRelease-1>", func=self.treeview_select)
        self.treeview.view.bind(sequence="<Double-1>", func=self.treeview_edit)

    def create_status_bar(self) -> None:
        """Create StatusBar frame."""
        status_bar_frm = ttk.Frame(master=self, border=1, height=50, relief=tk.GROOVE)
        status_bar_frm.pack(fill=tk.X, side=tk.BOTTOM)
        lbl = ttk.Label(
            master=status_bar_frm,
            padding=5,
            relief=tk.GROOVE,
            textvariable=VAR_STATUS_BAR,
        )
        self.setvar(name=VAR_STATUS_BAR, value="Ready")
        lbl.pack(anchor=tk.W, fill=tk.X)

    # Actions
    def on_action(self, action: str, event=None) -> None:
        if action == BTN_EXIT:
            self.master.on_close()
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
            _action = f"Action {action} not implemented yet!"
            # print(_action)
            logging.warning(msg=_action)

    # Treeview action
    def treeview_refresh(self) -> None:
        try:
            self.update_idletasks()
            _action = "Get all distributors from database"
            logging.debug(msg=_action)
            self.setvar(name=VAR_STATUS_BAR, value=_action)
            self.configure(cursor="wait")
            _distribution_list = self.controller.get_all_distributors()
            if _distribution_list is None or len(_distribution_list) == 0:
                self.configure(cursor="")
                msg = "No data found for distributors on database!"
                logging.warning(msg=msg)
                msg += (
                    f"\n\nClick on button [{BTN_IMPORT}] to import new distributors from excel file"
                    f" or click on menu item [{BTN_USER_ADD}] to add new distributor"
                )
                messagebox.showwarning(title=_action, message=msg, parent=self)
                return

            msg = (
                helpers.MSG_SUCCESS_TEMPLATE.format(_action)
                + f": records={len(_distribution_list):,d}"
            )
            logging.info(msg=msg)

            _action = "Add distributors data on treeview"
            logging.debug(msg=_action)
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
            logging.exception(msg=_action)
            self.configure(cursor="")
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)

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

    def treeview_edit(self, event):
        """On treeview double button"""
        self.on_action(action=BTN_USER_EDIT)

    # Show dialogs
    def show_import(self):
        """Show import dialog"""
        try:
            _action = "Show Import dialog"
            logging.debug(msg=_action)
            _options = {"controller": self.controller}
            dlg = views.ImportDialog(parent=self, title=BTN_IMPORT, **_options)
            result = dlg.result
            if result:
                self.treeview_refresh()
        except Exception as e:
            logging.exception(msg=_action)
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)

    def show_export(self):
        """Show Export dialog"""
        try:
            if self.settings is None:
                self.settings = self._get_settings()

            _action = "Get years from Invoices on database"
            logging.debug(msg=_action)
            years = self.controller.get_years_from_invoices()
            if len(years) == 0:
                msg = "No valid Years found on database in table Invoices!"
                logging.warning(msg=msg)
                msg += f"\n\nTry to import Invoices with [{BTN_IMPORT}] button"
                messagebox.showwarning(
                    title=BTN_EXPORT,
                    message=msg,
                    parent=self,
                )
                return

            _code_ente_prev = (
                self.get_setting_value("code_ente_prev")
                or helpers.EXPORT_CODE_ENTE_PREV
            )
            _denom_ente_prev = (
                self.get_setting_value("denom_ente_prev")
                or helpers.EXPORT_DENOM_ENTE_PREV
            )

            _code_somme_non_sogg = (
                self.get_setting_value("code_somme_non_sogg")
                or helpers.EXPORT_CODE_SOMME_NON_SOGG
            )

            _action = "Show Export dialog"
            logging.info(msg=f"{_action}: {years=}")
            _options = {
                "code_ente_prev": _code_ente_prev,
                "denom_ente_prev": _denom_ente_prev,
                "code_somme_non_sogg": _code_somme_non_sogg,
                "years": years,
                "controller": self.controller,
            }
            views.ExportDialog(parent=self, title=BTN_EXPORT, **_options)
            self.treeview.focus_set()
        except Exception as e:
            logging.exception(msg=_action)
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)
            return

    def show_user_add(self):
        """Show Distributor dialog for adding user"""
        try:
            _action = "Show Distributor dialog"
            logging.debug(msg=_action)
            _args = {"image": "user-add", "model": models.Distributor}
            dlg = views.DistributorDialog(parent=self, title=BTN_USER_ADD, **_args)
            result = dlg.result
            if result:
                _action = "Insert distributor"
                logging.debug(msg=f"{_action}: {result=}")
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
                msg = helpers.MSG_SUCCESS_TEMPLATE.format(_action) + f" for {id=}"
                logging.info(msg=msg)
                messagebox.showinfo(title=_action, message=msg, parent=self)

            self.treeview.focus_set()
        except Exception as e:
            logging.exception(msg=_action)
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)
            return

    def show_company(self):
        """Show Company dialog"""
        try:
            _action = "Get Company info from database"
            logging.debug(msg=_action)
            data = self.controller.get_company()
            if data is None:
                logging.warning(msg=f"{_action}: no data found, setting default")
                data = helpers.DEFAULT_COMPANY

            _action = "Show Company dialog"
            logging.debug(msg=f"{_action}: {data=}")
            _args = {"image": "company", "data": data, "model": models.Company}
            dlg = views.CompanyDialog(parent=self, title=BTN_COMPANY, **_args)
            result = dlg.result
            if result:
                if result == data:
                    logging.warning(f"{_action}: no change")
                    return

                _action = "Update company on database"
                logging.debug(msg=f"{_action}: {result=}")
                result, _ = self.controller.update_company(record=result)
                msg = (
                    helpers.MSG_SUCCESS_TEMPLATE.format(_action)
                    + f" for id={result.get("id")}"
                )
                logging.info(msg=msg)
                messagebox.showinfo(title=_action, message=msg, parent=self)
            self.treeview.focus()
        except Exception as e:
            logging.exception(msg=_action)
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)
            return

    def show_user_edit(self):
        """Show Distributor dialog for edit user"""
        try:
            _selected = self.treeview.get_rows(selected=True)
            if not _selected or len(_selected) == 0:
                return
            id = _selected[0].values[0]
            _action = "Get distributor from database"
            logging.debug(msg=f"{_action}: {id=}")
            data = self.controller.get_distributor_by_id(id)

            if data is None:
                msg = f"No distributor found on database for {id=}!"
                logging.warning(msg=msg)
                messagebox.showwarning(title=BTN_USER_EDIT, message=msg, parent=self)
                return

            _action = "Show Distributor dialog"
            logging.debug(msg=f"{_action}: {data=}")
            _args = {
                "image": "user-edit",
                "data": data,
                "model": models.Distributor,
            }
            dlg = views.DistributorDialog(parent=self, title=BTN_USER_EDIT, **_args)
            result = dlg.result
            if result:
                if result == data:
                    logging.warning(f"{_action}: no change")
                    return

                _action = "Update distributor"
                logging.debug(msg=f"{_action}: {result=}")
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
                msg = helpers.MSG_SUCCESS_TEMPLATE.format(_action) + f" for {id=}"
                logging.info(msg=msg)
                messagebox.showinfo(title=_action, message=msg, parent=self)
            self.treeview.focus_set()
        except Exception as e:
            logging.exception(msg=_action)
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)

    def show_about(self) -> None:
        """Show About dialog"""
        try:
            _action = "Show About dialog"
            logging.debug(msg=_action)

            uname = platform.uname()
            _msg = (
                f"\nAuthor: {config.AUTHOR} <{config.EMAIL}>"
                f"\nCopyright: {config.COPYRIGHT}"
                # f"\nDescription:\n{description}"
                f"\n{"-" * 20}"
                f"\nPython version: {platform.python_version()}"
                f"\nOS: {uname.system} {uname.release} v.{uname.version}"
                f"\nMachine: {uname.machine}"
            )

            # Add file LICENSE.txt exist control
            if os.path.exists(os.path.join(EXE_PATH, config.LICENSE_FILE_NAME)):
                _license_file = os.path.join(EXE_PATH, config.LICENSE_FILE_NAME)
            else:
                _license_file = None

            _args = {
                "image": "logo-small",
                "app_name": f"{config.PACKAGE} v{config.VERSION}",
                "description": _msg,
                "license_file": _license_file,
            }
            views.AboutDialog(parent=self, title=f"About {config.PACKAGE}", **_args)
        except Exception as e:
            logging.exception(msg=_action)
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)

    def show_settings(self):
        """Show Settings dialog"""
        try:
            if self.settings is None:
                self.settings = self._get_settings()

            data = self.settings
            _action = "Show Settings dialog"
            logging.debug(msg=f"{_action}: {data=}")
            _args = {"image": "settings", "settings": data, "model": models.Setting}
            dlg = views.SettingsDialog(parent=self, title=BTN_SETTINGS, **_args)
            result = dlg.result
            if result:
                # if result == data
                #     logging.warning(f"{_action}: no change")
                #     return

                _action = "Update settings on database"
                for value in result:
                    record, _ = self.controller.update_settings(record=value)
                logging.debug(msg=f"{_action}: {result=}")
                self.settings = result
                msg = helpers.MSG_SUCCESS_TEMPLATE.format(_action)
                logging.info(msg=msg)
                messagebox.showinfo(title=_action, message=msg, parent=self)
            self.treeview.focus_set()
        except Exception as e:
            logging.exception(msg=_action)
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)

    def show_user_delete(self):
        """Show user delete"""
        try:
            _selected = self.treeview.get_rows(selected=True)
            if not _selected or len(_selected) == 0:
                return

            _action = "Ask delete distributor"
            total = len(_selected)
            logging.debug(msg=f"{_action}: {total=}")
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
                logging.debug(msg=f"{_action} cancelled by user")
                return

            # Delete distributor
            _action = "Delete distributor"
            self.config(cursor="watch")
            ids = [item.values[0] for item in _selected]
            iids = [item.iid for item in _selected]
            logging.debug(msg=f"{_action}: {ids=}")

            self.controller.delete_distributor_by_id(ids=ids)
            self.treeview.delete_rows(iids=iids)
            self.config(cursor="")
            msg = helpers.MSG_SUCCESS_TEMPLATE.format(_action) + f" for {ids}"
            logging.info(msg=msg)
            messagebox.showinfo(title=_action, message=msg, parent=self)
            self.treeview.focus_set()
        except Exception as e:
            logging.exception(msg=_action)
            self.config(cursor="")
            msg = helpers.MSG_ERROR_TEMPLATE.format(_action, e)
            messagebox.showerror(title=_action, message=msg, parent=self)

    def toggle_theme(self) -> None:
        if sv_ttk.get_theme() == "dark":
            sv_ttk.use_light_theme()
            apply_theme_to_titlebar(self)
            msg = "Set light theme"
            logging.debug(msg=msg)
        elif sv_ttk.get_theme() == "light":
            sv_ttk.use_dark_theme()
            apply_theme_to_titlebar(self)
            msg = "Set dark theme"
            logging.debug(msg=msg)
        else:
            msg = "Not Sun Valley theme"
            logging.warning(msg=msg)

    def _get_settings(self) -> dict:
        _action = "Get Settings from database"
        logging.debug(msg=_action)
        data = self.controller.get_settings()
        if data is None:
            logging.warning(msg=f"{_action}: no data found, setting default")
            data = helpers.DEFAULT_SETTINGS
        logging.info(msg=f"{_action}: {data=}")
        return data

    def get_setting_value(self, name) -> str:
        if self.settings is None:
            self.settings = self._get_settings()

        for item in self.settings:
            if item["name"] == name:
                return str(item["value"])

        return None


def apply_theme_to_titlebar(window):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(
            window, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa"
        )
    elif version.major == 10:
        pywinstyles.apply_style(
            window, "dark" if sv_ttk.get_theme() == "dark" else "normal"
        )

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        window.wm_attributes("-alpha", 0.99)
        window.wm_attributes("-alpha", 1)


class MyApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sv_ttk.set_theme(theme=darkdetect.theme(), root=self)
        self.title(f"{config.PACKAGE} v.{config.VERSION}")
        self.geometry("{}x{}".format(1000, 800))
        self.minsize(width=800, height=800)
        self.iconbitmap(bitmap=os.path.join(RES_PATH, "assets", "main.ico"))
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", func=self.on_close)
        self.mainView = MainWindow(master=self)
        self.deiconify()

    def on_close(self):
        # self.destroy()
        self.quit()


def main() -> None:
    """Main function"""
    logging.config.dictConfig(config.LOGGING_CONFIG)
    logging.info(msg="-" * 50)
    logging.info(msg="Start application")
    if helpers.instance_check(config.PACKAGE):
        app = MyApplication()
        # apply_theme_to_titlebar(window=application)
        app.mainloop()
        logging.info("End application")
    else:
        logging.warning("Application is yet running")
        sys.exit(0)

    logging.info(msg="-" * 50)


if __name__ == "__main__":
    main()
