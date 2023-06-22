from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QMessageBox, QGridLayout, QFileDialog
from add_logo_properties import LogoWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from image_changed_signal import ImageSignal
from add_text_properties import TextWidget


class MainWindow(QMainWindow):
    # This is the signal that will be sent to logo and text widgets when we open the new photo in main_window
    image_changed = ImageSignal()

    def __init__(self):
        super().__init__()
        # Initiating method that creates GUI
        self.initUi()
        # Creating file_path variable and setting it to empty string
        self.file_path = ""

    def initUi(self):
        # Set window title
        self.setWindowTitle("Watermarker")

        # Set geometry of the main window
        self.setGeometry(300, 300, 900, 600)

        # Set up layout manager
        self.layout = QGridLayout()

        # Set the layout on the main window
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Create widgets
        self.open_image_btn = QPushButton("Open Image")
        self.add_logo_btn = QPushButton("Add Logo")
        self.add_text_btn = QPushButton("Add Text")
        self.preview = QLabel()

        # Set the preview label default color to black
        self.preview.setStyleSheet("background-color: black;")

        # Adding widgets to the layout
        self.layout.addWidget(self.open_image_btn, 1, 2)
        self.layout.addWidget(self.add_logo_btn, 1, 4)
        self.layout.addWidget(self.add_text_btn, 1, 6)
        self.layout.addWidget(self.preview, 2, 1, 5, 7)

        # Connect buttons with functionalities
        self.open_image_btn.clicked.connect(self.open_photo)
        self.add_text_btn.clicked.connect(self.add_text_widget)
        self.add_logo_btn.clicked.connect(self.add_logo_widget)

    def open_photo(self):
        """This method uses the QFileDialog() to give user ability to choose image for editing"""
        file_dialog = QFileDialog()
        self.file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png)")

        if self.file_path:
            # Send signal when the image is open
            self.image_changed.signal.emit(self.file_path)
            # Display image on preview label
            pixmap = QPixmap(self.file_path)
            self.preview.setPixmap(pixmap.scaled(self.preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def add_text_widget(self):
        """This method instantiates TextWidget class"""
        if self.file_path != "":
            if TextWidget.instance_count < 1:
                self.text_widget = TextWidget(self.file_path, main_window=self)
                main_window_geometry = self.frameGeometry()
                text_widget_x = main_window_geometry.x() + main_window_geometry.width()
                text_widget_y = main_window_geometry.y()
                self.text_widget.move(text_widget_x, text_widget_y)
                self.text_widget.show()
        else:
            self.no_image_dialog()

    def add_logo_widget(self):
        """This method instantiates LogoWidget class"""
        if self.file_path != "":
            if LogoWidget.instance_count < 1:
                self.logo_widget = LogoWidget(self.file_path, main_window=self)
                main_window_geometry = self.frameGeometry()
                logo_widget_x = main_window_geometry.x() + main_window_geometry.width()
                logo_widget_y = main_window_geometry.y()
                self.logo_widget.move(logo_widget_x, logo_widget_y)
                self.logo_widget.show()
        else:
            self.no_image_dialog()

    def update_image(self, edited_image):
        """This method updates the image in preview label. It gets image to display from TextWidget or LogoWidget"""
        qimage = QImage(edited_image.tobytes(), edited_image.width, edited_image.height, QImage.Format_RGBA8888)
        qpixmap = QPixmap.fromImage(qimage)
        scaled_qpixmap = qpixmap.scaled(self.preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview.setPixmap(scaled_qpixmap)

    def no_image_dialog(self):
        """This method informs the user that it needs to open an image in order to use program's functionalities"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("No image selected. Please select image first")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
