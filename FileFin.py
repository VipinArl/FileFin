import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import requests
import re
import threading
import sys
import importlib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from NameEditDialog import NameEditDialog
from PredictionChoiceDialog import PredictionChoiceDialog
from PatternsEditDialog import PatternsEditDialog

class FileFin:
    def __init__(self, root, api_key):
        self.root = root
        self.root.title("FileFin")
        self.root.geometry("1200x800")
        self.root.iconbitmap("FileFin.ico")
        
        # API configuration
        self.tmdb_api_key = api_key
        self.tmdb_base_url = "https://api.themoviedb.org/3"
        
        self.file_predictions = {}  # Store predictions for each file
        self.selected_names = {}    # Store user-selected names for files
        
        self.thread = None
        self.stop_prediction_flag = threading.Event()

        # Define colors for different prediction states
        self.colors = {
            'proper_prediction': '#E8F5E9',  # Light green for single prediction
            'multiple_predictions': '#FFF3E0',  # Light orange for multiple predictions
            'no_prediction': '#FFEBEE'  # Light red for no prediction
        }
        
    def setup_ui(self):
        # Main toolbar
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(self.toolbar, text="Select Folder", 
                    command=self.select_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Predict Names", 
                    command=self.predict_all_names).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Fix Names", 
                    command=self.apply_all_names).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Edit Patterns",
                    command=self.edit_patterns).pack(side=tk.LEFT, padx=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.toolbar, variable=self.progress_var, 
                                      maximum=100, length=200)
        self.progress.pack(side=tk.LEFT, padx=5)

        canvas = tk.Canvas(self.toolbar, width=20, height=20)
        canvas.pack(side=tk.LEFT, padx=5)
        circle = canvas.create_oval(2, 2, 19, 19, fill='red')
        canvas.create_text(10, 10, text='X', fill='white', font=('Arial', 12))
        canvas.bind("<Button-1>", lambda event: self.stop_prediction_flag.set())
        
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Style configuration for Treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)  # Increase row height
        style.configure("Treeview.Cell", padding=5)  # Add padding to cells
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe', 'border': 1})])  # Add border
        
        # Tree view setup
        columns = ('current_name', 'predicted_name', 'new_name')
        self.tree = ttk.Treeview(self.main_container, columns=columns, show='tree headings', style="Treeview")
        
        # Configure column properties
        self.tree.column('current_name', width=300, stretch=True)
        self.tree.column('predicted_name', width=300, stretch=True)
        self.tree.column('new_name', width=300, stretch=True)
        
        self.tree.heading('current_name', text='Current Name')
        self.tree.heading('predicted_name', text='Predicted Names')
        self.tree.heading('new_name', text='New Name')
        
        # Add tags for different prediction states
        self.tree.tag_configure('proper_prediction', background=self.colors['proper_prediction'])
        self.tree.tag_configure('multiple_predictions', background=self.colors['multiple_predictions'])
        self.tree.tag_configure('no_prediction', background=self.colors['no_prediction'])
        
        self.tree.bind('<Double-Button-1>', self.edit_or_select)
        
        vsb = ttk.Scrollbar(self.main_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.main_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        
        # Context menu setup
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit Name", command=self.edit_name)
        self.context_menu.add_command(label="Choose Prediction", command=self.choose_prediction)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Predict", command=self.predict_this_name)
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def update_row_color(self, item, predictions):
        if len(predictions) == 1:
            if predictions[0]['predicted'] == True:
                self.tree.item(item, tags=('proper_prediction',))
            else:
                self.tree.item(item, tags=('no_prediction',))
        else:
            self.tree.item(item, tags=('multiple_predictions',))
    
    def edit_patterns(self):
        PatternsEditDialog(self.root)
        
    def edit_or_select(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            predictions = self.file_predictions.get(item)
            if predictions and len(predictions) == 1:
                self.edit_name()
            else:
                self.choose_prediction()
        
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def edit_name(self):
        item = self.tree.selection()[0]
        if item:
            dialog = NameEditDialog(self.root, [
                self.tree.item(item, 'values')[0], 
                self.tree.item(item, 'values')[2]
            ])
            if dialog.result:
                self.selected_names[item] = dialog.result
                current_values = list(self.tree.item(item, 'values'))
                current_values[2] = dialog.result

                self.tree.item(item, values=current_values)
                self.update_row_color(item, [{'predicted':True}]) # Select Green
    
    def choose_prediction(self):
        item = self.tree.selection()[0]
        if item and item in self.file_predictions:
            dialog = PredictionChoiceDialog(self.root, self.file_predictions[item])
            if dialog.result:
                self.selected_names[item] = dialog.result
                current_values = list(self.tree.item(item, 'values'))
                current_values[2] = dialog.result

                self.tree.item(item, values=current_values)
                self.update_row_color(item, [{'predicted':True}]) # Select Green
    
    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.load_files(folder_path)
    
    def load_files(self, path):
        self.tree.delete(*self.tree.get_children())
        self.file_predictions.clear()
        self.selected_names.clear()
        
        for root, dirs, files in os.walk(path):
            parent = self.tree.insert('', 'end', text=os.path.basename(root), 
                                    values=(root, '', ''), open=True)
            
            for file in files:
                if file.endswith(('.mp4', '.mkv', '.avi', '.mov')):
                    file_path = os.path.join(root, file)
                    self.tree.insert(parent, 'end', text='', 
                                   values=(file, '', ''))
    
    def clean_filename(self, filename):
        # Reload patterns module to get latest patterns
        import Patterns
        importlib.reload(Patterns)
        
        clean_name = filename
        for pattern in Patterns.remove_patterns:
            clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE)

        for pattern in Patterns.replace_patterns:
            clean_name = re.sub(pattern, ' ', clean_name)
        
        return ' '.join(clean_name.split())        
    
    def predict_all_names(self):
        if self.thread and self.thread.is_alive():
            return
        
        self.stop_prediction_flag.clear()
        self.status_var.set("Processing...")
        self.root.update_idletasks()
        
        items = self.get_all_file_items()
        total = len(items)
        self.progress_var.set(0)
        
        def process_files():
            for i, item in enumerate(items):
                if self.stop_prediction_flag.is_set():
                    break
                file_name = self.tree.item(item, 'values')[0]
                self.status_var.set(f"Processing: {file_name}")
                self.root.update_idletasks()
                
                predictions = self.get_predictions(file_name)
                if predictions:
                    self.file_predictions[item] = predictions
                    predicted_str = ' | '.join(p['title'] for p in predictions[:3])
                    selected_str = ""
                    
                    # Set new name if single prediction
                    if len(predictions) == 1:
                        selected_str = predictions[0]['title']
                        self.selected_names[item] = selected_str
                    
                    self.tree.item(item, values=(file_name, predicted_str, selected_str))
                    self.update_row_color(item, predictions)
                
                progress = ((i + 1) / total) * 100
                self.progress_var.set(progress)

            self.status_var.set("Ready")
            self.root.update_idletasks()
        
        self.thread = threading.Thread(target=process_files, daemon=True)
        self.thread.start()
    
    def get_language_based_result(self, results):
        language_priority = ['ml', 'ta', 'te', 'hi', 'en']
        result_languages = [r.get('original_language', '') for r in results]
        for lang in language_priority:
            indices = [ri for ri, rlang in enumerate(result_languages) if rlang == lang]
            if len(indices) > 0:
                return [results[i] for i in indices]
        
        return results
    
    def predict_this_name(self):
        item = self.tree.selection()[0]
        if item:
            file_name = self.tree.item(item, 'values')[0]
            predictions = self.get_predictions(file_name)
            if predictions:
                self.file_predictions[item] = predictions
                predicted_str = ' | '.join(p['title'] for p in predictions[:3])
                selected_str = ""
                
                # Set new name if single prediction
                if len(predictions) == 1:
                    selected_str = predictions[0]['title']
                    self.selected_names[item] = selected_str
                
                self.tree.item(item, values=(file_name, predicted_str, selected_str))
                self.update_row_color(item, predictions)
                
                if len(predictions) > 1:
                    self.choose_prediction()
    
    def get_predictions(self, filename):
        clean_name = self.clean_filename(filename)
        try:
            response = requests.get(
                f"{self.tmdb_base_url}/search/movie",
                params={
                    "api_key": self.tmdb_api_key,
                    "query": clean_name,
                    "region": "IN"
                }
            )
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                
                if len(results) > 1:
                    results = self.get_language_based_result(results)
                
                if len(results) == 0:
                    return [
                        {
                            'title': clean_name,
                            'original_title': clean_name,
                            'year': '',
                            'predicted': False
                        }
                    ]
                return [
                    {
                        'title': f"{r['title']} ({r.get('release_date', '')[:4]})",
                        'original_title': r.get('original_title', ''),
                        'year': r.get('release_date', '')[:4],
                        'predicted': True
                    }
                    for r in results[:5]
                ]
        except Exception as e:
            print(f"Error fetching predictions: {str(e)}")
        return []
    
    def get_all_file_items(self):
        items = []
        for item in self.tree.get_children():
            items.extend(self.tree.get_children(item))
        return items
    
    def apply_all_names(self):
        changes = []
        for item in self.get_all_file_items():
            if item in self.selected_names:
                parent = self.tree.parent(item)
                directory = self.tree.item(parent, 'values')[0]
                old_name = self.tree.item(item, 'values')[0]
                new_name = self.selected_names[item]
                
                old_path = os.path.join(directory, old_name)
                extension = os.path.splitext(old_name)[1]
                new_path = os.path.join(directory, f"{new_name}{extension}")
                
                changes.append((old_path, new_path))
        
        if changes:
            if messagebox.askyesno("Confirm Changes", 
                                 f"Apply {len(changes)} name changes?"):
                for old_path, new_path in changes:
                    try:
                        os.rename(old_path, new_path)
                    except Exception as e:
                        messagebox.showerror("Error", 
                                           f"Failed to rename {old_path}: {str(e)}")
                
                # Reload the current folder
                current_folder = os.path.dirname(changes[0][0])
                self.load_files(current_folder)
                messagebox.showinfo("Success", "Files renamed successfully")
