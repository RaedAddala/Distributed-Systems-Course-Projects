import sys

sys.path.insert(0, '../')

from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from common.database import initialize_database, close_database
from common.rabbitmq import create_connection, close_connection

def main():
    app = QApplication(sys.argv)
    try:
        db_name, engine, session = initialize_database()
    except Exception as err:
          print(f"Error : {err}")
          sys.exit(-1)
    if not engine or not session:
        print("Failed to initialize database.")
        sys.exit(-1)
    
    connection, channel = create_connection()
    if not connection or not channel:
        print("Failed to establish RabbitMQ connection.")
        sys.exit(-1)
    
    window = MainWindow(session, channel)
    window.setWindowTitle(f"Head Office - {db_name}")
    window.show()
    app.aboutToQuit.connect(lambda: cleanup(window, session, engine, connection))
    
    result = app.exec_()
    sys.exit(result)

def cleanup(window, session, engine, connection):
    window.cleanup()
    session.close()
    close_database(engine)
    close_connection(connection)

if __name__ == "__main__":
    main()
