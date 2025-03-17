import logging

class ConsoleHandler(logging.Handler):
    """Custom logging handler to send logs to a Tkinter Text widget (e.g., console)."""

    def __init__(self, console_widget):
        super().__init__()
        self.console_widget = console_widget

    def emit(self, record):
        # Format the log record
        log_entry = self.format(record)
        # Insert the log entry into the console widget
        self.console_widget.insert("end", log_entry + "\n")
        # Ensure the latest log entry is visible
        self.console_widget.see("end")

