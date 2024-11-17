import tkinter as tk
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from setup import tmdb_api_key

from FileFin import FileFin

if __name__ == "__main__":
    root = tk.Tk()
    app = FileFin(root, tmdb_api_key)
    app.setup_ui()
    root.mainloop()