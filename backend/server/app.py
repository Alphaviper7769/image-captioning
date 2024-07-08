
import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
CORS(app, origins=['http://127.0.0.1:5173'])

class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return User(str(user["_id"]), user["username"], user["email"], user["password"])
        return None

    @staticmethod
    def get_by_email(email):
        user = mongo.db.users.find_one({"email": email})
        if user:
            return User(str(user["_id"]), user["username"], user["email"], user["password"])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/',methods=['GET'])
def first():
    return jsonify({'message': 'Welcome to the Image Captioning API'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    mongo.db.users.insert_one(user)
    return jsonify({'message': 'User registered successfully','success': True})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.get_by_email(email)
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful','success': True})
    else:
        return jsonify({'message': 'Login Unsuccessful. Please check email and password','success':False}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

@app.route('/home')
@login_required
def home():
    return jsonify({'message': f'Welcome, {current_user.username}!'})

if __name__ == '__main__':
    app.run(debug=True)
