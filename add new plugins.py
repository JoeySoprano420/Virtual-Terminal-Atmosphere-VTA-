# new_plugin.py
from base_plugin import BasePlugin

class NewPlugin(BasePlugin):
    def __init__(self, path):
        self.path = path

    def run_script(self, script):
        script_path = os.path.join(self.path, "temp_script.new")
        with open(script_path, "w") as file:
            file.write(script)
        result = subprocess.run(["python", os.path.join(self.path, "new_interpreter.py"), script_path], capture_output=True, text=True)
        return result.stdout

# Add new plugin to VTApp
# in vtapp.py
from new_plugin import NewPlugin

self.plugins = {
    "WordCom-ProLang-WCPL": WCPLPlugin(wcpl_path),
    "SpinStar": SpinStarPlugin(spinstar_path),
    "NewPlugin": NewPlugin("path/to/NewPlugin")
}
