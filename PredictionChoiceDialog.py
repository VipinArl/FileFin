import tkinter as tk

class PredictionChoiceDialog:
    def __init__(self, parent, predictions):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title("Choose Prediction")
        
        listbox = tk.Listbox(dialog, width=50)
        listbox.pack(padx=5, pady=5)
        
        for pred in predictions:
            listbox.insert(tk.END, pred['title'])
        
        def save():
            selection = listbox.curselection()
            if selection:
                self.result = predictions[selection[0]]['title']
            dialog.destroy()

        def select(event):
            save()
        
        listbox.bind('<Double-Button-1>', select)
        tk.ttk.Button(dialog, text="Choose", command=save).pack(pady=5)
        
        dialog.transient(parent)
        dialog.grab_set()
        parent.wait_window(dialog)