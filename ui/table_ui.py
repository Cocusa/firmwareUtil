import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip


class ControlProcessTable(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        super().configure(bootstyle="dark")
        super().columnconfigure(0, weight=30, minsize=100)
        super().columnconfigure(1, weight=10, minsize=100)
        # scroll_cf.add(output_container, textvariable='scroll-message')
        self.rows: dict[int, list[ttk.Label]] = {}

    def add(self, key, *rows_data):
        self.rows[key] = []
        row_index = len(self.rows)

        for i, data in enumerate(rows_data):
            filed = ttk.Label(self, text=data, bootstyle="default")
            filed.grid(
                row=row_index, column=i, sticky="ew", pady=1, padx=1, columnspan=1
            )
            self.rows[key].insert(1, filed)

    def clear(self):
        for row in self.rows.values():
            for cell in row:
                cell.destroy()

        self.rows.clear()

    def change_bootstyle(self, key: str, bootstyle: str):
        for cell in self.rows[key]:
            cell.configure(bootstyle=bootstyle)

        self.update()

    def change_tooltip(self, key: str, text: str):
        for cell in self.rows[key]:
            ToolTip(cell, text=text)

        self.update()

    def change_text(self, key: str, field_index: int, text: str):
        self.rows[key][field_index].configure(text=text)
        self.update()
