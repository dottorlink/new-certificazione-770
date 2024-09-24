# -*- coding: utf-8 -*-
"""
_Description_
"""
# Built-in/Generic Imports

# Libs
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.simpledialog import Dialog

# Modules
from tkcalendar import DateEntry

# Own modules

# Constants


class BaseDialog(Dialog):
    def __init__(self, parent=None, title="", **kwargs):
        self._title = title
        self._args = kwargs
        super().__init__(parent=parent, title=title)

    def headerbox(self, master, default: str) -> None:
        frm = ttk.Frame(master=master, padding=10)
        frm.pack(side=tk.TOP, fill=tk.X, expand=1)
        lbl = tk.Label(
            master=frm,
            text=self._title,
            font=("TkCaptionFont", 14, "bold"),
        )
        lbl.pack(side=tk.LEFT, expand=1, fill=tk.X)
        lbl = tk.Label(
            master=frm,
            text="",
            image=self._args.get("image", default),
            compound=tk.LEFT,
        )
        lbl.pack(side=tk.LEFT)

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

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind(sequence="<Escape>", func=self.cancel)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        ttk.Separator(self).pack(fill=tk.X)
        box.pack(side=tk.BOTTOM)

    def entry_by_fields(self, master, fields_list, options_dict=None):
        for key, val in fields_list.items():
            _ent = None
            _var = None
            _txt = val.get("title", str(key).replace("_", " ").title())

            field_type, is_nullable, has_default, default_value, constraints = (
                extract_field_metadata(val)
            )
            field_options = {"required": not is_nullable and not has_default}
            field_options.update(constraints)
            if has_default and default_value is not None:
                field_options["initial"] = default_value

            lbl = ttk.Label(master=master, text=_txt)
            lbl.pack(side=tk.TOP, expand=1, fill=tk.X)
            if options_dict and key in options_dict:
                # Ensure the choices are in list of 2-tuples BC THAT IS HOW DJANGO WANTS IT
                choices = options_dict[key]
                _var = tk.StringVar(self, name=key)
                _ent = ttk.Combobox(
                    master=master,
                    textvariable=_var,
                    values=choices,
                    state="readonly",
                )
            elif field_type in ["date", "date-time", "date-time"]:
                _var = tk.StringVar(self, name=key)
                _ent = DateEntry(
                    master=master,
                    selectmode="day",
                    date_pattern="yyyy-MM-dd",
                    locale="it_IT",
                    textvariable=_var,
                )
            elif field_type in ["number", "integer"]:
                _var = tk.IntVar(self, name=key)
                _ent = ttk.Entry(master=master, textvariable=_var)
            elif field_type == "boolean":
                _var = tk.BooleanVar(self, name=key)
                _ent = ttk.Entry(master=master, textvariable=_var)
            else:
                _var = tk.StringVar(self, name=key)
                _ent = ttk.Entry(master=master, textvariable=_var)

            _ent.pack(side=tk.TOP, expand=1, fill=tk.X, padx=(0, 5), pady=(0, 5))

            if key == "id":
                _ent.config(state="readonly")

            if field_options.get("required", False):
                add_validation(widget=_ent, func=validate_required_text)

            if field_options.get("initial", None):
                self.setvar(name=key, value=field_options.get("initial"))

    def validate(self) -> bool:
        data = {}
        self.result = None
        for key in self.fields_list.keys():
            try:
                data[key] = self.getvar(name=key)
            except Exception:
                pass

        try:
            model = self._args.get("model", None)
            if model:
                record = model.model_validate(obj=data, from_attributes=True)
                self.result = record.model_dump(exclude={"created_at", "updated_at"})
            return True
        except Exception as e:
            msg = "Invalid data!\nError:"
            if e.errors:
                for err in e.errors():
                    msg += f"\n - Field {err.get("loc")[0]} is {err.get("type")}: {err.get("msg")}"
            msg += "\n\nControl field values and retry"
            messagebox.showerror(title="Validate data", message=msg, parent=self)
            self.result = None
            return False


def extract_field_metadata(property_info):
    """
    class Model:
      date: Optional[Union[datetime, str]] = Field(None)

    property_info = {
      'anyOf': [{
        'format': 'date-time', 'type': 'string'}, # format can be different from type
        {'type': 'string'},
        {'type': 'null'},
      }],
      'default': None,
      'title': 'Date'
    }
    """
    # Initialize default values
    is_nullable = False
    has_default = "default" in property_info
    default_value = property_info.get("default", None)
    field_type = None
    constraints = {}

    # 'anyOf' is property generated by fields with input Union[[type1, type2]] or Optional[type1]
    if "anyOf" in property_info:
        field_type, is_nullable, constraints = handle_anyof_structure(
            property_info["anyOf"]
        )
    else:
        field_type = property_info.get("type")
        if property_info.get("format") in ["date", "date-time"]:
            field_type = property_info.get("format")
        is_nullable = field_type == "null"

    return field_type, is_nullable, has_default, default_value, constraints


def handle_anyof_structure(anyof_options):
    """
    If 'anyOf' is in property_info, use this func. Property is generated by fields with input Union[[type1, type2]] or Optional[type1]
    """
    type_priority = ["date-time", "string", "number", "date", "integer"]
    constraints = {}
    field_type = None
    is_nullable = any("null" in option.get("type", "") for option in anyof_options)

    for option in anyof_options:
        option_type, option_format = option.get("type"), option.get("format", None)

        # if format is date but type string, update type to date
        if option_type == "string" and option_format == "date-time":
            field_type = "date-time"
            break
        if option_type == "string" and option_format == "date":
            field_type = "date"
            break
        elif option_type in type_priority:
            field_type = option_type
            break

    for option in anyof_options:
        if option.get("type") != "null":
            # Extract constraints like 'minimum', 'maximum', 'minLength', and 'maxLength' (from pydantic anyOf)
            constraints.update(
                {
                    "min_length": option.get("minLength"),
                    "max_length": option.get("maxLength"),
                    "min_value": option.get("minimum"),
                    "max_value": option.get("maximum"),
                }
            )

    return field_type, is_nullable, constraints


def add_validation(widget, func, when="focusout", **kwargs):
    """Adds validation to the widget of type `Entry`, `Combobox`, or
    `Spinbox`. The func should accept a parameter of type
    `ValidationEvent` and should return a boolean value.

    Parameters:

        widget (Widget):
            The widget on which validation will be applied.

        func (Callable):
            The function that will be called when a validation event
            occurs.

        when (str):
            Indicates when the validation event should occur. Possible
            values include:

            * focus - whenever the widget gets or loses focus
            * focusin - whenever the widget gets focus
            * focusout - whenever the widget loses focus
            * key - whenever a key is pressed
            * all - validate in all of the above situations

        kwargs (Dict):
            Optional arguments passed to the callback.
    """
    f = widget.register(lambda *e: func(*e, **kwargs))
    subs = (r"%d", r"%i", r"%P", r"%s", r"%S", r"%v", r"%V", r"%W")
    widget.configure(validate=when, validatecommand=(f, *subs))


def validate_required_text(d, i, P, s, S, v, V, W) -> bool:
    if len(P) > 0:
        return True
    else:
        return False
