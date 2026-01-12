import os
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip

def process_video(raw_video_path, output_path, intro_path="introvideo.mp4", outro_path="intro.jpg"):
    """
    Processes the raw gameplay video:
    - Adds intro (image or video) and outro if they exist.
    - Converts to MP4 (if not already).
    """
    if not os.path.exists(raw_video_path):
        print(f"Error: Raw video {raw_video_path} not found.")
        return False

    try:
        clips = []
        
        # Add Intro
        if os.path.exists(intro_path):
            print(f"Adding intro from {intro_path}...")
            if intro_path.endswith(('.jpg', '.jpeg', '.png')):
                # Create a 6-second video clip from the image
                intro_clip = ImageClip(intro_path).set_duration(6).set_fps(24).resize(newsize=(1920, 1080))
                clips.append(intro_clip)
            else:
                clips.append(VideoFileClip(intro_path).resize(newsize=(1920, 1080)))
        else:
            print("No intro found, skipping.")

        # Add Gameplay
        print("Processing gameplay footage...")
        gameplay = VideoFileClip(raw_video_path).resize(newsize=(1920, 1080))
        # Optional: Trim start/end if needed, or overlay text
        clips.append(gameplay)

        # Add Outro
        if os.path.exists(outro_path):
            print("Adding outro...")
            if outro_path.endswith(('.jpg', '.jpeg', '.png')):
                # Create a 6-second video clip from the image
                outro_clip = ImageClip(outro_path).set_duration(6).set_fps(24).resize(newsize=(1920, 1080))
                clips.append(outro_clip)
            else:
                clips.append(VideoFileClip(outro_path).resize(newsize=(1920, 1080)))
        else:
            print("No outro found, skipping.")

        # Concatenate
        if len(clips) > 1:
            final_clip = concatenate_videoclips(clips, method="compose")
        else:
            final_clip = clips[0]

        # Write Output
        print(f"Writing final video to {output_path}...")
        final_clip.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac", 
            fps=24,
            preset="medium",
            threads=4
        )
        
        # Cleanup
        for clip in clips:
            clip.close()
            
        return True

    except Exception as e:
        print(f"Error processing video: {e}")
        return False
