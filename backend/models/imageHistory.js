const mongoose = require('mongoose');

const imageHistorySchema = new mongoose.Schema({
    imageUrl: {
        type: String,
        required: true,
    },
    caption: {
        type: String,
        required: true,
    },
    date: {
        type: Date,
        default: Date.now,
    },
});

const ImageHistory = mongoose.model('ImageHistory', imageHistorySchema);

module.exports = ImageHistory;
