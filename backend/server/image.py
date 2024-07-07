from flask import Flask, request, redirect, url_for, jsonify, send_file
from flask_pymongo import PyMongo
from bson import ObjectId
from gridfs import GridFS
from io import BytesIO

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/image_database"
mongo = PyMongo(app)
fs = GridFS(mongo.db)

@app.route("/")
def index():
    return "Upload endpoint at /upload and retrieve endpoint at /images"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files or "caption" not in request.form:
        return jsonify({'message': 'No image or caption part in the request'}), 400
    
    file = request.files["image"]
    caption = request.form["caption"]
    
    if file:
        file_id = fs.put(file, filename=file.filename)
        # Save file metadata and caption to MongoDB
        mongo.db.images.insert_one({
            "_id": file_id,
            "filename": file.filename,
            "caption": caption
        })
        return jsonify({'message': 'File uploaded successfully'}), 200
    return jsonify({'message': 'File upload failed'}), 400

@app.route("/images", methods=["GET"])
def get_images():
    images = mongo.db.images.find()
    image_list = []
    for img in images:
        image_data = {
            "id": str(img["_id"]),
            "filename": img["filename"],
            "caption": img["caption"]
        }
        image_list.append(image_data)
    return jsonify(image_list), 200

@app.route("/image/<image_id>", methods=["GET"])
def get_image(image_id):
    try:
        file_id = ObjectId(image_id)
        image = fs.get(file_id)
        return send_file(BytesIO(image.read()), mimetype='image/jpeg', as_attachment=True, attachment_filename=image.filename)
    except Exception as e:
        return str(e), 400

if __name__ == "__main__":
    app.run(debug=True)
