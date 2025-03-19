"""
InspireSearch - AI-Powered Visual Search Engine
Utility functions for file handling and image processing

Copyright (c) 2025 Nicole LeGuern
Licensed under MIT License with attribution requirements
https://github.com/CodeQueenie/InspireSearch---AI_Powered_Visual_Search_Engine
"""
import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    """
    Check if the file has an allowed extension.
    
    Args:
        filename: Name of the file to check
        
    Returns:
        Boolean indicating if the file has an allowed extension
    """
    try:
        return "." in filename and \
               filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    except Exception as e:
        print(f"Error checking file extension: {e}")
        return False

def save_uploaded_file(file, upload_folder):
    """
    Save an uploaded file with a secure filename.
    
    Args:
        file: The uploaded file object
        upload_folder: Directory to save the file in
        
    Returns:
        Path to the saved file
    """
    try:
        # Create the upload folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
        
        # Generate a secure filename with a UUID to avoid collisions
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Save the file
        file.save(file_path)
        
        return file_path
    except Exception as e:
        print(f"Error saving uploaded file: {e}")
        return None

def get_relative_path(absolute_path):
    """
    Convert an absolute path to a relative path for use in templates.
    
    Args:
        absolute_path: Absolute path to convert
        
    Returns:
        Relative path for use in templates
    """
    try:
        # Replace backslashes with forward slashes for web paths
        path = absolute_path.replace("\\", "/")
        
        # Extract the part of the path after 'static/'
        if "static/" in path:
            return path.split("static/", 1)[1]
        elif "static\\" in path:
            return path.split("static\\", 1)[1]
        
        return path
    except Exception as e:
        print(f"Error converting path: {e}")
        return absolute_path
