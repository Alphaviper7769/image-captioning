import os
import asyncio
from flask import Flask, request, jsonify, send_file
from flask_pymongo import PyMongo
from gridfs import GridFS
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Dropout, Dense, Embedding, LSTM, add
from tensorflow.keras.utils import plot_model
from bson import ObjectId
from io import BytesIO
import numpy as np
from deep_translator import GoogleTranslator
import pickle

from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:5173'])
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MONGO_URI"] = "mongodb://localhost:27017/image_database"
mongo = PyMongo(app)
fs = GridFS(mongo.db)



# directory=os.path.join("static/uploads",'file.jpg')
# Load VGG16 model on startup

def load_vgg16_model():
    global model_VGG16
    model_VGG16 = VGG16()
    model_VGG16 = Model(inputs=model_VGG16.inputs, outputs=model_VGG16.layers[-2].output)
    print("VGG16 model loaded")
    print(model_VGG16.summary())



# Extract features using VGG16
def extract_vgg16_features(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    features = model_VGG16.predict(image)
    return features

# Load the tokenizer from the pickle file
def load_tokenizer():
    with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    return tokenizer

# Load the tokenizer when the application starts
tokenizer = load_tokenizer()

def load_model():
    # Define the encoder model
 # Image feature layers
 global model
 vocab_size=len(tokenizer.word_index)+1
 max_length=74
 inputs1 = Input(shape=(4096,), name="image")
 fe1 = Dropout(0.4)(inputs1)
 fe2 = Dense(256, activation='relu')(fe1)

 # Sequence feature layers
 inputs2 = Input(shape=(max_length,), name="text")
 se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
 se2 = Dropout(0.4)(se1)
 # Disable cuDNN in LSTM to handle non-right-padded sequences
 se3 = LSTM(256,use_cudnn=False)(se2)

 # Decoder model
 decoder1 = add([fe2, se3])
 decoder2 = Dense(256, activation='relu')(decoder1)
 outputs = Dense(vocab_size, activation='softmax')(decoder2)

 model = Model(inputs=[inputs1, inputs2], outputs=outputs)
 model.compile(loss='categorical_crossentropy', optimizer='adam')

 # Plot the modelpy
#  plot_model(model, show_shapes=True)

 # Print the model summary
 model.summary()
 
 model.load_weights('model_epoch_20.weights.h5')
#  print(weights_path)

#  load_model()


def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


   

def predict_caption(model, features, tokenizer, max_length):
    # add start tag for generation process
    in_text = 'startseq'
    # iterate over the max length of sequence
    for i in range(max_length):
        # encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad the sequence
        sequence = pad_sequences([sequence], max_length)
        # predict next word
        yhat = model.predict([features, sequence], verbose=0)
        # get index with high probability
        yhat = np.argmax(yhat)
        # convert index to word
        word = idx_to_word(yhat, tokenizer)
        # stop if word not found
        if word is None:
            break
        # append word as input for generating next word
        in_text += " " + word
        # stop if we reach end tag
        if word == 'endseq':
            break
      
    return in_text

@app.route("/")
def index():
    return "Upload endpoint at /upload, retrieve endpoint at /images, and generate features endpoint at /generate_features/<image_id>"


@app.route("/tokenizer", methods=["GET"])
def provide_tokenizer():
    tokenizer_json = tokenizer.to_json()
    return jsonify({"tokenizer": tokenizer_json})

# Ensure the upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return jsonify({'message': 'No image or caption part in the request'}), 400
    
    file = request.files["image"]
    # caption = request.form["caption"]
    
    if file:
        filename = file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        # Save file metadata and caption to MongoDB
        file_id = mongo.db.images.insert_one({
            "filename": filename,
            # "caption": caption,
            "path": filepath
        }).inserted_id
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
        return jsonify({'message': 'Features not generated and stored successfully'}), 400

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

@app.route("/image/<image_id>", methods=["GET"])
def get_image(image_id):
    try:
        file_id = ObjectId(image_id)
        image = fs.get(file_id)
        return send_file(BytesIO(image.read()), mimetype='image/jpeg', as_attachment=True, attachment_filename=image.filename)
    except Exception as e:
        return str(e), 400

@app.route("/predict_caption/<image_id>", methods=["GET"])
def predict_caption_route(image_id):
    try:
        file_id = ObjectId(image_id)
        image_doc = mongo.db.images.find_one({"_id": file_id})
        if image_doc is None:
            return jsonify({'message': 'Image not found'}), 404

        temp_path = image_doc["path"]
        features = extract_vgg16_features(temp_path)
        
        caption = predict_caption(model, features, tokenizer, 74)
        
        return jsonify({'caption': caption}), 200
    except Exception as e:
        return jsonify({'caption': "error occured"}), 400
    
@app.route("/translate/<caption>",methods=["GET"])
def caption_translate(caption,lang='hi'):
    try:
        t=GoogleTranslator(source='auto', target=lang).translate(caption) 
        return jsonify({'caption': t}), 200
    except Exception as e:
        return jsonify({'caption': "error occured"}), 400
    
if __name__ == "__main__":
    load_vgg16_model()  # Load VGG16 model
    load_model()
    
    app.run(debug=True)
