"""
InspireSearch - AI-Powered Visual Search Engine
Core image search functionality

Copyright (c) 2025 Nicole LeGuern
Licensed under MIT License with attribution requirements
https://github.com/CodeQueenie/InspireSearch---AI_Powered_Visual_Search_Engine
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
import faiss
from PIL import Image
import pickle

class ImageSearch:
    def __init__(self, index_path="static/index", dataset_path="static/dataset"):
        """
        Initialize the image search engine.
        
        Args:
            index_path: Path to save/load the Faiss index and metadata
            dataset_path: Path to the dataset images
        """
        self.index_path = index_path
        self.dataset_path = dataset_path
        self.index_file = os.path.join(index_path, "faiss_index.bin")
        self.metadata_file = os.path.join(index_path, "metadata.pkl")
        
        try:
            # Load the pre-trained ResNet50 model without the classification layer
            self.model = ResNet50(weights="imagenet", include_top=False, pooling="avg")
            
            # Create the index directory if it doesn't exist
            os.makedirs(index_path, exist_ok=True)
            
            # Initialize the index and metadata
            self.index = None
            self.image_paths = []
            
            # Load the index if it exists
            if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
                self.load_index()
        except Exception as e:
            print(f"Error initializing ImageSearch: {e}")
            raise
        
    def extract_features(self, img_path):
        """
        Extract features from an image using ResNet50.
        
        Args:
            img_path: Path to the image
            
        Returns:
            Feature vector (embedding) for the image
        """
        try:
            img = Image.open(img_path).convert("RGB")
            img = img.resize((224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            features = self.model.predict(x)
            return features.flatten()
        except Exception as e:
            print(f"Error extracting features from {img_path}: {e}")
            return None
    
    def build_index(self):
        """
        Build a Faiss index from all images in the dataset directory.
        
        Returns:
            Boolean indicating if the index was successfully built
        """
        try:
            # Get all image files from the dataset directory
            image_files = []
            for root, _, files in os.walk(self.dataset_path):
                for file in files:
                    if file.lower().endswith((".png", ".jpg", ".jpeg")):
                        image_files.append(os.path.join(root, file))
            
            if not image_files:
                print(f"No images found in {self.dataset_path}")
                return False
            
            # Extract features for all images
            features_list = []
            valid_paths = []
            
            for img_path in image_files:
                features = self.extract_features(img_path)
                if features is not None:
                    features_list.append(features)
                    valid_paths.append(img_path)
                    
            if not features_list:
                print("No valid features extracted")
                return False
            
            # Convert to numpy array
            features_array = np.array(features_list).astype("float32")
            
            # Create and train the index
            dimension = features_array.shape[1]  # Dimension of the feature vector
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(features_array)
            self.image_paths = valid_paths
            
            # Save the index and metadata
            self.save_index()
            
            print(f"Index built with {len(valid_paths)} images")
            return True
        except Exception as e:
            print(f"Error building index: {e}")
            return False
    
    def save_index(self):
        """
        Save the Faiss index and image paths to disk.
        
        Returns:
            Boolean indicating if the index was successfully saved
        """
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
            
            # Save the Faiss index
            faiss.write_index(self.index, self.index_file)
            
            # Save the image paths
            with open(self.metadata_file, "wb") as f:
                pickle.dump(self.image_paths, f)
                
            print(f"Index saved to {self.index_file}")
            return True
        except Exception as e:
            print(f"Error saving index: {e}")
            return False
    
    def load_index(self):
        """
        Load the Faiss index and image paths from disk.
        
        Returns:
            Boolean indicating if the index was successfully loaded
        """
        try:
            # Load the Faiss index
            self.index = faiss.read_index(self.index_file)
            
            # Load the image paths
            with open(self.metadata_file, "rb") as f:
                self.image_paths = pickle.load(f)
                
            print(f"Index loaded with {len(self.image_paths)} images")
            return True
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def search(self, query_image_path, top_k=5):
        """
        Search for similar images.
        
        Args:
            query_image_path: Path to the query image
            top_k: Number of similar images to return
            
        Returns:
            List of paths to similar images and their distances
        """
        try:
            if self.index is None:
                print("Index not loaded")
                return []
            
            # Extract features from the query image
            query_features = self.extract_features(query_image_path)
            if query_features is None:
                print(f"Could not extract features from {query_image_path}")
                return []
            
            # Reshape for Faiss
            query_features = np.array([query_features]).astype("float32")
            
            # Search the index
            distances, indices = self.index.search(query_features, min(top_k, len(self.image_paths)))
            
            # Get the image paths for the results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.image_paths):
                    results.append({
                        "path": self.image_paths[idx],
                        "distance": float(distances[0][i])
                    })
            
            return results
        except Exception as e:
            print(f"Error searching for similar images: {e}")
            return []
