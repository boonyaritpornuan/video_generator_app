"""
Configuration Manager for Video Generator App
Handles reading and writing configuration settings
"""

import os
import json
import configparser
from pathlib import Path

class ConfigManager:
    """Manages application configuration settings"""
    
    DEFAULT_CONFIG = {
        "service_account_key_path": "",
        "project_id": "",
        "location": "us-central1",
        "image_width": 1080,
        "image_height": 1920,
        "video_fps": 30,
        "default_tts_voice": "th-TH-Neural2-C",
        "default_image_style_prompt": "ภาพถ่ายสมจริง, แสงสวยงาม, มุมกล้องระดับสายตา",
        "output_paths": {
            "scripts": "generated_content/scripts",
            "images": "generated_content/images",
            "audios": "generated_content/audios",
            "videos": "generated_content/videos"
        }
    }
    
    def __init__(self, config_file_path="config.json"):
        """Initialize with path to config file"""
        self.config_file_path = config_file_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or create default if not exists"""
        if os.path.exists(self.config_file_path):
            try:
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"Error loading config file: {e}")
                return self._create_default_config()
        else:
            return self._create_default_config()
    
    def _create_default_config(self):
        """Create and save default configuration"""
        self.save_config(self.DEFAULT_CONFIG)
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config file: {e}")
            return False
    
    def get_config(self):
        """Get current configuration"""
        return self.config
    
    def update_config(self, key, value):
        """Update a specific configuration value"""
        # Handle nested keys with dot notation (e.g., "output_paths.scripts")
        if "." in key:
            main_key, sub_key = key.split(".", 1)
            if main_key in self.config and isinstance(self.config[main_key], dict):
                self.config[main_key][sub_key] = value
            else:
                print(f"Invalid config key: {key}")
                return False
        else:
            self.config[key] = value
        
        return self.save_config()
    
    def get_full_path(self, path_key):
        """Get absolute path for a relative output path"""
        if path_key not in self.config["output_paths"]:
            return None
        
        # Get the base directory of the application
        base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        relative_path = self.config["output_paths"][path_key]
        
        return os.path.join(base_dir, relative_path)
    
    def ensure_directories_exist(self):
        """Ensure all output directories exist"""
        for path_key in self.config["output_paths"]:
            full_path = self.get_full_path(path_key)
            os.makedirs(full_path, exist_ok=True)


# Example usage
if __name__ == "__main__":
    config_manager = ConfigManager()
    print("Current configuration:")
    print(json.dumps(config_manager.get_config(), indent=2, ensure_ascii=False))
    
    # Ensure directories exist
    config_manager.ensure_directories_exist()
