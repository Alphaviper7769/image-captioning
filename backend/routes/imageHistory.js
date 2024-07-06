const express = require('express');
const router = express.Router();
const ImageHistory = require('../models/imageHistory');
const { body, validationResult } = require('express-validator');

// Fetch all image history
router.get('/', async (req, res) => {
    try {
        const history = await ImageHistory.find();
        res.status(200).json(history);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// Fetch a single image history entry by ID
router.get('/:id', async (req, res) => {
    try {
        const history = await ImageHistory.findById(req.params.id);
        if (!history) {
            return res.status(404).json({ message: 'Entry not found' });
        }
        res.status(200).json(history);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// Create a new image history entry
router.post(
    '/',
    body('imageUrl').isURL().withMessage('Invalid URL'),
    body('caption').notEmpty().withMessage('Caption is required'),
    async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { imageUrl, caption } = req.body;

        const history = new ImageHistory({
            imageUrl,
            caption,
        });

        try {
            const newHistory = await history.save();
            res.status(201).json(newHistory);
        } catch (error) {
            res.status(400).json({ message: error.message });
        }
    }
);

// Update an existing image history entry
router.put(
    '/:id',
    body('imageUrl').isURL().withMessage('Invalid URL'),
    body('caption').notEmpty().withMessage('Caption is required'),
    async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { imageUrl, caption } = req.body;

        try {
            const updatedHistory = await ImageHistory.findByIdAndUpdate(
                req.params.id,
                { imageUrl, caption },
                { new: true }
            );
            if (!updatedHistory) {
                return res.status(404).json({ message: 'Entry not found' });
            }
            res.status(200).json(updatedHistory);
        } catch (error) {
            res.status(400).json({ message: error.message });
        }
    }
);

// Delete an image history entry
router.delete('/:id', async (req, res) => {
    try {
        const deletedHistory = await ImageHistory.findByIdAndDelete(req.params.id);
        if (!deletedHistory) {
            return res.status(404).json({ message: 'Entry not found' });
        }
        res.status(200).json({ message: 'Entry deleted successfully' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

module.exports = router;
