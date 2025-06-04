"""
Gemini Client Module for Video Generator App
Handles interactions with Google's Gemini API via Vertex AI
"""

import os
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part

class GeminiClient:
    """Client for interacting with Google's Gemini API"""
    
    def __init__(self, project_id, location):
        """Initialize the Gemini client with project and location"""
        self.project_id = project_id
        self.location = location
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
    
    def generate_script(self, topic):
        """Generate a video script based on the given topic"""
        # Create the prompt for script generation
        prompt = f"""
        สร้างสคริปต์วิดีโอเกี่ยวกับ "{topic}" โดยแบ่งเป็นฉากๆ ในรูปแบบต่อไปนี้:
        
        # สคริปต์วิดีโอ: {topic}
        
        ## ฉากที่ 1: [ชื่อฉาก]
        **คำพูด**: [คำพูดสำหรับฉากนี้]
        **ภาพ**: [คำอธิบายภาพที่ควรแสดงในฉากนี้]
        
        ## ฉากที่ 2: [ชื่อฉาก]
        **คำพูด**: [คำพูดสำหรับฉากนี้]
        **ภาพ**: [คำอธิบายภาพที่ควรแสดงในฉากนี้]
        
        (ทำต่อไปจนครบประมาณ 4-6 ฉาก)
        
        คำแนะนำเพิ่มเติม:
        - แต่ละฉากควรมีความยาวคำพูดประมาณ 2-4 ประโยค
        - คำอธิบายภาพควรมีรายละเอียดเพียงพอสำหรับการสร้างภาพ
        - เนื้อหาควรมีความต่อเนื่องและครอบคลุมประเด็นสำคัญของหัวข้อ
        """
        
        # Call Gemini API
        model = GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        
        return response.text
    
    def generate_image_prompt_for_scene(self, scene_description, image_style_config):
        """Generate an image prompt for Imagen based on scene description"""
        # Create the prompt for image prompt generation
        prompt = f"""
        ฉันต้องการสร้าง prompt ภาษาอังกฤษสำหรับ text-to-image AI เพื่อสร้างภาพจากคำอธิบายนี้:
        
        "{scene_description}"
        
        สไตล์ภาพที่ต้องการ: {image_style_config}
        
        โปรดสร้าง prompt ที่มีรายละเอียดมากพอสำหรับ AI สร้างภาพ โดยระบุ:
        - สิ่งที่ต้องการให้แสดงในภาพ
        - มุมมองกล้อง
        - แสงและบรรยากาศ
        - สไตล์ภาพ
        - รายละเอียดอื่นๆ ที่จำเป็น
        
        ให้ตอบเฉพาะ prompt ภาษาอังกฤษเท่านั้น ไม่ต้องมีคำอธิบายเพิ่มเติม
        """
        
        # Call Gemini API
        model = GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        
        return response.text
    
    def parse_script(self, script_text):
        """Parse script text into structured scene data"""
        # Create the prompt for script parsing
        prompt = f"""
        โปรดแยกสคริปต์วิดีโอต่อไปนี้เป็นฉากๆ และส่งกลับในรูปแบบ JSON:
        
        {script_text}
        
        โครงสร้าง JSON ที่ต้องการ:
        ```json
        [
          {{
            "scene_number": 1,
            "title": "ชื่อฉาก",
            "speech": "คำพูดสำหรับฉากนี้",
            "description": "คำอธิบายภาพที่ควรแสดงในฉากนี้"
          }},
          {{
            "scene_number": 2,
            "title": "ชื่อฉาก",
            "speech": "คำพูดสำหรับฉากนี้",
            "description": "คำอธิบายภาพที่ควรแสดงในฉากนี้"
          }}
        ]
        ```
        
        ให้ตอบเฉพาะ JSON เท่านั้น ไม่ต้องมีคำอธิบายเพิ่มเติม
        """
        
        # Call Gemini API
        model = GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        
        # In a real implementation, we would parse the JSON response
        # For now, we'll just return the text
        return response.text


# Example usage
if __name__ == "__main__":
    import os
    
    # Set environment variable for authentication
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service_account_key.json"
    
    # Create client
    client = GeminiClient("your-project-id", "us-central1")
    
    # Generate script
    script = client.generate_script("การเรียนรู้ภาษาอังกฤษด้วยตนเอง")
    print(script)
    
    # Generate image prompt
    image_prompt = client.generate_image_prompt_for_scene(
        "ภาพแสดงคนกำลังเรียนภาษาอังกฤษด้วยแอพพลิเคชันบนโทรศัพท์มือถือ",
        "ภาพถ่ายสมจริง, แสงสวยงาม, มุมกล้องระดับสายตา"
    )
    print(image_prompt)
