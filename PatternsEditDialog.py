import importlib
import tkinter as tk
from tkinter import ttk, messagebox
import json

class PatternsEditDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Patterns")
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.load_patterns()
        
        self.dialog.wait_window()
    
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.dialog)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Remove patterns tab
        self.remove_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.remove_frame, text="Remove Patterns")
        
        # Replace patterns tab
        self.replace_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.replace_frame, text="Replace Patterns")
        
        # Setup remove patterns list
        remove_label = ttk.Label(self.remove_frame, text="Patterns to remove:")
        remove_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.remove_text = tk.Text(self.remove_frame, height=15)
        self.remove_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        # Setup replace patterns list
        replace_label = ttk.Label(self.replace_frame, text="Patterns to replace with space:")
        replace_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.replace_text = tk.Text(self.replace_frame, height=15)
        self.replace_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Save", command=self.save_patterns).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
    
    def load_patterns(self):
        import Patterns
        importlib.reload(Patterns)
        
        # Load remove patterns
        remove_text = '\n'.join(p.strip('r\'').strip('\'') for p in Patterns.remove_patterns)
        self.remove_text.delete('1.0', tk.END)
        self.remove_text.insert('1.0', remove_text)
        
        # Load replace patterns
        replace_text = '\n'.join(p.strip('r\'').strip('\'') for p in Patterns.replace_patterns)
        self.replace_text.delete('1.0', tk.END)
        self.replace_text.insert('1.0', replace_text)
    
    def save_patterns(self):
        try:
            # Get patterns from text areas
            remove_patterns = [f"r'{p.strip()}'" for p in self.remove_text.get('1.0', tk.END).strip().split('\n') if p.strip()]
            replace_patterns = [f"r'{p.strip()}'" for p in self.replace_text.get('1.0', tk.END).strip().split('\n') if p.strip()]
            
            # Create patterns file content
            line_sep = r"',\n    '"
            content = f"""# Remove common patterns
remove_patterns = [
    {line_sep.join(remove_patterns)}
]

# Replace patterns with spaces
replace_patterns = [
    {line_sep.join(replace_patterns)}
]"""
            
            # Write to file
            with open('Patterns.py', 'w') as f:
                f.write(content)
            
            messagebox.showinfo("Success", "Patterns saved successfully!")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save patterns: {str(e)}")
