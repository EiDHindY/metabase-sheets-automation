from dotenv import load_dotenv
load_dotenv()
import sys
from PySide6.QtWidgets import QApplication
from src.ui.gui.main_window import MainWindow
def main() -> None:
    """Initialize the Qt application, create the main window, and start the event loop."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()



