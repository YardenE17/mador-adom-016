"""
Project name: Duchifat
Author: Yarden Eshel

Description:
Duchifat is a cyberattack platform. It offers python platform and a development environment.
BLAH BLAH BLAH BLAH
"""

import customtkinter as ctk
import os
import json
import importlib.util
import pathlib
from time import strftime

class App(ctk.CTk):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root_dir = pathlib.Path(__file__).parent.parent

    def __init__(self):
        super().__init__()
        self.title("TITLE")
        self.geometry("800x650")
        self.minsize(800, 650)
        favicon = self.root_dir / "duchifat.ico"
        if favicon.exists():
            self.iconbitmap(favicon)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True)

        self.plugin_folder = self.root_dir / 'plugins'
        self.load_plugins()

    def load_plugins(self) -> None:
        # Iterate through the plugin folder
        for plugin_name in os.listdir(self.plugin_folder):
            plugin_path = os.path.join(self.plugin_folder, plugin_name)
            if os.path.isdir(plugin_path) and "__init__.py" in os.listdir(plugin_path):
                schema_file = os.path.join(plugin_path, "schema.json")
                if os.path.exists(schema_file):
                    with open(schema_file, "r") as f:
                        schema = json.load(f)
                    self.add_plugin_tab(plugin_name, schema, plugin_path)

    def add_plugin_tab(self, plugin_name: str, schema, plugin_path: str) -> None:
        tab = self.tabs.add(plugin_name)

        # Dynamically create input fields based on schema
        entries = {}
        for field in schema.get("fields", []):
            label = ctk.CTkLabel(tab, text=field["name"])
            label.pack()
            entry = ctk.CTkEntry(tab)
            entry.pack()
            entries[field["name"]] = entry

        # Console view
        console = ctk.CTkTextbox(tab)
        console.pack(fill="x", pady=10)

        def run_script() -> None:
            # Collect user inputs as keyword arguments (kwargs) from the entries
            kwargs = {field: entry.get() for field, entry in entries.items()}

            # Path to the plugin script
            script_path = os.path.join(plugin_path, f"{plugin_name}.py")

            if os.path.exists(script_path):
                try:
                    # Dynamically import the plugin module
                    spec = importlib.util.spec_from_file_location(plugin_name, script_path)
                    plugin_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(plugin_module)

                    # Ensure the plugin has a 'main' function
                    if hasattr(plugin_module, 'main') and callable(plugin_module.main):
                        # Call the plugin's main() function with the kwargs
                        console.delete("1.0", "end")  # Clear the console view
                        try:
                            output = plugin_module.main(**kwargs)  # Pass keyword arguments dynamically
                            console.insert("end", output)  # Display the output in the console
                        except Exception as e:
                            console.insert("end", f"[ERROR] {str(e)}")
                    else:
                        console.insert("end",
                                       f"[ERROR] Plugin '{plugin_name}' does not have a callable main() function!")
                except Exception as e:
                    console.insert("end", f"[ERROR] Failed to load or execute plugin '{plugin_name}': {str(e)}")
            else:
                console.insert("end", f"[ERROR] Plugin script not found at {script_path}!")

        def save_log_to_file():
            log_content = console.get("1.0", "end").strip()  # Get all text from the console
            if log_content:
                logs_dir = self.root_dir / "logs"
                logs_dir.mkdir(parents=True, exist_ok=True)
                log_file_path = logs_dir / f"{plugin_name}_{strftime('%Y-%m-%d_%H-%M-%S')}.log"
                try:
                    print(log_content)
                    log_file_path.write_text(log_content)
                    print(log_content)
                    console.insert("end", f"\n[INFO] Log saved to {log_file_path}")
                except Exception as e:
                    console.insert("end", f"\n[ERROR] Failed to save log: {str(e)}")

        run_button = ctk.CTkButton(tab, text="Run", command=run_script)
        run_button.pack(pady=5)

        save_button = ctk.CTkButton(tab, text="Save Log", command=save_log_to_file)
        save_button.pack(pady=5)