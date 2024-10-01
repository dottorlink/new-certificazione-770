# -*- coding: utf-8 -*-
"""
About dialog

@File: about.py
@Date: 2024-08-14
"""

# Built-in/Generic Imports
import pathlib
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

# Owned modules
from .dialog import BaseDialog


class AboutDialog(BaseDialog):
    """About Me popup widow to display general application description"""

    def __init__(self, parent=None, title="", **kwargs):
        super().__init__(parent=parent, title=title, **kwargs)

    def body(self, master):
        """Body

        Args:
            master (_type_): _description_
        """
        # image and application name
        self.resizable(0, 0)
        frm = ttk.Frame(master)

        image = self._args.get("image", "logo")
        lbl = ttk.Label(frm, image=image, anchor=tk.W)
        lbl.pack(side=tk.LEFT, padx=(15, 5), pady=5)
        app_name = self._args.get("app_name", "Application")
        lbl = ttk.Label(frm, text=app_name, font=("TkCaptionFont", 10, "bold"))
        lbl.pack(side=tk.LEFT, padx=(5, 15), pady=5)
        frm.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)

        text = self._args.get("author", "Author")
        lbl = ttk.Label(master, text=text)
        lbl.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        text = self._args.get("copyright", "Copyright")
        lbl = ttk.Label(master, text=text)
        lbl.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        # description
        description = self._args.get("description", None)
        if description:
            sep = ttk.Separator(master, orient=tk.HORIZONTAL)
            sep.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X, expand=tk.YES)
            lbl = ttk.Label(master, text=description, anchor=tk.W)
            lbl.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

        # license text widget
        license_file = self._args.get("license_file", None)
        if license_file:
            sep = ttk.Separator(master, orient=tk.HORIZONTAL)
            sep.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X, expand=tk.YES)
            frm = ttk.Frame(master)
            self.text = ScrolledText(frm, wrap="word", width=50, height=10)
            mylicense = pathlib.Path(license_file).read_text()
            self.text.insert(tk.END, mylicense)
            # pack widgets to window
            self.text.pack(side=tk.TOP, padx=(15, 0), pady=10, ipadx=10, ipady=10)
            # make text widget 'read-only'
            self.text.configure(state=tk.DISABLED)
            frm.pack(pady=(0, 0), fill=tk.X, expand=tk.YES)

    def buttonbox(self):
        """Create the dialog button box.

        This method should be overridden and is called by the `build`
        method. Set the `self._initial_focus` for the button that
        should receive the initial focus.

        Parameters:

            master (Widget):
                The parent widget.
        """
        box = ttk.Frame(master=self)

        w = ttk.Button(box, text="OK", width=10, command=self.cancel, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind(sequence="<Escape>", func=self.cancel)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        ttk.Separator(self).pack(fill=tk.X)
        box.pack(side=tk.BOTTOM)


class TestWindow(tk.Tk):
    """A window used for testing the various module dialogs"""

    def __init__(self):
        super().__init__()
        self.title("Testing Window")
        self.text = tk.Text(self)
        self.text.pack(fill=tk.BOTH, expand=tk.YES)
        self.text.insert(tk.END, "This is a test. This is only a test.")


if __name__ == "__main__":
    w = TestWindow()
    AboutDialog(w)
    w.mainloop()
