"""
Main Application for Video Generator App
Handles the main application window and orchestrates the video generation process
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import threading
import json
from datetime import datetime

# Import local modules
from config_manager import ConfigManager
from app_gui import ScrollableTextFrame, SceneFrame, SettingsFrame

class VideoGeneratorApp:
    """Main application class for Video Generator App"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Video Generator App")
        self.root.geometry("1000x800")
        
        # Initialize config manager
        self.config_manager = ConfigManager("config.json")
        
        # Ensure output directories exist
        self.config_manager.ensure_directories_exist()
        
        # Create main container
        self.main_container = ctk.CTkFrame(root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tab view
        self.tab_view = ctk.CTkTabview(self.main_container)
        self.tab_view.pack(fill="both", expand=True)
        
        # Create tabs
        self.main_tab = self.tab_view.add("สร้างวิดีโอ")
        self.settings_tab = self.tab_view.add("ตั้งค่า")
        
        # Set up main tab
        self.setup_main_tab()
        
        # Set up settings tab
        self.setup_settings_tab()
        
        # Initialize scenes list
        self.scenes = []
        
        # Status bar
        self.status_bar = ctk.CTkFrame(root, height=25)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_label = ctk.CTkLabel(self.status_bar, text="พร้อมใช้งาน")
        self.status_label.pack(side="left", padx=10)
    
    def setup_main_tab(self):
        """Set up the main tab for video generation"""
        # Topic input frame
        self.topic_frame = ctk.CTkFrame(self.main_tab)
        self.topic_frame.pack(fill="x", padx=10, pady=10)
        
        self.topic_label = ctk.CTkLabel(self.topic_frame, text="หัวข้อวิดีโอ:", font=ctk.CTkFont(size=14))
        self.topic_label.pack(side="left", padx=10)
        
        self.topic_entry = ctk.CTkEntry(self.topic_frame, width=400)
        self.topic_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        self.generate_script_btn = ctk.CTkButton(self.topic_frame, text="สร้างสคริปต์", 
                                               command=self.generate_script)
        self.generate_script_btn.pack(side="right", padx=10)
        
        # Script output frame
        self.script_frame = ctk.CTkFrame(self.main_tab)
        self.script_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.script_label = ctk.CTkLabel(self.script_frame, text="สคริปต์:", font=ctk.CTkFont(size=14))
        self.script_label.pack(anchor="w", padx=10, pady=5)
        
        self.script_text = ScrollableTextFrame(self.script_frame)
        self.script_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Scenes frame (initially hidden)
        self.scenes_container = ctk.CTkScrollableFrame(self.main_tab, label_text="ฉาก")
        
        # Bottom buttons frame
        self.bottom_frame = ctk.CTkFrame(self.main_tab)
        self.bottom_frame.pack(fill="x", padx=10, pady=10)
        
        self.parse_script_btn = ctk.CTkButton(self.bottom_frame, text="แยกฉากจากสคริปต์", 
                                            command=self.parse_script)
        self.parse_script_btn.pack(side="left", padx=10)
        
        self.create_video_btn = ctk.CTkButton(self.bottom_frame, text="สร้างวิดีโอทั้งหมด", 
                                            command=self.create_video)
        self.create_video_btn.pack(side="right", padx=10)
    
    def setup_settings_tab(self):
        """Set up the settings tab"""
        self.settings_frame = SettingsFrame(self.settings_tab, self.config_manager)
        self.settings_frame.pack(fill="both", expand=True)
    
    def generate_script(self):
        """Generate script using Gemini API"""
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาระบุหัวข้อวิดีโอ")
            return
        
        # Update status
        self.status_label.configure(text="กำลังสร้างสคริปต์...")
        
        # In a real implementation, this would call the Gemini API
        # For now, we'll just simulate it with a placeholder
        def mock_generate_script():
            # Simulate API delay
            import time
            time.sleep(2)
            
            # Create a placeholder script based on the topic
            placeholder_script = f"""# สคริปต์วิดีโอ: {topic}

## ฉากที่ 1: บทนำ
**คำพูด**: สวัสดีครับ/ค่ะ วันนี้เราจะมาพูดถึงเรื่อง{topic}กัน ซึ่งเป็นหัวข้อที่น่าสนใจมากในปัจจุบัน
**ภาพ**: ภาพหน้าปกที่แสดงถึง{topic} พร้อมชื่อเรื่องที่น่าสนใจ

## ฉากที่ 2: ความสำคัญ
**คำพูด**: {topic}มีความสำคัญอย่างมากเพราะเป็นเรื่องที่เกี่ยวข้องกับชีวิตประจำวันของเราทุกคน
**ภาพ**: ภาพแสดงให้เห็นถึงความสำคัญของ{topic} ในชีวิตประจำวัน

## ฉากที่ 3: ประโยชน์
**คำพูด**: ประโยชน์ของ{topic}มีมากมาย ไม่ว่าจะเป็นการช่วยให้ชีวิตสะดวกสบายขึ้น ประหยัดเวลา และเพิ่มประสิทธิภาพในการทำงาน
**ภาพ**: ภาพแสดงประโยชน์ต่างๆ ของ{topic}

## ฉากที่ 4: สรุป
**คำพูด**: สรุปแล้ว {topic}เป็นเรื่องที่น่าสนใจและมีประโยชน์มากมาย หวังว่าวิดีโอนี้จะช่วยให้คุณเข้าใจเรื่อง{topic}มากขึ้นนะครับ/คะ
**ภาพ**: ภาพสรุปเนื้อหาทั้งหมดของ{topic} พร้อมข้อความขอบคุณผู้ชม"""
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.script_text.insert_text(placeholder_script))
            self.root.after(0, lambda: self.status_label.configure(text="สร้างสคริปต์เสร็จสิ้น"))
        
        # Run in a separate thread to avoid freezing the UI
        threading.Thread(target=mock_generate_script).start()
    
    def parse_script(self):
        """Parse script into scenes"""
        script_text = self.script_text.get_text()
        if not script_text:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบสคริปต์ กรุณาสร้างสคริปต์ก่อน")
            return
        
        # Clear existing scenes
        for widget in self.scenes_container.winfo_children():
            widget.destroy()
        self.scenes = []
        
        # Show scenes container
        self.scenes_container.pack(fill="both", expand=True, padx=10, pady=10, before=self.bottom_frame)
        
        # Simple parsing logic (in a real app, this would be more robust)
        import re
        scene_pattern = r"## ฉากที่ (\d+): (.+?)\n\*\*คำพูด\*\*: (.+?)\n\*\*ภาพ\*\*: (.+?)(?=\n\n|$)"
        matches = re.findall(scene_pattern, script_text, re.DOTALL)
        
        if not matches:
            messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถแยกฉากจากสคริปต์ได้ กรุณาตรวจสอบรูปแบบสคริปต์")
            return
        
        # Create scene frames
        for i, (scene_num, title, speech, description) in enumerate(matches):
            scene_frame = SceneFrame(self.scenes_container, scene_id=i)
            scene_frame.pack(fill="x", expand=True, padx=5, pady=10)
            
            # Set scene data
            scene_frame.speech_text.insert("1.0", speech.strip())
            scene_frame.desc_text.insert("1.0", description.strip())
            
            self.scenes.append(scene_frame)
        
        self.status_label.configure(text=f"แยกฉากเสร็จสิ้น พบทั้งหมด {len(self.scenes)} ฉาก")
    
    def create_video(self):
        """Create video from all scenes"""
        if not self.scenes:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบฉาก กรุณาแยกฉากจากสคริปต์ก่อน")
            return
        
        # Check if all scenes have images and audio
        # In a real implementation, this would check if files actually exist
        
        # Update status
        self.status_label.configure(text="กำลังสร้างวิดีโอ...")
        
        # In a real implementation, this would call the media processor
        # For now, we'll just simulate it
        def mock_create_video():
            # Simulate processing delay
            import time
            time.sleep(3)
            
            # Generate a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"video_{timestamp}.mp4"
            output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                     "generated_content", "videos", filename)
            
            # Update UI in the main thread
            self.root.after(0, lambda: messagebox.showinfo("สร้างวิดีโอเสร็จสิ้น", 
                                                        f"สร้างวิดีโอเสร็จสิ้น\nบันทึกไฟล์ที่: {output_path}"))
            self.root.after(0, lambda: self.status_label.configure(text="สร้างวิดีโอเสร็จสิ้น"))
        
        # Run in a separate thread to avoid freezing the UI
        threading.Thread(target=mock_create_video).start()


def main():
    """Main function to run the application"""
    # Set up the root window
    root = ctk.CTk()
    app = VideoGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
