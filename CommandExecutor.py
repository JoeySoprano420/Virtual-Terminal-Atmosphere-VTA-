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
            self.supported_languages[language] = getattr(module, 'execute')
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Error loading language module '{module_path}': {e}")

    def execute_command(self, language, command):
        if language in self.supported_languages:
            return self.supported_languages[language](command)
        else:
            return f"Language '{language}' is not supported."

    # Other methods unchanged...
