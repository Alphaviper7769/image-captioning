import os
from flask import Flask, request, jsonify, send_file
from flask_pymongo import PyMongo
from gridfs import GridFS
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from bson import ObjectId
from io import BytesIO
import numpy as np

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/image_database"
mongo = PyMongo(app)
fs = GridFS(mongo.db)

# Load VGG16 model on startup
def load_vgg16_model():
    global vgg16_model
    vgg16_model = VGG16(weights='imagenet')
    vgg16_model = Model(inputs=vgg16_model.inputs, outputs=vgg16_model.layers[-2].output)
    print("VGG16 model loaded")

# Extract features using VGG16
def extract_vgg16_features(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    features = vgg16_model.predict(image)
    return features

@app.route("/")
def index():
    return "Upload endpoint at /upload, retrieve endpoint at /images, and generate features endpoint at /generate_features/<image_id>"

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
        return jsonify({'message': 'File uploaded successfully', 'file_id': str(file_id)}), 200
    return jsonify({'message': 'File upload failed'}), 400

@app.route("/generate_features/<image_id>", methods=["GET"])
def generate_features(image_id):
    try:
        file_id = ObjectId(image_id)
        image = fs.get(file_id)
        temp_path = f"temp_{image.filename}"
        
        with open(temp_path, 'wb') as f:
            f.write(image.read())
        
        features = extract_vgg16_features(temp_path)
        os.remove(temp_path)
        
        mongo.db.image_features.insert_one({
            "image_id": file_id,
            "features": features.tolist()
        })
        return jsonify({'message': 'Features generated and stored successfully'}), 200
    except Exception as e:
        return str(e), 400

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
    load_vgg16_model()  # Load VGG16 model
    app.run(debug=True)
