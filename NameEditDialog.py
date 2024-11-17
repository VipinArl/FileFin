import tkinter as tk
from tkinter import ttk


class NameEditDialog:
    def __init__(self, parent, current_names):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Name")
        
        ttk.Label(self.dialog, text="Enter new name:").pack(padx=5, pady=5)
        
        self.entry = ttk.Entry(self.dialog, width=50)
        self.entry.pack(padx=5, pady=5)

        ttk.Label(self.dialog, text="Current Names:").pack(padx=5, pady=5)

        self.listbox = tk.Listbox(self.dialog, width=50)
        self.listbox.pack(padx=5, pady=5)

        for name in current_names:
            self.listbox.insert(tk.END, name)
        
        self.listbox.bind('<Double-Button-1>', self.select)
        
        ttk.Button(self.dialog, text="Save", command=self.save).pack(pady=5)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)

    def save(self):
        self.result = self.entry.get()
        self.dialog.destroy()

    def select(self, _):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.listbox.get(self.listbox.curselection()))
        