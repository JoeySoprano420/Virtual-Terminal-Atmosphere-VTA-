import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import subprocess
import os

class VTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Terminal Atmosphere (VTA)")
        self.root.geometry("800x600")

        self.create_widgets()
        self.clone_repository()

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

        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.run_menu.add_command(label="Run WCPL Code", command=self.run_wcpl_code)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)

        self.root.config(menu=self.menu_bar)

        self.current_file = None

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

    def clone_repository(self):
        repo_url = "https://github.com/JoeySoprano420/WordCom-ProLang-WCPL-.git"
        repo_name = "WordCom-ProLang-WCPL-"
        if not os.path.exists(repo_name):
            self.text_area.insert(tk.END, f"Cloning repository {repo_url}...\n")
            try:
                result = subprocess.run(f"git clone {repo_url}", shell=True, capture_output=True, text=True)
                self.text_area.insert(tk.END, result.stdout)
                if result.stderr:
                    self.text_area.insert(tk.END, result.stderr)
            except Exception as e:
                self.text_area.insert(tk.END, f"Error cloning repository: {e}\n")
        else:
            self.text_area.insert(tk.END, f"Repository {repo_name} already exists.\n")

    def new_file(self):
        self.current_file = None
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".wcpl",
                                               filetypes=[("WCPL Files", "*.wcpl"), ("All Files", "*.*")])
        if file_path:
            self.current_file = file_path
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".wcpl",
                                                 filetypes=[("WCPL Files", "*.wcpl"), ("All Files", "*.*")])
        if file_path:
            self.current_file = file_path
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    def run_wcpl_code(self):
        if not self.current_file:
            messagebox.showwarning("Warning", "Save the code before running.")
            return

        try:
            result = subprocess.run(f"wcpl {self.current_file}", shell=True, capture_output=True, text=True)
            self.text_area.insert(tk.END, "\n--- WCPL Output ---\n")
            self.text_area.insert(tk.END, result.stdout)
            if result.stderr:
                self.text_area.insert(tk.END, result.stderr)
        except Exception as e:
            self.text_area.insert(tk.END, f"Error running WCPL code: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VTApp(root)
    root.mainloop()
