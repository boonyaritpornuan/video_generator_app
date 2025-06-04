"""
Text-to-Speech Client Module for Video Generator App
Handles interactions with Google Cloud Text-to-Speech API
"""

import os
from google.cloud import texttospeech

class TTSClient:
    """Client for interacting with Google Cloud Text-to-Speech API"""
    
    def __init__(self, project_id):
        """Initialize the TTS client with project ID"""
        self.project_id = project_id
        self.client = texttospeech.TextToSpeechClient()
    
    def generate_audio_for_scene(self, text_to_speak, voice_config, output_path):
        """Generate audio for a scene and return the path and duration"""
        try:
            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)
            
            # Parse voice config
            voice_name = voice_config.get("name", "th-TH-Neural2-C")
            voice_language = voice_name.split("-")[0] + "-" + voice_name.split("-")[1]
            
            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_language,
                name=voice_name,
            )
            
            # Select the type of audio file
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=voice_config.get("speaking_rate", 1.0),
                pitch=voice_config.get("pitch", 0.0),
            )
            
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            
            # Write the response to the output file
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            
            # Get audio duration (in a real implementation, we would use a library like pydub)
            # For now, we'll estimate based on character count and speaking rate
            # This is a very rough estimate and should be replaced with actual duration calculation
            char_count = len(text_to_speak)
            estimated_duration = (char_count / 15) * (1 / voice_config.get("speaking_rate", 1.0))
            
            return {
                "path": output_path,
                "duration": estimated_duration
            }
        
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            raise
    
    def list_available_voices(self, language_code=None):
        """List available voices, optionally filtered by language code"""
        try:
            # List all available voices
            response = self.client.list_voices(language_code=language_code)
            voices = []
            
            for voice in response.voices:
                voices.append({
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz
                })
            
            return voices
        
        except Exception as e:
            print(f"Error listing voices: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    import os
    
    # Set environment variable for authentication
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service_account_key.json"
    
    # Create client
    client = TTSClient("your-project-id")
    
    # Generate audio
    output_path = "generated_content/audios/test_audio.mp3"
    result = client.generate_audio_for_scene(
        "สวัสดีครับ นี่คือการทดสอบการสร้างเสียงด้วย Google Cloud Text-to-Speech API",
        {"name": "th-TH-Neural2-C", "speaking_rate": 1.0, "pitch": 0.0},
        output_path
    )
    print(f"Audio saved to {result['path']} with duration {result['duration']} seconds")
    
    # List available Thai voices
    voices = client.list_available_voices("th-TH")
    print(f"Available Thai voices: {voices}")
