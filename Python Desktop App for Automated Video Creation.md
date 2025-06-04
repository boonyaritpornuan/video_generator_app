# Python Desktop App for Automated Video Creation

This project implements a desktop application that automates video creation using Google Cloud APIs (Gemini, Imagen, and Text-to-Speech) and MoviePy.

## Project Structure

```
video_generator_app/
├── assets/                  # Folder for UI assets and resources
├── generated_content/       # Folder for generated content
│   ├── scripts/             # Generated scripts
│   ├── images/              # Generated images
│   ├── audios/              # Generated audio files
│   └── videos/              # Generated videos
├── gcp_clients/             # Google Cloud API client modules
│   ├── gemini_client.py     # Client for Gemini API
│   ├── imagen_client.py     # Client for Imagen API
│   └── tts_client.py        # Client for Text-to-Speech API
├── app_gui.py               # GUI components
├── config.json              # Configuration file
├── config_manager.py        # Configuration management
├── main_app.py              # Main application entry point
├── media_processor.py       # Video assembly module
└── requirements.txt         # Python dependencies
```

## Setup Instructions

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Google Cloud Setup**:
   - Create a Google Cloud project
   - Enable the following APIs:
     - Vertex AI API (for Gemini and Imagen)
     - Cloud Text-to-Speech API
   - Create a service account with appropriate permissions
   - Download the service account key JSON file

4. **Configure the Application**:
   - Place your service account key file in a secure location
   - Update the configuration in the app's settings tab with:
     - Path to your service account key
     - Your Google Cloud project ID
     - Other settings as needed

## Running the Application

```bash
python main_app.py
```

## Features

- **Script Generation**: Create video scripts using Gemini API
- **Image Generation**: Generate images for each scene using Imagen API
- **Audio Generation**: Create voiceovers using Text-to-Speech API
- **Video Assembly**: Combine images and audio into a complete video
- **User-friendly Interface**: Easy-to-use GUI for managing the entire process

## Implementation Details

### Main Components

1. **Configuration Manager** (`config_manager.py`):
   - Handles reading/writing configuration settings
   - Manages paths for generated content

2. **GUI Components** (`app_gui.py`):
   - Implements the user interface using CustomTkinter
   - Provides frames for script editing, scene management, and settings

3. **Main Application** (`main_app.py`):
   - Entry point for the application
   - Orchestrates the video generation workflow

4. **API Clients** (in `gcp_clients/`):
   - `gemini_client.py`: Handles interactions with Gemini API
   - `imagen_client.py`: Handles interactions with Imagen API
   - `tts_client.py`: Handles interactions with Text-to-Speech API

5. **Media Processor** (`media_processor.py`):
   - Assembles images and audio into videos using MoviePy
