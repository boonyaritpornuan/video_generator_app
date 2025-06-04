"""
GUI Components for Video Generator App
Contains classes and functions for creating the application's user interface
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import json

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ScrollableTextFrame(ctk.CTkFrame):
    """A frame with scrollable text widget"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create a text widget with scrollbar
        self.text_widget = ctk.CTkTextbox(self, wrap="word", height=200)
        self.text_widget.pack(fill="both", expand=True, padx=5, pady=5)
    
    def insert_text(self, text):
        """Insert text into the text widget"""
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", text)
    
    def get_text(self):
        """Get text from the text widget"""
        return self.text_widget.get("1.0", "end-1c")
    
    def clear(self):
        """Clear the text widget"""
        self.text_widget.delete("1.0", "end")


class SceneFrame(ctk.CTkFrame):
    """Frame for displaying and editing a single scene"""
    
    def __init__(self, master, scene_id=0, **kwargs):
        super().__init__(master, **kwargs)
        self.scene_id = scene_id
        
        # Scene header
        self.header_label = ctk.CTkLabel(self, text=f"ฉากที่ {scene_id + 1}", font=ctk.CTkFont(size=16, weight="bold"))
        self.header_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        
        # Speech text
        self.speech_label = ctk.CTkLabel(self, text="คำพูด:")
        self.speech_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.speech_text = ctk.CTkTextbox(self, height=60, width=400)
        self.speech_text.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Scene description
        self.desc_label = ctk.CTkLabel(self, text="คำอธิบายภาพ:")
        self.desc_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.desc_text = ctk.CTkTextbox(self, height=80, width=400)
        self.desc_text.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        # Image prompt
        self.prompt_label = ctk.CTkLabel(self, text="Prompt รูปภาพ:")
        self.prompt_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.prompt_text = ctk.CTkTextbox(self, height=80, width=400)
        self.prompt_text.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # Generate image prompt button
        self.gen_prompt_btn = ctk.CTkButton(self.buttons_frame, text="สร้าง Prompt รูปภาพ", 
                                           command=self.generate_image_prompt)
        self.gen_prompt_btn.pack(side="left", padx=5, pady=5)
        
        # Generate image button
        self.gen_image_btn = ctk.CTkButton(self.buttons_frame, text="สร้างรูปภาพ", 
                                          command=self.generate_image)
        self.gen_image_btn.pack(side="left", padx=5, pady=5)
        
        # Generate audio button
        self.gen_audio_btn = ctk.CTkButton(self.buttons_frame, text="สร้างเสียง", 
                                          command=self.generate_audio)
        self.gen_audio_btn.pack(side="left", padx=5, pady=5)
        
        # Image preview (placeholder)
        self.image_frame = ctk.CTkFrame(self, width=200, height=200)
        self.image_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.image_label = ctk.CTkLabel(self.image_frame, text="[ตัวอย่างรูปภาพจะแสดงที่นี่]")
        self.image_label.pack(expand=True, fill="both")
        
        # Status indicators
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.image_status = ctk.CTkLabel(self.status_frame, text="รูปภาพ: ยังไม่สร้าง", text_color="gray")
        self.image_status.pack(side="left", padx=10)
        
        self.audio_status = ctk.CTkLabel(self.status_frame, text="เสียง: ยังไม่สร้าง", text_color="gray")
        self.audio_status.pack(side="left", padx=10)
        
        # Configure grid column weights
        self.grid_columnconfigure(1, weight=1)
    
    def generate_image_prompt(self):
        """Generate image prompt for the scene"""
        # This would call the Gemini API in the actual implementation
        messagebox.showinfo("สร้าง Prompt", "ฟังก์ชันนี้จะเรียกใช้ Gemini API เพื่อสร้าง Prompt รูปภาพ")
        # Placeholder for demonstration
        scene_desc = self.desc_text.get("1.0", "end-1c")
        if scene_desc:
            placeholder_prompt = f"High quality photograph of {scene_desc}, professional lighting, 8k resolution"
            self.prompt_text.delete("1.0", "end")
            self.prompt_text.insert("1.0", placeholder_prompt)
    
    def generate_image(self):
        """Generate image for the scene"""
        # This would call the Imagen API in the actual implementation
        messagebox.showinfo("สร้างรูปภาพ", "ฟังก์ชันนี้จะเรียกใช้ Imagen API เพื่อสร้างรูปภาพ")
        # Update status
        self.image_status.configure(text="รูปภาพ: สร้างแล้ว ✓", text_color="green")
    
    def generate_audio(self):
        """Generate audio for the scene"""
        # This would call the Text-to-Speech API in the actual implementation
        messagebox.showinfo("สร้างเสียง", "ฟังก์ชันนี้จะเรียกใช้ Text-to-Speech API เพื่อสร้างเสียง")
        # Update status
        self.audio_status.configure(text="เสียง: สร้างแล้ว ✓", text_color="green")
    
    def get_scene_data(self):
        """Get all data for this scene"""
        return {
            "scene_id": self.scene_id,
            "speech": self.speech_text.get("1.0", "end-1c"),
            "description": self.desc_text.get("1.0", "end-1c"),
            "image_prompt": self.prompt_text.get("1.0", "end-1c"),
            "image_path": "",  # Would be populated in actual implementation
            "audio_path": "",  # Would be populated in actual implementation
        }
    
    def set_scene_data(self, data):
        """Set scene data from dictionary"""
        if "speech" in data:
            self.speech_text.delete("1.0", "end")
            self.speech_text.insert("1.0", data["speech"])
        
        if "description" in data:
            self.desc_text.delete("1.0", "end")
            self.desc_text.insert("1.0", data["description"])
        
        if "image_prompt" in data:
            self.prompt_text.delete("1.0", "end")
            self.prompt_text.insert("1.0", data["image_prompt"])


