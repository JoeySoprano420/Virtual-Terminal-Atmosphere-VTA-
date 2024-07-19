import tkinter as tk
from tkinter import scrolledtext

class VTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Terminal Atmosphere (VTA)")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.root, font=("Courier", 12))
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        command = self.entry.get()
        self.text_area.insert(tk.END, f"> {command}\n")
        self.entry.delete(0, tk.END)
        # Here, you would integrate the logic to handle the command execution

if __name__ == "__main__":
    root = tk.Tk()
    app = VTApp(root)
    root.mainloop()
