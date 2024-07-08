# Flask Image Captioning API

This API allows users to upload images, generate image features using the VGG16 model, and predict captions for images.

## Setup

1. Ensure you have Python and the required packages installed. You can install the required packages using:
    ```sh
    pip install -r requirements.txt
    ```

2. Make sure MongoDB is running on your local machine.

3. Place the `model_epoch_20.weights.h5` and `tokenizer.pkl` files in the working directory.

4. Ensure the `static/uploads` folder exists or will be created by the Flask application.

## Endpoints

### Index

- **URL:** `/`
- **Method:** `GET`
- **Description:** Provides basic information about the available endpoints.

### Upload File

- **URL:** `/upload`
- **Method:** `POST`
- **Description:** Uploads an image and its caption.
- **Request Parameters:**
    - `image` (form-data): The image file to be uploaded.
    - `caption` (form-data): The caption for the image.
- **Response:**
    - `200 OK`: `{'message': 'File uploaded successfully', 'file_id': '<file_id>'}`
    - `400 Bad Request`: `{'message': 'File upload failed'}`

### Generate Features

- **URL:** `/generate_features/<image_id>`
- **Method:** `GET`
- **Description:** Generates and stores features for a given image.
- **Request Parameters:**
    - `image_id` (URL parameter): The ID of the image for which to generate features.
- **Response:**
    - `200 OK`: `{'message': 'Features generated and stored successfully'}`
    - `400 Bad Request`: Error message

### Get Images

- **URL:** `/images`
- **Method:** `GET`
- **Description:** Retrieves a list of uploaded images and their metadata.
- **Response:**
    - `200 OK`: List of image metadata.

### Get Image

- **URL:** `/image/<image_id>`
- **Method:** `GET`
- **Description:** Retrieves the actual image file.
- **Request Parameters:**
    - `image_id` (URL parameter): The ID of the image to retrieve.
- **Response:**
    - Image file as attachment
    - `400 Bad Request`: Error message

### Predict Caption

- **URL:** `/predict_caption/<image_id>`
- **Method:** `GET`
- **Description:** Predicts the caption for a given image.
- **Request Parameters:**
    - `image_id` (URL parameter): The ID of the image for which to predict the caption.
- **Response:**
    - `200 OK`: `{'caption': '<predicted_caption>'}`
    - `400 Bad Request`: Error message

### Provide Tokenizer

- **URL:** `/tokenizer`
- **Method:** `GET`
- **Description:** Provides the tokenizer in JSON format.
- **Response:**
    - `200 OK`: `{'tokenizer': '<tokenizer_json>'}`

## Running the Application

To run the Flask application, use:
```sh
python vgg16.py



# Flask User Authentication API

This API allows users to register, login, and logout. It also provides a protected route that requires authentication.

## Setup

1. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Environment Variables:**
   Create a `.env` file in the root directory of your project with the following content:
    ```env
    SECRET_KEY=your_secret_key
    MONGO_URI=mongodb://localhost:27017/your_database_name
    ```

3. **Run the Application:**
    ```sh
    python app.py
    ```

## Endpoints

### Register

- **URL:** `/register`
- **Method:** `POST`
- **Description:** Registers a new user.
- **Request Body:**
    ```json
    {
        "username": "user",
        "email": "user@example.com",
        "password": "password"
    }
    ```
- **Response:**
    - `200 OK`: `{'message': 'User registered successfully'}`

### Login

- **URL:** `/login`
- **Method:** `POST`
- **Description:** Logs in a user.
- **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "password"
    }
    ```
- **Response:**
    - `200 OK`: `{'message': 'Login successful'}`
    - `401 Unauthorized`: `{'message': 'Login Unsuccessful. Please check email and password'}`

### Logout

- **URL:** `/logout`
- **Method:** `POST`
- **Description:** Logs out the current user. Requires authentication.
- **Response:**
    - `200 OK`: `{'message': 'Logout successful'}`

### Home

- **URL:** `/home`
- **Method:** `GET`
- **Description:** Protected route that returns a welcome message for the authenticated user.
- **Response:**
    - `200 OK`: `{'message': 'Welcome, <username>!'}`

## Running the Application

To run the Flask application, use:
```sh
python app.py
