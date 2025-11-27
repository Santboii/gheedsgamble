const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;
const DB_PATH = path.resolve(__dirname, '../../bot_data.db');

// Middleware
app.use(cors());
app.use(express.json());

// Database connection
const db = new sqlite3.Database(DB_PATH, (err) => {
    if (err) {
        console.error('Error opening database:', err.message);
    } else {
        console.log('Connected to SQLite database at:', DB_PATH);
    }
});

// Routes

// Get stats
app.get('/api/stats', (req, res) => {
    const stats = {};

    db.serialize(() => {
        // Total processed
        db.get("SELECT COUNT(*) as count FROM processed_posts", (err, row) => {
            if (err) return res.status(500).json({ error: err.message });
            stats.total_processed = row.count;

            // Total responses
            db.get("SELECT COUNT(*) as count FROM responses", (err, row) => {
                if (err) return res.status(500).json({ error: err.message });
                stats.total_responses = row.count;

                // Responses today
                db.get("SELECT COUNT(*) as count FROM responses WHERE DATE(created_at) = DATE('now')", (err, row) => {
                    if (err) return res.status(500).json({ error: err.message });
                    stats.responses_today = row.count;

                    res.json(stats);
                });
            });
        });
    });
});

// Get opportunities
app.get('/api/opportunities', (req, res) => {
    const status = req.query.status || 'new';
    const limit = req.query.limit || 50;

    let query = "SELECT * FROM opportunities WHERE status = ? ORDER BY created_at DESC LIMIT ?";
    let params = [status, limit];

    if (status === 'all') {
        query = "SELECT * FROM opportunities ORDER BY created_at DESC LIMIT ?";
        params = [limit];
    }

    db.all(query, params, (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }

        // Parse JSON fields
        const opportunities = rows.map(row => {
            try {
                row.analysis = JSON.parse(row.analysis_json || '{}');
                row.products = JSON.parse(row.products_json || '[]');
            } catch (e) {
                row.analysis = {};
                row.products = [];
            }
            return row;
        });

        res.json(opportunities);
    });
});

// Update opportunity status
app.post('/api/opportunities/:id/status', (req, res) => {
    const { status } = req.body;
    const { id } = req.params;

    if (!['new', 'replied', 'skipped'].includes(status)) {
        return res.status(400).json({ error: 'Invalid status' });
    }

    db.run("UPDATE opportunities SET status = ? WHERE post_id = ?", [status, id], function (err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ success: true, changes: this.changes });
    });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
