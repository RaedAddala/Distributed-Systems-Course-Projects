import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from common.database import initialize_database, close_database
from common.rabbitmq import create_connection, setup_common_queue, receive_messages, close_connection

def main():
    
    app = QApplication(sys.argv)
    
    # Initialize the database and session
    db_name, engine, session = initialize_database()
    if not engine or not session:
        print("Failed to initialize database.")
        sys.exit(-1)

    # Establish RabbitMQ connection and channel
    connection, channel = create_connection()
    if not connection or not channel:
        print("Failed to establish RabbitMQ connection.")
        sys.exit(-1) 
    
    
    # Initialize and display the GUI
    window = MainWindow(session, channel)
    window.setWindowTitle(f"Head Office - {db_name}")
    
    # Declare the common queue for messaging and start listening
    setup_common_queue(channel, 'common_queue')
    receive_messages(channel, 'common_queue', session, lambda message: window.update_display(message))


    window.show()
    
    # Connect the cleanup function to the aboutToQuit signal
    app.aboutToQuit.connect(lambda: cleanup(window, session, engine, connection))

    # Start the Qt application loop
    result = app.exec_()
    sys.exit(result)

def cleanup(window, session, engine, connection):
    """Clean up resources on application exit."""
    print("Cleaning up resources!")
    window.cleanup()  
    session.close()  
    close_database(engine)  
    close_connection(connection)  

if __name__ == "__main__":
    main()
