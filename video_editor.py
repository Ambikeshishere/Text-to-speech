import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class VideoEditorApp(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Video Editor")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        self.layout = QVBoxLayout()

        # Video preview label
        self.video_preview_label = QLabel("Video Preview", self)
        self.video_preview_label.setAlignment(Qt.AlignCenter)
        self.video_preview_label.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.video_preview_label)

        # Buttons
        self.load_button = QPushButton("Load Video", self)
        self.load_button.clicked.connect(self.load_video)
        self.layout.addWidget(self.load_button)

        self.edit_button = QPushButton("Edit Video", self)
        self.edit_button.clicked.connect(self.edit_video)
        self.edit_button.setEnabled(False)  # Enable only after loading a video
        self.layout.addWidget(self.edit_button)

        self.save_button = QPushButton("Save Video", self)
        self.save_button.clicked.connect(self.save_video)
        self.save_button.setEnabled(False)  # Enable only after editing a video
        self.layout.addWidget(self.save_button)

        # Set layout
        self.setLayout(self.layout)

        # State variables
        self.video_file = None
        self.edited_video = None
        self.frame_width = None
        self.frame_height = None

    def load_video(self):
        # Open file dialog to load a video
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mkv *.mov)")
        if file_name:
            self.video_file = file_name
            self.edit_button.setEnabled(True)
            self.preview_video(file_name)

    def preview_video(self, video_path):
        # Preview the first frame of the video
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        if ret:
            self.display_frame(frame)
        else:
            self.video_preview_label.setText("Failed to load video!")
        cap.release()

    def edit_video(self):
        if self.video_file:
            # Resize the video to half its original dimensions
            self.edited_video = []
            cap = cv2.VideoCapture(self.video_file)
            self.frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 2)
            self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2)
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                resized_frame = cv2.resize(frame, (self.frame_width, self.frame_height))
                self.edited_video.append(resized_frame)

            cap.release()
            self.save_button.setEnabled(True)

            # Display the first frame of the edited video
            if self.edited_video:
                self.display_frame(self.edited_video[0])

    def save_video(self):
        if self.edited_video:
            # Open file dialog to save the video
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "Video Files (*.mp4 *.avi)")
            if save_path:
                # Write the edited video
                fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi
                out = cv2.VideoWriter(save_path, fourcc, 20.0, (self.frame_width, self.frame_height))

                for frame in self.edited_video:
                    out.write(frame)

                out.release()

    def display_frame(self, frame):
        # Convert frame to QImage and display it in QLabel
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = frame_rgb.shape
        q_image = QImage(frame_rgb.data, width, height, width * channels, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.video_preview_label.setPixmap(pixmap.scaled(self.video_preview_label.size(), Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoEditorApp()
    window.show()
    sys.exit(app.exec_())