class SettingsFrame(ctk.CTkFrame):
    """Frame for application settings"""
    
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.config_manager = config_manager
        
        # Title
        self.title_label = ctk.CTkLabel(self, text="การตั้งค่า", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 20))
        
        # Service Account Key
        self.key_label = ctk.CTkLabel(self, text="Service Account Key Path:")
        self.key_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.key_frame = ctk.CTkFrame(self)
        self.key_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        self.key_entry = ctk.CTkEntry(self.key_frame, width=300)
        self.key_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.key_button = ctk.CTkButton(self.key_frame, text="Browse", command=self.browse_key_file)
        self.key_button.pack(side="right")
        
        # Project ID
        self.project_label = ctk.CTkLabel(self, text="Project ID:")
        self.project_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.project_entry = ctk.CTkEntry(self, width=300)
        self.project_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        # Location
        self.location_label = ctk.CTkLabel(self, text="Location:")
        self.location_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.location_entry = ctk.CTkEntry(self, width=300)
        self.location_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        
        # Image dimensions
        self.dimensions_frame = ctk.CTkFrame(self)
        self.dimensions_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.width_label = ctk.CTkLabel(self.dimensions_frame, text="Image Width:")
        self.width_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.width_entry = ctk.CTkEntry(self.dimensions_frame, width=100)
        self.width_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        self.height_label = ctk.CTkLabel(self.dimensions_frame, text="Image Height:")
        self.height_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.height_entry = ctk.CTkEntry(self.dimensions_frame, width=100)
        self.height_entry.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        
        # Video FPS
        self.fps_label = ctk.CTkLabel(self, text="Video FPS:")
        self.fps_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.fps_entry = ctk.CTkEntry(self, width=100)
        self.fps_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
        
        # TTS Voice
        self.voice_label = ctk.CTkLabel(self, text="TTS Voice:")
        self.voice_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)
        
        self.voice_var = ctk.StringVar(value="th-TH-Neural2-C")
        self.voice_combobox = ctk.CTkComboBox(self, values=["th-TH-Neural2-C", "th-TH-Neural2-D"], 
                                             variable=self.voice_var, width=300)
        self.voice_combobox.grid(row=6, column=1, sticky="w", padx=10, pady=5)
        
        # Image Style Prompt
        self.style_label = ctk.CTkLabel(self, text="Default Image Style:")
        self.style_label.grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.style_text = ctk.CTkTextbox(self, height=60, width=300)
        self.style_text.grid(row=7, column=1, sticky="ew", padx=10, pady=5)
        
        # Save button
        self.save_button = ctk.CTkButton(self, text="บันทึกการตั้งค่า", command=self.save_settings)
        self.save_button.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Configure grid column weights
        self.grid_columnconfigure(1, weight=1)
        
        # Load current settings
        self.load_settings()
    
    def browse_key_file(self):
        """Open file dialog to select service account key file"""
        filename = filedialog.askopenfilename(
            title="เลือกไฟล์ Service Account Key",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            self.key_entry.delete(0, "end")
            self.key_entry.insert(0, filename)
    
    def load_settings(self):
        """Load settings from config manager"""
        config = self.config_manager.get_config()
        
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, config.get("service_account_key_path", ""))
        
        self.project_entry.delete(0, "end")
        self.project_entry.insert(0, config.get("project_id", ""))
        
        self.location_entry.delete(0, "end")
        self.location_entry.insert(0, config.get("location", "us-central1"))
        
        self.width_entry.delete(0, "end")
        self.width_entry.insert(0, str(config.get("image_width", 1080)))
        
        self.height_entry.delete(0, "end")
        self.height_entry.insert(0, str(config.get("image_height", 1920)))
        
        self.fps_entry.delete(0, "end")
        self.fps_entry.insert(0, str(config.get("video_fps", 30)))
        
        self.voice_var.set(config.get("default_tts_voice", "th-TH-Neural2-C"))
        
        self.style_text.delete("1.0", "end")
        self.style_text.insert("1.0", config.get("default_image_style_prompt", 
                                               "ภาพถ่ายสมจริง, แสงสวยงาม, มุมกล้องระดับสายตา"))
    
    def save_settings(self):
        """Save settings to config manager"""
        try:
            self.config_manager.update_config("service_account_key_path", self.key_entry.get())
            self.config_manager.update_config("project_id", self.project_entry.get())
            self.config_manager.update_config("location", self.location_entry.get())
            self.config_manager.update_config("image_width", int(self.width_entry.get()))
            self.config_manager.update_config("image_height", int(self.height_entry.get()))
            self.config_manager.update_config("video_fps", int(self.fps_entry.get()))
            self.config_manager.update_config("default_tts_voice", self.voice_var.get())
            self.config_manager.update_config("default_image_style_prompt", self.style_text.get("1.0", "end-1c"))
            
            messagebox.showinfo("บันทึกการตั้งค่า", "บันทึกการตั้งค่าเรียบร้อยแล้ว")
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {str(e)}")
