import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QIcon, QImage, QPixmap
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
        self.video_preview_label.setStyleSheet("border: 2px solid #ccc;")
        self.layout.addWidget(self.video_preview_label)

        # Button for loading a video
        self.load_button = QPushButton("Load Video", self)
        self.load_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.load_button.clicked.connect(self.load_video)
        self.layout.addWidget(self.load_button)

        # Button for editing video
        self.edit_button = QPushButton("Edit Video", self)
        self.edit_button.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;")
        self.edit_button.clicked.connect(self.edit_video)
        self.edit_button.setEnabled(False)  # Disable until a video is loaded
        self.layout.addWidget(self.edit_button)

        # Button for saving the edited video
        self.save_button = QPushButton("Save Video", self)
        self.save_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        self.save_button.clicked.connect(self.save_video)
        self.save_button.setEnabled(False)  # Disable until a video is edited
        self.layout.addWidget(self.save_button)

        # Set layout for the main window
        self.setLayout(self.layout)

        # Video file path
        self.video_file = None
        self.edited_clip = None

    def show_message(self, title, message, icon=QMessageBox.Information):
        """Display a message box with feedback."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()

    def load_video(self):
        """Load video and preview the first frame."""
        video_file, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if video_file:
            self.video_file = video_file
            self.edit_button.setEnabled(True)
            self.show_message("Video Loaded", "Successfully loaded the video.")
            self.preview_video(video_file)

    def preview_video(self, video_file):
        """Preview the first frame of the video."""
        cap = cv2.VideoCapture(video_file)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = frame.shape
            image = QImage(frame.data, width, height, 3 * width, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.video_preview_label.setPixmap(pixmap.scaled(self.video_preview_label.size(), Qt.KeepAspectRatio))
        else:
            self.show_message("Error", "Failed to preview the video.", QMessageBox.Critical)
        cap.release()

    def edit_video(self):
        """Edit the loaded video (e.g., resize)."""
        if self.video_file:
            try:
                clip = mp.VideoFileClip(self.video_file)
                self.edited_clip = clip.resize(0.5)  # Example: Resize to 50% of the original
                self.save_button.setEnabled(True)
                self.show_message("Edit Complete", "The video has been resized.")
                self.preview_edited_video()
            except Exception as e:
                self.show_message("Error", f"Failed to edit the video.\n{str(e)}", QMessageBox.Critical)

    def preview_edited_video(self):
        """Preview a frame from the edited video."""
        if self.edited_clip:
            try:
                frame = self.edited_clip.get_frame(0)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, _ = frame.shape
                image = QImage(frame.data, width, height, 3 * width, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.video_preview_label.setPixmap(pixmap.scaled(self.video_preview_label.size(), Qt.KeepAspectRatio))
            except Exception as e:
                self.show_message("Error", f"Failed to preview the edited video.\n{str(e)}", QMessageBox.Critical)

    def save_video(self):
        """Save the edited video."""
        if self.edited_clip:
            save_file, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
            if save_file:
                try:
                    self.edited_clip.write_videofile(save_file)
                    self.show_message("Save Complete", "The video has been saved successfully.")
                except Exception as e:
                    self.show_message("Error", f"Failed to save the video.\n{str(e)}", QMessageBox.Critical)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoEditorApp()
    window.show()
    sys.exit(app.exec_())
