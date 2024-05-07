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
        print(f"Error initializing database: {err}")
        sys.exit(-1)

    if not engine or not session:
        print("Failed to initialize database.")
        sys.exit(-1)

    try:
        connection, channel = create_connection()
    except Exception as err:
        print(f"Error establishing RabbitMQ connection: {err}")
        sys.exit(-1)
    
    if not connection or not channel:
        print("Failed to establish RabbitMQ connection.")
        sys.exit(-1)

    try:
        window = MainWindow(session, channel, f"Base Office - {db_name}")
        window.show()
    except Exception as err:
        print(f"Error during GUI initialization: {err}")
        sys.exit(-1)

    app.aboutToQuit.connect(lambda: cleanup(window, session, engine, connection))
    sys.exit(app.exec_())

def cleanup(window, session, engine, connection):
    window.cleanup()
    session.close()
    close_database(engine)
    close_connection(connection)

if __name__ == "__main__":
    main()