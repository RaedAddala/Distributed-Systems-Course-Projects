from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget
from common.rabbitmq import setup_common_exchange, receive_messages
from PyQt5.QtCore import pyqtSignal, QObject

class Worker(QObject):
    message_received = pyqtSignal(str)  # Custom signal to handle string messages // to prevent race conditions when working with threads

class MainWindow(QMainWindow):
    def __init__(self, session, channel,title):
        super().__init__()
        self.session = session
        self.channel = channel
        self.title = title
        self.worker = Worker()  # Worker object to handle background tasks
        self.worker.message_received.connect(self.update_display)  # Connect signal to slot
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Text display for incoming messages
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)
        
        # Setup RabbitMQ listening for incoming data
        try:
            setup_common_exchange(self.channel, 'common_exchange')
            receive_messages(self.channel, 'common_exchange', self.session, self.worker.message_received.emit)
        except Exception as err:
            print(f"Error setting up RabbitMQ in GUI: {err}")

    def update_display(self, message):
        """Updates the text display with a new message."""
        self.text_display.append(message)

    def cleanup(self):
        """Cleans up resources on application close."""
        print("Cleaning up resources...")
        self.session.close()
        self.channel.close()


        
