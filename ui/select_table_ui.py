import tkinter as tk
from tkinter import ttk

class TableWindow(tk.Toplevel):
    def __init__(self, parent, objects, fields, fields_name: list[str], title):
        super().__init__(parent)
        self.objects = objects
        self.fields = fields
        self.parent = parent
        self.selected_obj = None
        self.title(title)
        self.geometry("400x500")
        self.minsize(300, 400)

        # Create a frame for the treeview
        self.treeview_frame = ttk.Frame(self)
        self.treeview_frame.pack(fill=tk.BOTH, expand=True)

        # Create a treeview in the frame
        self.treeview = ttk.Treeview(self.treeview_frame)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Set the font size to 15 and row height to accommodate it
        style = ttk.Style(self)
        style.configure("Treeview", font=("TkDefaultFont", 15), rowheight=30)

        # Create columns
        self.treeview["columns"] = fields
        self.treeview.column("#0", width=0, stretch=tk.NO)
        for field in fields:
            self.treeview.column(field, width=100)

        # Create headers
        for i, field in enumerate(fields):
            self.treeview.heading(field, text=fields_name[i])

        # Add rows
        for obj in objects:
            values = [getattr(obj, field) for field in fields]
            self.treeview.insert("", "end", values=values, tags=(str(id(obj)),))

        # Create a frame for the buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill=tk.X)

        # Create OK button
        self.ok_button = ttk.Button(self.buttons_frame, text="OK", command=self.on_ok, state='disabled')
        self.ok_button.pack(side=tk.RIGHT)

        # Create Cancel button
        cancel_button = ttk.Button(self.buttons_frame, text="Отмена", command=self.on_cancel)
        cancel_button.pack(side=tk.RIGHT)

        # Update OK button state when a row is selected
        self.treeview.bind('<<TreeviewSelect>>', self.update_ok_button_state)

    def update_ok_button_state(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            self.ok_button['state'] = 'normal'
        else:
            self.ok_button['state'] = 'disabled'

    def on_ok(self):
        selected_item = self.treeview.selection()
        if selected_item:
            selected_item = selected_item[0]
            self.selected_obj = next(obj for obj in self.objects if str(id(obj)) in self.treeview.item(selected_item, 'tags'))
        self.destroy()

    def on_cancel(self):
        self.destroy()
