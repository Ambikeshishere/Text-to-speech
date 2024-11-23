import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import cv2
import moviepy.editor as mp

class VideoEditorApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Video Editing Software")
        self.setWindowIcon(QIcon("video_icon.png"))  # Add your custom icon here
        self.setGeometry(100, 100, 800, 600)

        # Set layout
        self.layout = QVBoxLayout()
        
        # Video preview label
        self.video_preview_label = QLabel("Video Preview Here", self)
        self.video_preview_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_preview_label)

        # Button for loading a video
        self.load_button = QPushButton("Load Video", self)
        self.load_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.load_button.clicked.connect(self.load_video)
        self.layout.addWidget(self.load_button)

        # Button for editing video
        self.edit_button = QPushButton("Edit Video", self)
        self.edit_button.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.edit_button)

        # Button for saving the edited video
        self.save_button = QPushButton("Save Video", self)
        self.save_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.save_button)

        # Set layout for the main window
        self.setLayout(self.layout)

    def load_video(self):
        # File dialog to load a video
        video_file, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if video_file:
            self.preview_video(video_file)

    def preview_video(self, video_file):
        # Use OpenCV to show a frame from the video
        cap = cv2.VideoCapture(video_file)
        ret, frame = cap.read()
        if ret:
            # Show the first frame as preview
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = frame.shape
            image = QImage(frame.data, width, height, 3 * width, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.video_preview_label.setPixmap(pixmap.scaled(self.video_preview_label.size(), Qt.KeepAspectRatio))
        cap.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoEditorApp()
    window.show()
    sys.exit(app.exec_())
