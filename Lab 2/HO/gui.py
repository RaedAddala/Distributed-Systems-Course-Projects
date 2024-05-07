from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from common.rabbitmq import setup_common_queue, receive_messages
from common.database import get_data
import json

class MainWindow(QMainWindow):
    def __init__(self, session, channel):
        super().__init__()
        self.session = session
        self.channel = channel
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Head Office GUI')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Text display for incoming messages
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)

        # RabbitMQ Listening for incoming data
        setup_common_queue(self.channel, 'common_queue')
        receive_messages(self.channel, 'common_queue', self.session, self.display_message)

        # Button to refresh and check database
        self.refresh_button = QPushButton('Check Database', self)
        self.refresh_button.clicked.connect(self.check_database)
        layout.addWidget(self.refresh_button)

    def display_message(self, message):
        """Updates the text display with a new message, parsed from JSON."""
        try:
            data = json.loads(message)
            display_text = f"Received update - Date: {data['Date']}, Region: {data['Region']}, Product: {data['Product']}, Qty: {data['Qty']}, Cost: {data['Cost']}, Amount: {data['Amount']}, Tax: {data['Tax']}, Total: {data['Total']}"
            self.text_display.append(display_text)
        except json.JSONDecodeError:
            self.text_display.append("Received non-JSON message: " + message)

    def check_database(self):
        """Function to fetch and display data from the database."""
        try:
            data = get_data(self.session)
            self.text_display.append("Database Check:")
            for record in data:
                self.text_display.append(str(record))
        except Exception as e:
            self.text_display.append(f"Error checking database: {str(e)}")

    def cleanup(self):
        """Cleans up resources on application close."""
        print("Cleaning up resources!")
        self.session.close()
        self.channel.close()




        
