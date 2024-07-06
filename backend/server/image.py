from flask import Flask, request, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId
from gridfs import GridFS

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/image_database"
mongo = PyMongo(app)
fs = GridFS(mongo.db)

@app.route("/")
def index():
    return "Upload endpoint at /upload"

@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        print("request.files:", request.files)  # Debugging output
        
        if "image" not in request.files:
            return "No image part in the request", 400
        
        file = request.files["image"]
        if file:
            file_id = fs.put(file, filename=file.filename)
            # Optionally, save other metadata to MongoDB
            mongo.db.images.insert_one({"_id": file_id, "filename": file.filename})
            return "File uploaded successfully", 200
    return "Upload failed", 400

if __name__ == "__main__":
    app.run(debug=True)
