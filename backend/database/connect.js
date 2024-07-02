require('dotenv').config()
const mongoose = require('mongoose');

const connect = async () => {
    try {
        const connection = await mongoose.connect("mongodb://localhost:27017/ImageCap", { useNewUrlParser: true });
        console.log("Successfully connected to the database.");
    } catch (err) {
        console.log(err);
        process.exit(1);
    }
};

module.exports = connect;