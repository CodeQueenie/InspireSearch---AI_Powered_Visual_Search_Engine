"""
InspireSearch - AI-Powered Visual Search Engine
Main Flask application file

Copyright (c) 2025 Nicole LeGuern
Licensed under MIT License with attribution requirements
https://github.com/CodeQueenie/InspireSearch---AI_Powered_Visual_Search_Engine
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from app.image_search import ImageSearch
from app.utils import allowed_file, save_uploaded_file, get_relative_path

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload size

# Create upload folder if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize the image search engine
search_engine = ImageSearch(index_path="static/index", dataset_path="static/dataset")

@app.route("/")
def index():
    """
    Render the home page.
    
    Returns:
        Rendered index.html template
    """
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    """
    Handle image upload and search.
    
    Returns:
        Rendered results.html template with search results
        or redirects back to the upload page if there's an error
    """
    try:
        # Check if a file was uploaded
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]
        
        # Check if the file is empty
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        
        # Check if the file has an allowed extension
        if not allowed_file(file.filename):
            flash("Invalid file type. Please upload a PNG or JPEG image.")
            return redirect(request.url)
        
        # Save the uploaded file
        file_path = save_uploaded_file(file, app.config["UPLOAD_FOLDER"])
        if not file_path:
            flash("Error saving uploaded file")
            return redirect(request.url)
        
        # Check if the index exists, if not, build it
        if search_engine.index is None:
            if not os.path.exists(search_engine.index_file):
                flash("Building image index for the first time. This may take a moment...")
                search_engine.build_index()
            else:
                search_engine.load_index()
        
        # Search for similar images
        results = search_engine.search(file_path, top_k=5)
        
        # Process results for display
        processed_results = []
        
        # Find the maximum distance to normalize similarity scores
        max_distance = 0
        for result in results:
            max_distance = max(max_distance, result["distance"])
        
        # Ensure we don't divide by zero
        if max_distance == 0:
            max_distance = 1
            
        for result in results:
            # Get the relative path for use in templates
            relative_path = get_relative_path(result["path"])
            
            # Convert distance to similarity score (0-100%)
            # Lower distance means higher similarity
            similarity = 100 * (1 - (result["distance"] / max_distance))
            
            processed_results.append({
                "path": relative_path,
                "distance": result["distance"],
                "similarity": round(similarity, 1)  # Round to 1 decimal place
            })
        
        # Get the relative path of the query image
        query_image = get_relative_path(file_path)
        
        return render_template("results.html", 
                              query_image=query_image, 
                              results=processed_results)
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for("index"))

@app.route("/about")
def about():
    """
    Render the about page.
    
    Returns:
        Rendered about.html template
    """
    return render_template("about.html")

@app.errorhandler(413)
def too_large(e):
    """
    Handle file too large error.
    
    Args:
        e: The error object
        
    Returns:
        Redirect to the index page with an error message
    """
    flash("File too large. Maximum size is 16MB.")
    return redirect(url_for("index"))

@app.errorhandler(500)
def server_error(e):
    """
    Handle server error.
    
    Args:
        e: The error object
        
    Returns:
        Redirect to the index page with an error message
    """
    flash("An error occurred while processing your request.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    try:
        # Check if we have sample images in the dataset folder
        dataset_path = "static/dataset"
        if not os.path.exists(dataset_path) or not os.listdir(dataset_path):
            print("Warning: No images found in the dataset folder. Please add some images to 'static/dataset'.")
        
        # Check if we have an index, if not, build it if there are images
        if not os.path.exists(search_engine.index_file) and os.path.exists(dataset_path) and os.listdir(dataset_path):
            print("Building image index for the first time. This may take a moment...")
            search_engine.build_index()
        
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting application: {e}")
