"""
Imagen Client Module for Video Generator App
Handles interactions with Google's Imagen API via Vertex AI
"""

import os
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part
import base64
from PIL import Image
import io

class ImagenClient:
    """Client for interacting with Google's Imagen API"""
    
    def __init__(self, project_id, location):
        """Initialize the Imagen client with project and location"""
        self.project_id = project_id
        self.location = location
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
    
    def generate_image(self, image_prompt, width, height, output_path):
        """Generate an image based on the given prompt and save it to the output path"""
        try:
            # Call Imagen API
            model = GenerativeModel("imagegeneration@002")
            response = model.generate_content(
                image_prompt,
                generation_config={
                    "width": width,
                    "height": height,
                }
            )
            
            # Extract image data
            if response.candidates and response.candidates[0].content.parts:
                image_part = response.candidates[0].content.parts[0]
                if hasattr(image_part, "file_data") and image_part.file_data:
                    # Save the image to the output path
                    with open(output_path, "wb") as f:
                        f.write(image_part.file_data.file_content)
                    
                    return output_path
            
            raise Exception("Failed to generate image: No image data in response")
        
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise
    
    def generate_image_from_base64(self, base64_image):
        """Convert base64 image data to PIL Image"""
        try:
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            return image
        except Exception as e:
            print(f"Error converting base64 to image: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    import os
    
    # Set environment variable for authentication
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service_account_key.json"
    
    # Create client
    client = ImagenClient("your-project-id", "us-central1")
    
    # Generate image
    output_path = "generated_content/images/test_image.png"
    client.generate_image(
        "A beautiful landscape with mountains and a lake, photorealistic style",
        1080,
        1080,
        output_path
    )
    print(f"Image saved to {output_path}")
