"""
Script to download sample images for InspireSearch demo.
This will download a small set of images from Unsplash to use as a sample dataset.

Copyright (c) 2025 Nicole LeGuern
Licensed under MIT License with attribution requirements
https://github.com/CodeQueenie/InspireSearch---AI_Powered_Visual_Search_Engine
"""
import os
import requests
import shutil
from tqdm import tqdm

def download_image(url, filename):
    """
    Download an image from a URL and save it to a file.
    
    Args:
        url: URL of the image to download
        filename: Path where the image will be saved
        
    Returns:
        Boolean indicating if the download was successful
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return True
        else:
            print(f"Failed to download {url}: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    """
    Main function to download sample images for the InspireSearch demo.
    
    Creates necessary directories and downloads sample images from Unsplash.
    """
    try:
        # Create dataset directory if it doesn't exist
        dataset_dir = "static/dataset"
        os.makedirs(dataset_dir, exist_ok=True)

        # Create index directory if it doesn't exist
        index_dir = "static/index"
        os.makedirs(index_dir, exist_ok=True)

        # Create placeholder image for upload section
        img_dir = "static/img"
        os.makedirs(img_dir, exist_ok=True)

        # Sample image URLs from Unsplash (free to use)
        # These are various categories to demonstrate visual search
        image_urls = [
            # Nature
            "https://images.unsplash.com/photo-1501854140801-50d01698950b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1469474968028-56623f02e42e?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            
            # Urban/Architecture
            "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1444723121867-7a241cacace9?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1490644658840-3f2e3f8c5625?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1496588152823-86ff7695e68f?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            
            # Food
            "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1484723091739-30a097e8f929?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1498837167922-ddd27525d352?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            
            # People
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1504257432389-52343af06ae3?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
        ]

        # Create a placeholder image
        placeholder_url = "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"

        # Download placeholder image
        print("Downloading placeholder image...")
        placeholder_path = os.path.join(img_dir, "placeholder.png")
        download_image(placeholder_url, placeholder_path)

        # Download sample images
        print(f"Downloading {len(image_urls)} sample images...")
        for i, url in enumerate(tqdm(image_urls)):
            filename = os.path.join(dataset_dir, f"sample_{i+1}.jpg")
            download_image(url, filename)

        print(f"Downloaded {len(image_urls)} images to {dataset_dir}")
        print("You can now run the application with 'python app.py'")
    except Exception as e:
        print(f"Error downloading sample images: {e}")

if __name__ == "__main__":
    main()
