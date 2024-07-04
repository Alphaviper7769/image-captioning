const mongoose = require("mongoose");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");

const userSchema = new mongoose.Schema({
    name: String,
    email: String,
    password: String,
    tokens: [
        {
            jwtoken: {
                type: String,
                required: true
            }
        }
    ]
});

userSchema.pre("save", async function (next) {
    if (this.isModified("password")) {
        this.password = await bcrypt.hash(this.password, 10);
    }
    next();
});

userSchema.methods.generateAuthToken = async function () {
    try {
        let token = jwt.sign({ _id: this._id }, "translater");
        this.tokens = this.tokens.concat({ jwtoken: token });
        await this.save();
        return token;
    } catch (err) {
        console.log(err);
    }
};

const User = mongoose.model("User", userSchema);

module.exports = User;