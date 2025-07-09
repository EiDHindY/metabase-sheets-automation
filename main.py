# main.py

from dotenv import load_dotenv
load_dotenv()

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from src.ui.gui.main_window import MainWindow

def main() -> None:
    """Initialize the Qt application, create the main window, and start the event loop."""
    
    # Enable high DPI scaling for modern displays
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # Create application
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Team Data Processor")
    app.setApplicationVersion("1.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Center the window on screen
    screen = app.primaryScreen().geometry()
    window_geometry = window.geometry()
    x = (screen.width() - window_geometry.width()) // 2
    y = (screen.height() - window_geometry.height()) // 2
    window.move(x, y)
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()