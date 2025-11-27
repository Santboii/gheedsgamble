"""Database module for tracking processed posts and bot activity."""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict
import os


class BotDatabase:
    """Manages SQLite database for tracking bot activity."""
    
    def __init__(self, db_path: str = "bot_data.db"):
        """Initialize database connection and create tables if needed.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Table for tracking processed posts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT UNIQUE NOT NULL,
                subreddit TEXT NOT NULL,
                post_title TEXT,
                post_author TEXT,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responded BOOLEAN DEFAULT 0,
                response_id TEXT,
                products_recommended TEXT
            )
        """)
        
        # Table for tracking responses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT NOT NULL,
                response_id TEXT UNIQUE NOT NULL,
                subreddit TEXT NOT NULL,
                response_text TEXT,
                products_mentioned TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES processed_posts(post_id)
            )
        """)
        
        # Table for analytics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE NOT NULL,
                posts_analyzed INTEGER DEFAULT 0,
                responses_posted INTEGER DEFAULT 0,
                subreddits_monitored TEXT
            )
        """)
        
        # Table for opportunities (for dashboard)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                subreddit TEXT NOT NULL,
                author TEXT,
                body TEXT,
                analysis_json TEXT,
                products_json TEXT,
                suggested_response TEXT,
                status TEXT DEFAULT 'new',  -- new, replied, skipped
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def is_post_processed(self, post_id: str) -> bool:
        """Check if a post has already been processed.
        
        Args:
            post_id: Reddit post ID
            
        Returns:
            True if post has been processed, False otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT 1 FROM processed_posts WHERE post_id = ?",
            (post_id,)
        )
        return cursor.fetchone() is not None
    
    def mark_post_processed(
        self,
        post_id: str,
        subreddit: str,
        post_title: str,
        post_author: str,
        responded: bool = False,
        response_id: Optional[str] = None,
        products: Optional[List[str]] = None
    ):
        """Mark a post as processed.
        
        Args:
            post_id: Reddit post ID
            subreddit: Subreddit name
            post_title: Post title
            post_author: Post author username
            responded: Whether bot responded to this post
            response_id: Reddit comment ID if responded
            products: List of product IDs recommended
        """
        cursor = self.conn.cursor()
        products_str = ",".join(products) if products else None
        
        cursor.execute("""
            INSERT OR REPLACE INTO processed_posts 
            (post_id, subreddit, post_title, post_author, responded, response_id, products_recommended)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (post_id, subreddit, post_title, post_author, responded, response_id, products_str))
        
        self.conn.commit()
    
    def add_response(
        self,
        post_id: str,
        response_id: str,
        subreddit: str,
        response_text: str,
        products: List[str]
    ):
        """Record a bot response.
        
        Args:
            post_id: Original post ID
            response_id: Bot's comment ID
            subreddit: Subreddit name
            response_text: Full response text
            products: List of product IDs mentioned
        """
        cursor = self.conn.cursor()
        products_str = ",".join(products)
        
        cursor.execute("""
            INSERT INTO responses 
            (post_id, response_id, subreddit, response_text, products_mentioned)
            VALUES (?, ?, ?, ?, ?)
        """, (post_id, response_id, subreddit, response_text, products_str))
        
        self.conn.commit()
    
    def get_responses_today(self) -> int:
        """Get count of responses posted today.
        
        Returns:
            Number of responses posted today
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM responses 
            WHERE DATE(created_at) = DATE('now')
        """)
        result = cursor.fetchone()
        return result['count'] if result else 0
    
    def get_responses_last_hour(self) -> int:
        """Get count of responses posted in the last hour.
        
        Returns:
            Number of responses in last hour
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM responses 
            WHERE created_at >= datetime('now', '-1 hour')
        """)
        result = cursor.fetchone()
        return result['count'] if result else 0
    
    def get_stats(self) -> Dict:
        """Get overall bot statistics.
        
        Returns:
            Dictionary with bot statistics
        """
        cursor = self.conn.cursor()
        
        # Total posts processed
        cursor.execute("SELECT COUNT(*) as count FROM processed_posts")
        total_processed = cursor.fetchone()['count']
        
        # Total responses
        cursor.execute("SELECT COUNT(*) as count FROM responses")
        total_responses = cursor.fetchone()['count']
        
        # Responses today
        responses_today = self.get_responses_today()
        
        # Most active subreddit
        cursor.execute("""
            SELECT subreddit, COUNT(*) as count 
            FROM responses 
            GROUP BY subreddit 
            ORDER BY count DESC 
            LIMIT 1
        """)
        most_active = cursor.fetchone()
        
        return {
            'total_posts_processed': total_processed,
            'total_responses': total_responses,
            'responses_today': responses_today,
            'most_active_subreddit': dict(most_active) if most_active else None
        }

    def add_opportunity(self, opportunity: Dict):
        """Add a new opportunity to the database.
        
        Args:
            opportunity: Dictionary containing opportunity details
        """
        cursor = self.conn.cursor()
        
        # Convert dicts/lists to JSON strings
        import json
        analysis_json = json.dumps(opportunity.get('analysis', {}))
        routes_json = json.dumps(opportunity.get('recommended_routes', []))
        
        cursor.execute("""
            INSERT OR IGNORE INTO opportunities 
            (post_id, title, url, subreddit, author, body, analysis_json, products_json, suggested_response)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            opportunity['post_id'],
            opportunity['post_title'],
            opportunity['post_url'],
            opportunity['subreddit'],
            opportunity['author'],
            opportunity.get('post_body', ''),
            analysis_json,
            routes_json,
            opportunity['suggested_response']
        ))
        
        self.conn.commit()
    
    def get_opportunities(self, status: str = 'new', limit: int = 50) -> List[Dict]:
        """Get opportunities filtered by status.
        
        Args:
            status: Status to filter by (new, replied, skipped, all)
            limit: Maximum number of results
            
        Returns:
            List of opportunity dictionaries
        """
        cursor = self.conn.cursor()
        
        if status == 'all':
            cursor.execute("""
                SELECT * FROM opportunities 
                ORDER BY created_at DESC LIMIT ?
            """, (limit,))
        else:
            cursor.execute("""
                SELECT * FROM opportunities 
                WHERE status = ? 
                ORDER BY created_at DESC LIMIT ?
            """, (status, limit))
            
        rows = cursor.fetchall()
        results = []
        
        import json
        for row in rows:
            item = dict(row)
            # Parse JSON fields
            try:
                item['analysis'] = json.loads(item['analysis_json']) if item['analysis_json'] else {}
                item['products'] = json.loads(item['products_json']) if item['products_json'] else []
            except:
                item['analysis'] = {}
                item['products'] = []
            results.append(item)
            
        return results
    
    def update_opportunity_status(self, post_id: str, status: str):
        """Update the status of an opportunity.
        
        Args:
            post_id: Reddit post ID
            status: New status (new, replied, skipped)
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE opportunities 
            SET status = ? 
            WHERE post_id = ?
        """, (status, post_id))
        self.conn.commit()
    
    def close(self):
        """Close database connection."""
        self.conn.close()
