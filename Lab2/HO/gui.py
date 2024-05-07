from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget
from common.rabbitmq import setup_common_queue, receive_messages

class MainWindow(QMainWindow):
    def __init__(self, session, channel,title):
        super().__init__()
        self.session = session
        self.channel = channel
        self.title = title
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
            setup_common_queue(self.channel, 'common_queue')
            receive_messages(self.channel, 'common_queue', self.session, self.update_display)
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


        
