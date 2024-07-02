require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const imageHistoryRoutes = require('./routes/imageHistory');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Database connection
mongoose.connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
    .then(() => {
        console.log('Database connection successful');
    })
    .catch((err) => {
        console.error('Database connection error:', err);
    });

// Routes
app.use('/api/image-history', imageHistoryRoutes);

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
