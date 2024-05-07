import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from common.database import initialize_database

def main():
    app = QApplication(sys.argv)
    db_name = initialize_database()  # Create and connect to a new database
    window = MainWindow()
    window.setWindowTitle(f"Base Office - {db_name}")
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
