import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import subprocess
import os
import re
import qiskit
import pygame
from pydub import AudioSegment
from midiutil import MIDIFile
import manim

# Lexer for WCPL
class Lexer:
    TOKENS = {
        'START': r'\bstart\b',
        'STOP': r'\bstop\b',
        'OPEN': r'\bopen\b',
        'CLOSE': r'\bclose\b',
        'PRINT': r'\bdynamic_print\b',
        'SCRIPT': r'\bscript\b',
        'QUANTUM': r'\bquantum\b',
        'GAME': r'\bgame\b',
        'MUSIC': r'\bmusic\b',
        'ANIMATION': r'\banimation\b',
        'IDENTIFIER': r'[a-zA-Z_][a-zA-Z_0-9]*',
        'STRING': r'\".*?\"',
        'NUMBER': r'\b\d+\b',
        'WHITESPACE': r'\s+',
        'NEWLINE': r'\n',
        'COMMENT': r'#.*',
    }

    def __init__(self, code):
        self.code = code
        self.tokens = self.tokenize()
    
    def tokenize(self):
        tokens = []
        for token_type, pattern in self.TOKENS.items():
            regex = re.compile(pattern)
            for match in regex.finditer(self.code):
                tokens.append((token_type, match.group()))
        tokens.sort(key=lambda x: x[1])
        return tokens

# Parser for WCPL
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.macros = {}

    def parse(self):
        parsed_code = []
        while self.pos < len(self.tokens):
            token_type, value = self.tokens[self.pos]
            if token_type == 'START':
                parsed_code.append({'action': 'start'})
            elif token_type == 'STOP':
                parsed_code.append({'action': 'stop'})
            elif token_type == 'PRINT':
                self.pos += 1
                value = self.tokens[self.pos][1]
                parsed_code.append({'action': 'dynamic_print', 'value': value})
            elif token_type == 'QUANTUM':
                self.pos += 1
                q_command = self.tokens[self.pos][1]
                parsed_code.append({'action': 'quantum', 'command': q_command})
            elif token_type == 'GAME':
                self.pos += 1
                g_command = self.tokens[self.pos][1]
                parsed_code.append({'action': 'game', 'command': g_command})
            elif token_type == 'MUSIC':
                self.pos += 1
                m_command = self.tokens[self.pos][1]
                parsed_code.append({'action': 'music', 'command': m_command})
            elif token_type == 'ANIMATION':
                self.pos += 1
                a_command = self.tokens[self.pos][1]
                parsed_code.append({'action': 'animation', 'command': a_command})
            # Add more parsing rules here
            self.pos += 1
        return parsed_code

# Main VTA Application
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

        with open(self.current_file, "r") as file:
            code = file.read()

        lexer = Lexer(code)
        parser = Parser(lexer.tokens)
        parsed_code = parser.parse()

        for command in parsed_code:
            if command['action'] == 'start':
                self.text_area.insert(tk.END, "\n--- WCPL Code Start ---\n")
            elif command['action'] == 'stop':
                self.text_area.insert(tk.END, "\n--- WCPL Code Stop ---\n")
            elif command['action'] == 'dynamic_print':
                self.text_area.insert(tk.END, f"{command['value']}\n")
            elif command['action'] == 'quantum':
                self.run_quantum_command(command['command'])
            elif command['action'] == 'game':
                self.run_game_command(command['command'])
            elif command['action'] == 'music':
                self.run_music_command(command['command'])
            elif command['action'] == 'animation':
                self.run_animation_command(command['command'])

    def run_quantum_command(self, command):
        try:
            if command == "create_circuit":
                qc = qiskit.QuantumCircuit(2)
                qc.h(0)
                qc.cx(0, 1)
                result = qc.draw()
                self.text_area.insert(tk
                self.text_area.insert(tk.END, f"Quantum Circuit:\n{result}\n")
            # Add more quantum-related commands here
        except Exception as e:
            self.text_area.insert(tk.END, f"Error running quantum command: {e}\n")

    def run_game_command(self, command):
        try:
            if command == "init_pygame":
                pygame.init()
                self.text_area.insert(tk.END, "Pygame initialized.\n")
            elif command == "create_window":
                screen = pygame.display.set_mode((800, 600))
                self.text_area.insert(tk.END, "Pygame window created.\n")
            elif command == "load_image":
                image = pygame.image.load('example.png')
                self.text_area.insert(tk.END, "Image loaded.\n")
            # Add more pygame-related commands here
        except Exception as e:
            self.text_area.insert(tk.END, f"Error running game command: {e}\n")

    def run_music_command(self, command):
        try:
            if command.startswith("load_audio"):
                _, file_path = command.split(' ', 1)
                audio = AudioSegment.from_file(file_path)
                self.text_area.insert(tk.END, f"Audio loaded from {file_path}.\n")
            elif command == "play_audio":
                # Playing audio functionality would require additional code
                self.text_area.insert(tk.END, "Audio playing functionality needs implementation.\n")
            # Add more music-related commands here
        except Exception as e:
            self.text_area.insert(tk.END, f"Error running music command: {e}\n")

    def run_animation_command(self, command):
        try:
            if command == "render_scene":
                # Example: Render a simple scene using Manim
                scene = manim.Scene()
                scene.play(manim.Write(manim.Text("Hello, Manim!")))
                self.text_area.insert(tk.END, "Animation rendered.\n")
            # Add more animation-related commands here
        except Exception as e:
            self.text_area.insert(tk.END, f"Error running animation command: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VTApp(root)
    root.mainloop()
