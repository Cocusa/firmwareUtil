import ttkbootstrap as ttk
from ttkbootstrap.constants import END


class Output(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)

        self.text_area = ttk.ScrolledText(self)
        self.text_area.configure(state="disabled")
        self.text_area.pack(fill="both", expand=True)
        # scroll_cf.add(output_container, textvariable='scroll-message')
        self.update()

    def next(self, text, tag=None):
        self.text_area.configure(state="normal")
        self.text_area.insert(ttk.INSERT, text + "\n\n", tag)
        self.text_area.configure(state="disabled")
        self.update()

    def clear(self):
        self.text_area.configure(state="normal")
        self.text_area.delete(1.0, END)
        self.text_area.configure(state="disabled")
        self.update()

    def text(self) -> str:
        return str(self.text_area.get("1.0", END))

    def set_tag(self, tag: str, **args):
        self.text_area.tag_config(tag, **args)


class SerialNumberEntry(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)

        validate_sn_func = self.register(self.validate_serial_number)

        ttk.Label(self, text="Серийный номер").pack(expand=True)
        self.input_frame = ttk.Frame(self)
        self.sn_entry = ttk.Entry(
            self.input_frame, validate="focus", validatecommand=(validate_sn_func, "%P")
        )
        self.sn_start_button = ttk.Button(self.input_frame, text="Начать")

        self.sn_start_button.pack(side="right")
        self.sn_entry.pack(padx=10, pady=10, expand=True, side="top")
        self.input_frame.pack(side="top")

    def validate_serial_number(self=None, x=None) -> bool:
        """Validates serial number"""
        return False

    def get(self) -> str:
        return self.sn_entry.get()

    def on_enter(self, func):
        self.sn_entry.bind("<Return>", func)
        self.sn_start_button.bind("<Button-1>", func)

    def set_focus(self):
        self.sn_entry.selection_range(0, END)
        self.sn_entry.focus_set()
