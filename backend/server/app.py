from flask import Flask, request, jsonify
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')  # Upload folder for images
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Load VGG16 model for feature extraction
vgg_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

@app.route('/extract_features', methods=['POST'])
def extract_features():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # Check if the file is an image
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'})

    try:
        # Save the uploaded file to the static folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Read and preprocess the image
        img = load_img(filename, target_size=(224, 224))
        img = img_to_array(img)  # Convert image to numpy array
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        img = preprocess_input(img)  # Preprocess image for VGG16

        # Extract features using VGG16
        features = vgg_model.predict(img)
        features = features.flatten()  # Flatten features to a 1D array for simplicity

        # Convert to list for JSON serialization
        features_list = features.tolist()

        return jsonify({'features': features_list})

    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.run(debug=True)
