"""
GUI Application Launcher Entry Point for AI-Powered Secure Code Analyzer.
"""

import os
import sys

# Ensure root workspace directory is in sys.path when executed directly from inside gui/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gui.main_window import MainWindow
from gui.controller import Controller


def main() -> None:
    """Instantiates MainWindow and Controller and runs main event loop."""
    app = MainWindow()
    controller = Controller(app)
    app.mainloop()


if __name__ == "__main__":
    main()
