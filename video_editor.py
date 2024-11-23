import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, 
    QFileDialog, QSlider, QMessageBox, QListWidget, QHBoxLayout
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips


class VideoEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Editor")
        self.setGeometry(100, 100, 900, 600)

        # Video player setup
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        # UI elements
        self.open_button = QPushButton("Load Video")
        self.open_button.clicked.connect(self.open_file)

        self.trim_button = QPushButton("Trim Video")
        self.trim_button.clicked.connect(self.trim_video)

        self.merge_button = QPushButton("Merge Videos")
        self.merge_button.clicked.connect(self.merge_videos)

        self.export_button = QPushButton("Export Video")
        self.export_button.clicked.connect(self.export_video)

        self.video_list = QListWidget()  # For storing multiple videos for merging

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self.set_position)

        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Layout setup
        control_layout = QVBoxLayout()
        control_layout.addWidget(self.open_button)
        control_layout.addWidget(self.trim_button)
        control_layout.addWidget(self.merge_button)
        control_layout.addWidget(self.export_button)
        control_layout.addWidget(self.video_list)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_widget)
        main_layout.addWidget(self.slider)
        main_layout.addWidget(self.status_label)

        layout = QHBoxLayout()
        layout.addLayout(main_layout, 3)
        layout.addLayout(control_layout, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect media player to video widget
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.update_status)

        # Variables to store loaded video
        self.current_video = None
        self.loaded_videos = []

    def open_file(self):
        """Load a video file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if file_name:
            self.current_video = VideoFileClip(file_name)
            self.loaded_videos.append(self.current_video)
            self.video_list.addItem(file_name)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.media_player.play()
            self.status_label.setText("Video Loaded: Playing")

    def trim_video(self):
        """Trim the currently loaded video."""
        if not self.current_video:
            QMessageBox.warning(self, "Error", "No video loaded!")
            return
        start_time, end_time = 0, 10  # Hardcoded for now (e.g., trim first 10 seconds)
        trimmed_video = self.current_video.subclip(start_time, end_time)
        self.current_video = trimmed_video
        self.status_label.setText("Video Trimmed!")

    def merge_videos(self):
        """Merge multiple videos."""
        if len(self.loaded_videos) < 2:
            QMessageBox.warning(self, "Error", "Add at least 2 videos to merge!")
            return
        merged_video = concatenate_videoclips(self.loaded_videos)
        self.current_video = merged_video
        self.status_label.setText("Videos Merged!")

    def export_video(self):
        """Export the current video."""
        if not self.current_video:
            QMessageBox.warning(self, "Error", "No video to export!")
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Video", "", "MP4 Files (*.mp4)")
        if file_name:
            self.current_video.write_videofile(file_name, codec="libx264")
            self.status_label.setText("Video Exported Successfully!")

    def set_position(self, position):
        """Set the video position."""
        self.media_player.setPosition(position)

    def update_status(self):
        """Update the status label based on the media player state."""
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.status_label.setText("Status: Playing")
        elif self.media_player.state() == QMediaPlayer.PausedState:
            self.status_label.setText("Status: Paused")
        else:
            self.status_label.setText("Status: Stopped")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoEditorApp()
    window.show()
    sys.exit(app.exec_())
