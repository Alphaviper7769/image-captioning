from flask import Flask, request, jsonify, send_from_directory
from flask_pymongo import PyMongo
from bson import ObjectId
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MONGO_URI"] = "mongodb://localhost:27017/image_database"

mongo = PyMongo(app)

# Ensure the upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files or "caption" not in request.form:
        return jsonify({'message': 'No image or caption part in the request'}), 400
    
    file = request.files["image"]
    caption = request.form["caption"]
    
    if file:
        filename = file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        # Save file metadata and caption to MongoDB
        file_id = mongo.db.images.insert_one({
            "filename": filename,
            "caption": caption,
            "path": filepath
        }).inserted_id
        return jsonify({'message': 'File uploaded successfully', 'file_id': str(file_id)}), 200
    return jsonify({'message': 'File upload failed'}), 400

@app.route("/images", methods=["GET"])
def get_images():
    images = mongo.db.images.find()
    image_list = []
    for img in images:
        image_data = {
            "id": str(img["_id"]),
            "filename": img["filename"],
            "caption": img["caption"],
            "path": img.get("path", "")  # Handle missing 'path' field gracefully
        }
        image_list.append(image_data)
    return jsonify(image_list), 200

@app.route("/image/<filename>", methods=["GET"])
def get_image(filename):
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    except Exception as e:
        return jsonify({'message': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
