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
            self.supported_languages[language
