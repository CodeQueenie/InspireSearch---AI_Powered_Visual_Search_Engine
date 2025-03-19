"""
InspireSearch - AI-Powered Visual Search Engine
Script to index images in the dataset directory

Copyright (c) 2025 Nicole LeGuern
Licensed under MIT License with attribution requirements
https://github.com/CodeQueenie/InspireSearch---AI_Powered_Visual_Search_Engine
"""
import os
import argparse
from tqdm import tqdm
from image_search import ImageSearch

def main():
    """
    Main function to index images for InspireSearch.
    
    Parses command line arguments and builds the image index.
    """
    try:
        parser = argparse.ArgumentParser(description="Index images for InspireSearch")
        parser.add_argument("--dataset", type=str, default="../static/dataset",
                            help="Path to the dataset directory")
        parser.add_argument("--index", type=str, default="../static/index",
                            help="Path to save the index")
        args = parser.parse_args()

        # Create the index directory if it doesn't exist
        os.makedirs(args.index, exist_ok=True)
        
        print(f"Indexing images from {args.dataset}")
        
        # Initialize the image search engine
        search_engine = ImageSearch(index_path=args.index, dataset_path=args.dataset)
        
        # Build the index
        success = search_engine.build_index()
        
        if success:
            print("Indexing completed successfully!")
        else:
            print("Indexing failed. Check the logs for details.")
    except Exception as e:
        print(f"Error during indexing: {e}")

if __name__ == "__main__":
    main()
