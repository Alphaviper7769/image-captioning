from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# on startup of server
def load_model():
    global model_VGG16
    model_VGG16 = VGG16()
    model_VGG16 = Model(inputs=model_VGG16.inputs, outputs=model_VGG16.layers[-2].output)
    print("VGG16 model loaded")
    print(model_VGG16.summary())


# on request
def get_features(image_path):
    image = load_img(image_path, target_size=(224, 224))
    #convert the image pixels to a numpy array
    image = img_to_array(image)
    # Reshape data for model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # Preprocess image for VGG
    image = preprocess_input(image)
    # Extract features
    feature = model_VGG16.predict(image, verbose=0)
    return feature