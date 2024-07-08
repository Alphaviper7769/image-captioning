import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from gridfs import GridFS
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from bson import ObjectId
from io import BytesIO

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/image_database"
mongo = PyMongo(app)
fs = GridFS(mongo.db)

# Load VGG16 model on startup
def load_model():
    global model_VGG16
    model_VGG16 = VGG16()
    model_VGG16 = Model(inputs=model_VGG16.inputs, outputs=model_VGG16.layers[-2].output)
    print("VGG16 model loaded")
    print(model_VGG16.summary())

# Extract features using VGG16
def get_features(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    feature = model_VGG16.predict(image, verbose=0)
    return feature

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
        # Save the file temporarily to extract features
        temp_path = f"temp_{file.filename}"
        file.save(temp_path)
        features = get_features(temp_path)
        os.remove(temp_path)
        mongo.db.image_features.insert_one({
            "image_id": file_id,
            "features": features.tolist()
        })
        return jsonify({'message': 'File uploaded and features extracted successfully'}), 200
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
    load_model()  # Load the VGG16 model when the server starts
    app.run(debug=True)
