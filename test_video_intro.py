
from video_producer import process_video
import os

raw_video = "demo_gameplay.webm"
output_video = "test_output.mp4"

if not os.path.exists(raw_video):
    print("DEMO VIDEO MISSING. Creating dummy...")
    from moviepy.editor import ColorClip
    ColorClip(size=(1920, 1080), color=(0,0,0), duration=5).write_videofile(raw_video, fps=24)

print("Testing video processing with intro.jpg...")
success = process_video(raw_video, output_video)

if success and os.path.exists(output_video):
    print("SUCCESS: Output video created.")
    # Optional: Verify duration if possible, but existence is a good first step.
else:
    print("FAILURE: output video not created.")
