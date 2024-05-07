from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QFormLayout, QDateEdit
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from common.database import insert_data
from common.rabbitmq import send_message, setup_common_queue, receive_messages

class MainWindow(QMainWindow):
    def __init__(self, session, channel, title):
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
        form_layout = QFormLayout()

        # Setup input fields
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        form_layout.addRow('Date:', self.date_edit)

        self.region_edit = QLineEdit()
        form_layout.addRow('Region:', self.region_edit)

        self.product_edit = QLineEdit()
        form_layout.addRow('Product:', self.product_edit)

        self.qty_edit = QLineEdit()
        self.qty_edit.setValidator(QIntValidator(1, 1000))
        form_layout.addRow('Qty:', self.qty_edit)

        self.cost_edit = QLineEdit()
        self.cost_edit.setValidator(QDoubleValidator(0.01, 10000.0, 2))
        form_layout.addRow('Cost:', self.cost_edit)

        self.amount_edit = QLineEdit()
        self.amount_edit.setValidator(QDoubleValidator(0.01, 1000000.0, 2))
        form_layout.addRow('Amount:', self.amount_edit)

        self.tax_edit = QLineEdit()
        self.tax_edit.setValidator(QDoubleValidator(0.01, 100000.0, 2))
        form_layout.addRow('Tax:', self.tax_edit)

        self.total_edit = QLineEdit()
        self.total_edit.setValidator(QDoubleValidator(0.01, 1000000.0, 2))
        form_layout.addRow('Total:', self.total_edit)

        # Submit and Send buttons
        self.submit_button = QPushButton('Submit Data & Send Updates', self)
        self.submit_button.clicked.connect(self.send_updates)
        form_layout.addRow(self.submit_button)

        # self.send_button = QPushButton('Send Updates', self)
        # self.send_button.clicked.connect(self.send_updates)
        # form_layout.addRow(self.send_button)

        layout.addLayout(form_layout)

        # Text display for incoming messages
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)

        # Setup RabbitMQ listening for incoming data
        setup_common_queue(self.channel, 'common_queue')
        receive_messages(self.channel, 'common_queue', self.session, self.update_display)

    def submit_data(self):
        data = {
            'Date': self.date_edit.date().toString("yyyy-MM-dd"),
            'Region': self.region_edit.text(),
            'Product': self.product_edit.text(),
            'Qty': int(self.qty_edit.text()),
            'Cost': float(self.cost_edit.text()),
            'Amount': float(self.amount_edit.text()),
            'Tax': float(self.tax_edit.text()),
            'Total': float(self.total_edit.text())
        }
        insert_data(self.session, **data)
        self.update_display(f"Inserted data: {data}")

    def send_updates(self):
        data = {
            'date': self.date_edit.date().toString("yyyy-MM-dd"),
            'region': self.region_edit.text(),
            'product': self.product_edit.text(),
            'qty': int(self.qty_edit.text()),
            'cost': float(self.cost_edit.text()),
            'amount': float(self.amount_edit.text()),
            'tax': float(self.tax_edit.text()),
            'total': float(self.total_edit.text())
        }
        send_message(self.channel, 'common_queue', data)
        insert_data(self.session, **data)
        self.update_display(f"Sent data: {data}")

    def update_display(self, message):
        """Updates the text display with a new message."""
        self.text_display.append(message)

    def cleanup(self):
        """Cleans up resources on application close."""
        print("Cleaning up resources...")
        self.session.close()
        self.channel.close()
