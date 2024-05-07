import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow  
from common.database import initialize_database

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # Create and connect to a new database
    db_name = initialize_database()  
    window.setWindowTitle(f"Head Office - {db_name}")
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
