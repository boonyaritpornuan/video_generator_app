"""
Media Processor Module for Video Generator App
Handles video assembly from images and audio using MoviePy
"""

import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
import moviepy.config as mp_config

class MediaProcessor:
    """Handles video assembly from images and audio"""
    
    def __init__(self, video_fps=30):
        """Initialize the media processor with video FPS"""
        self.video_fps = video_fps
    
    def create_video_from_scenes(self, scenes_data, output_video_path):
        """Create a video from multiple scenes
        
        Args:
            scenes_data: List of dictionaries with scene information
                Each dictionary should contain:
                - image_path: Path to the image file
                - audio_path: Path to the audio file
                - audio_duration: Duration of the audio in seconds
                - text: (Optional) Text to overlay on the image
            output_video_path: Path to save the output video
        
        Returns:
            Path to the created video file
        """
        try:
            # Create clips for each scene
            clips = []
            
            for scene in scenes_data:
                # Create image clip
                img_clip = ImageClip(scene["image_path"])
                
                # Set duration to match audio
                img_clip = img_clip.set_duration(scene["audio_duration"])
                
                # Add audio
                audio_clip = AudioFileClip(scene["audio_path"])
                img_clip = img_clip.set_audio(audio_clip)
                
                # Add text overlay if provided
                if "text" in scene and scene["text"]:
                    txt_clip = TextClip(
                        scene["text"],
                        font="Arial",
                        fontsize=24,
                        color="white",
                        bg_color="rgba(0,0,0,0.5)",
                        method="caption",
                        size=(img_clip.w, None)
                    )
                    txt_clip = txt_clip.set_position(("center", "bottom")).set_duration(img_clip.duration)
                    img_clip = CompositeVideoClip([img_clip, txt_clip])
                
                clips.append(img_clip)
            
            # Concatenate all clips
            final_clip = concatenate_videoclips(clips)
            
            # Write the result to a file
            final_clip.write_videofile(
                output_video_path,
                fps=self.video_fps,
                codec="libx264",
                audio_codec="aac"
            )
            
            return output_video_path
        
        except Exception as e:
            print(f"Error creating video: {str(e)}")
            raise
    
    def add_background_music(self, video_path, music_path, output_path, music_volume=0.3):
        """Add background music to a video
        
        Args:
            video_path: Path to the input video
            music_path: Path to the music file
            output_path: Path to save the output video
            music_volume: Volume of the background music (0.0 to 1.0)
        
        Returns:
            Path to the created video file
        """
        try:
            from moviepy.editor import VideoFileClip, AudioFileClip
            
            # Load video and music
            video = VideoFileClip(video_path)
            music = AudioFileClip(music_path)
            
            # Loop music if it's shorter than the video
            if music.duration < video.duration:
                music = music.loop(duration=video.duration)
            else:
                # Trim music if it's longer than the video
                music = music.subclip(0, video.duration)
            
            # Set music volume
            music = music.volumex(music_volume)
            
            # Mix audio
            final_audio = video.audio.set_start(0).volumex(1.0)
            final_audio = final_audio.audio_fadeout(3)
            
            # Add music to video
            final_clip = video.set_audio(CompositeAudioClip([final_audio, music.set_start(0)]))
            
            # Write the result to a file
            final_clip.write_videofile(
                output_path,
                fps=self.video_fps,
                codec="libx264",
                audio_codec="aac"
            )
            
            return output_path
        
        except Exception as e:
            print(f"Error adding background music: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    # Create media processor
    processor = MediaProcessor(video_fps=30)
    
    # Example scenes data
    scenes_data = [
        {
            "image_path": "generated_content/images/scene1.png",
            "audio_path": "generated_content/audios/scene1.mp3",
            "audio_duration": 5.0,
            "text": "This is scene 1"
        },
        {
            "image_path": "generated_content/images/scene2.png",
            "audio_path": "generated_content/audios/scene2.mp3",
            "audio_duration": 4.5,
            "text": "This is scene 2"
        }
    ]
    
    # Create video
    output_path = "generated_content/videos/test_video.mp4"
    processor.create_video_from_scenes(scenes_data, output_path)
    print(f"Video created at {output_path}")
    
    # Add background music
    music_path = "assets/background_music.mp3"
    final_path = "generated_content/videos/test_video_with_music.mp4"
    processor.add_background_music(output_path, music_path, final_path, music_volume=0.3)
    print(f"Video with music created at {final_path}")
