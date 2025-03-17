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
import logging

from ctk.consoleHandler import ConsoleHandler


class App(ctk.CTk):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root_dir = pathlib.Path(__file__).parent.parent
    logs_dir = root_dir / "logs"

    def __init__(self):
        super().__init__()
        self.title("Duchifat")
        self.geometry("800x650")
        self.minsize(800, 650)

        # Load favicon if it exists
        favicon = self.root_dir / "duchifat.ico"
        if favicon.exists():
            self.iconbitmap(favicon)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True)

        self.plugin_folder = self.root_dir / "plugins"
        self.load_plugins()

    def initialize_logger(self, plugin_name, console_widget, log_level=logging.INFO):
        """
        Initialize a logger for a specific plugin.
        Each plugin will have its own logger with a separate file and console output.

        :param plugin_name: Name of the plugin.
        :param console_widget: Console widget for real-time log display.
        :param log_level: Logging level. Default is logging.INFO.
        :return: Configured logger instance.
        """
        # Ensure the plugin's log directory exists
        plugin_log_dir = self.logs_dir / plugin_name
        plugin_log_dir.mkdir(parents=True, exist_ok=True)

        # Create a timestamped log file
        log_file = plugin_log_dir / f"{strftime('%Y-%m-%d_%H-%M-%S')}.log"

        # Create a logger for the plugin
        logger = logging.getLogger(plugin_name)
        logger.setLevel(log_level)

        # Avoid adding multiple handlers if the logger is already initialized
        if not logger.handlers:
            # Console handler (logs to the console widget)
            console_handler = ConsoleHandler(console_widget)
            console_handler.setLevel(log_level)
            console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            console_handler.setFormatter(console_formatter)

            # File handler (logs to a file)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(file_formatter)

            # Add handlers to the logger
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

        return logger

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
        console.pack(fill="both", expand=True, pady=10)

        # Initialize a logger for the plugin with the console widget
        logger = self.initialize_logger(plugin_name, console)
        def run_script() -> None:
            # Collect user inputs as keyword arguments (kwargs) from the entries
            kwargs = {field: entry.get() for field, entry in entries.items()} | {'logger': logger}
            logger.info(f"Running script '{plugin_name}' with arguments: {kwargs}")

            # Path to the plugin script
            script_path = os.path.join(plugin_path, f"{plugin_name}.py")

            if os.path.exists(script_path):
                try:
                    # Dynamically import the plugin module
                    spec = importlib.util.spec_from_file_location(plugin_name, script_path)
                    plugin_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(plugin_module)

                    # Ensure the plugin has a 'main' function
                    if hasattr(plugin_module, "main") and callable(plugin_module.main):
                        try:
                            output = plugin_module.main(**kwargs)  # Call the plugin's main() function
                        except Exception as e:
                            logger.error(f"Error while executing plugin '{plugin_name}': {e}")
                    else:
                        logger.error(f"Plugin '{plugin_name}' does not have a callable main() function!")
                except Exception as e:
                    logger.error(f"Failed to load or execute plugin '{plugin_name}': {e}")
            else:
                logger.error(f"Plugin script not found at '{script_path}'!")

        run_button = ctk.CTkButton(tab, text="Run", command=run_script)
        run_button.pack(pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
