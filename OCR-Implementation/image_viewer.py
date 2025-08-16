import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
)
from PySide6.QtGui import QPixmap


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setGeometry(200, 200, 600, 400)

        # Layout
        self.layout = QVBoxLayout()

        # Button to load image
        self.button = QPushButton("Open Image")
        self.button.clicked.connect(self.open_image)
        self.layout.addWidget(self.button)

        # Label to show image
        self.image_label = QLabel("No Image Selected")
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.image_label.setScaledContents(True)  # Scale image to fit label
        self.layout.addWidget(self.image_label)

        self.setLayout(self.layout)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            self.image_path = file_name  # save path
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)
            self.image_label.resize(pixmap.width(), pixmap.height())

        return self.image_path  # return the path

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())
