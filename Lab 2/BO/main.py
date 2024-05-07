import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from common.database import initialize_database
from common.gui import cleanup

def main():
    app = QApplication(sys.argv)
    db_name = initialize_database()  # Create and connect to a new database
    window = MainWindow()
    window.setWindowTitle(f"Base Office - {db_name}")
    
    # Connect the cleanup function to the aboutToQuit signal
    app.aboutToQuit.connect(cleanup)

    window.show()

    app.exec_()
    
if __name__ == "__main__":
    main()
