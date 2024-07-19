import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import torch
from transformers import pipeline
import importlib

class CommandExecutor:
    def __init__(self):
        self.supported_languages = {
            'bash': self.execute_bash,
            'shell': self.execute_shell,
            'wcpl': self.execute_wcpl,
            'spinstar': self.execute_spinstar,
            'yaml': self.execute_yaml,
            'antlr': self.execute_antlr,
            'generate': self.generate_text
        }
        self.generator = pipeline('text-generation', model='gpt-2')

    def load_language_module(self, language, module_path):
        try:
            module = importlib.import_module(module_path)
            self.supported_languages[language] = module.execute
            return f"Module for language '{language}' loaded successfully."
        except Exception as e:
            return f"Failed to load module for language '{language}': {e}"

    def execute_bash(self, code):
        return subprocess.check_output(code, shell=True, text=True)

    def execute_shell(self, code):
        return subprocess.check_output(code, shell=True, text=True)

    def execute_wcpl(self, code):
        # Placeholder for WCPL execution
        return "Executing WCPL: " + code

    def execute_spinstar(self, code):
        # Placeholder for SpinStar execution
        return "Executing SpinStar: " + code

    def execute_yaml(self, code):
        # Placeholder for YAML execution
        return "Executing YAML: " + code

    def execute_antlr(self, code):
        # Placeholder for ANTLR execution
        return "Executing ANTLR: " + code

    def generate_text(self, prompt):
        result = self.generator(prompt, max_length=50, num_return_sequences=1)
        return result[0]['generated_text']

    def execute(self, language, code):
        if language in self.supported_languages:
            return self.supported_languages[language](code)
        else:
            return f"Unsupported language: {language}"

class CommandApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Command Executor")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.language_label = tk.Label(root, text="Language:")
        self.language_label.pack(padx=10, pady=5)

        self.language_entry = tk.Entry(root)
        self.language_entry.pack(padx=10, pady=5)

        self.execute_button = tk.Button(root, text="Execute", command=self.execute_command)
        self.execute_button.pack(padx=10, pady=10)

        self.result_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
        self.result_area.pack(padx=10, pady=10)

        self.executor = CommandExecutor()

    def execute_command(self):
        code = self.text_area.get("1.0", tk.END).strip()
        language = self.language_entry.get().strip().lower()

        if code and language:
            result = self.executor.execute(language, code)
            self.result_area.delete("1.0", tk.END)
            self.result_area.insert(tk.END, result)
        else:
            self.result_area.delete("1.0", tk.END)
            self.result_area.insert(tk.END, "Please enter both code and language.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CommandApp(root)
    root.mainloop()
