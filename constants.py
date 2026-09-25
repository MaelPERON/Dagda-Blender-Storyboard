import os

# Folders
LOCAL_DATA = ("%LOCALAPPDATA%/Blender Foundation/Blender/"
              "dagda-blender-storyboard")
VENV = os.path.join(LOCAL_DATA, "venv")

# Files
REQUIREMENTS = os.path.join(__file__, "..", "requirements.txt")

# LISTS
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

# VALUES
LOGGING_LEVEL = "INFO"
