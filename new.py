import moviepy.editor as mp

# Test MoviePy with a sample video
try:
    clip = mp.VideoFileClip("sample_video.mp4")  # Replace with your test video path
    print(f"Video duration: {clip.duration} seconds")
    clip_resized = clip.resize(0.5)
    clip_resized.write_videofile("resized_video.mp4")
except Exception as e:
    print(f"Error with MoviePy: {e}")
