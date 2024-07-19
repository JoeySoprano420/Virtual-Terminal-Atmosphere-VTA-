import tkinter as tk
from tkinter import scrolledtext
import subprocess

class VTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Terminal Atmosphere (VTA)")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(fill=tk.X)

        self.entry = tk.Entry(self.entry_frame, font=("Courier", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.execute_command)

        self.submit_button = tk.Button(self.entry_frame, text="Submit", command=self.execute_command)
        self.submit_button.pack(side=tk.RIGHT)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_output)
        self.clear_button.pack(fill=tk.X)

    def execute_command(self, event=None):
        command = self.entry.get()
        self.text_area.insert(tk.END, f"> {command}\n")
        self.entry.delete(0, tk.END)

        if command.strip() == "":
            return

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.text_area.insert(tk.END, result.stdout)
            if result.stderr:
                self.text_area.insert(tk.END, result.stderr)
        except Exception as e:
            self.text_area.insert(tk.END, f"Error executing command: {e}\n")

    def clear_output(self):
        self.text_area.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VTApp(root)
    root.mainloop()
