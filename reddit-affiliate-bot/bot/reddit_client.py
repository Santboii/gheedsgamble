"""Reddit client using public JSON endpoints (No API credentials required)."""

import requests
import logging
import time
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RedditPost:
    """Data class to mimic PRAW Submission object."""
    id: str
    title: str
    selftext: str
    author: str
    permalink: str
    created_utc: float
    subreddit: 'Subreddit'
    comments: List[Dict] = None  # Will be populated if fetched
    
    @property
    def body(self):
        return self.selftext
    
    def get_top_comments(self, max_comments: int = 5) -> str:
        """Get top comments as a single string for context."""
        if not self.comments:
            return ""
        
        comment_texts = []
        for comment in self.comments[:max_comments]:
            author = comment.get('author', '[deleted]')
            body = comment.get('body', '')
            if author not in ['[deleted]', '[removed]', 'AutoModerator'] and body:
                comment_texts.append(f"{author}: {body}")
        
        return "\n".join(comment_texts)

class Subreddit:
    """Data class to mimic PRAW Subreddit object."""
    def __init__(self, display_name: str):
        self.display_name = display_name

class RedditClient:
    """Handles Reddit interactions via public JSON endpoints."""
    
    BASE_URL = "https://www.reddit.com"
    
    def __init__(self):
        """Initialize Reddit client."""
        # Use a generic looking user agent to avoid immediate blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        logger.info("Reddit JSON client initialized (Scraping mode)")
    
    @classmethod
    def from_env(cls) -> 'RedditClient':
        """Create RedditClient (env vars not needed for scraping)."""
        return cls()
    
    def get_new_posts(
        self,
        subreddit_name: str,
        limit: int = 25,
        min_age_minutes: int = 5,
        max_age_hours: int = 24
    ) -> List[RedditPost]:
        """Fetch new posts from a subreddit using JSON feed.
        
        Args:
            subreddit_name: Name of subreddit (without r/)
            limit: Maximum number of posts to fetch (approximate)
            min_age_minutes: Minimum post age in minutes
            max_age_hours: Maximum post age in hours
            
        Returns:
            List of RedditPost objects
        """
        url = f"{self.BASE_URL}/r/{subreddit_name}/new.json"
        params = {'limit': limit}
        
        posts = []
        now = datetime.utcnow()
        min_time = now - timedelta(minutes=min_age_minutes)
        max_time = now - timedelta(hours=max_age_hours)
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 429:
                logger.warning(f"Rate limited by Reddit. Waiting 5 seconds...")
                time.sleep(5)
                return []
                
            if response.status_code != 200:
                logger.error(f"Error fetching r/{subreddit_name}: {response.status_code}")
                return []
                
            data = response.json()
            children = data.get('data', {}).get('children', [])
            
            for child in children:
                post_data = child.get('data', {})
                
                # Create post object
                post = RedditPost(
                    id=post_data.get('id'),
                    title=post_data.get('title'),
                    selftext=post_data.get('selftext', ''),
                    author=post_data.get('author', '[deleted]'),
                    permalink=post_data.get('permalink'),
                    created_utc=post_data.get('created_utc'),
                    subreddit=Subreddit(subreddit_name)
                )
                
                # Filter by age
                post_time = datetime.utcfromtimestamp(post.created_utc)
                
                if post_time > min_time:
                    continue  # Too new
                if post_time < max_time:
                    continue  # Too old
                
                # Skip deleted/removed
                if post.author in ['[deleted]', '[removed]']:
                    continue
                    
                posts.append(post)
                
            logger.info(f"Fetched {len(posts)} posts from r/{subreddit_name}")
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching posts from r/{subreddit_name}: {e}")
            return []

    def is_likely_seeking_recommendation(self, post: RedditPost) -> bool:
        """Quick heuristic check if post might be seeking recommendations."""
        content = (post.title + "\n" + post.selftext).lower()
        
        question_words = [
            'what', 'which', 'recommend', 'suggestion', 'advice',
            'help', 'looking for', 'should i', 'best', 'good',
            'beginner', 'first', 'buy', 'purchase', 'need'
        ]
        
        return any(word in content for word in question_words)
    
    def fetch_post_comments(self, post: RedditPost, max_comments: int = 10) -> None:
        """Fetch top comments for a post and add them to the post object.
        
        Args:
            post: RedditPost object to fetch comments for
            max_comments: Maximum number of top-level comments to fetch
        """
        url = f"{self.BASE_URL}{post.permalink}.json"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"Failed to fetch comments: {response.status_code}")
                post.comments = []
                return
            
            data = response.json()
            
            # Reddit returns [post_data, comments_data]
            if len(data) < 2:
                post.comments = []
                return
            
            comments_data = data[1].get('data', {}).get('children', [])
            comments = []
            
            for comment_child in comments_data[:max_comments]:
                comment_data = comment_child.get('data', {})
                
                # Skip "more comments" placeholders
                if comment_child.get('kind') != 't1':
                    continue
                
                comments.append({
                    'author': comment_data.get('author', '[deleted]'),
                    'body': comment_data.get('body', ''),
                    'score': comment_data.get('score', 0)
                })
            
            post.comments = comments
            logger.debug(f"Fetched {len(comments)} comments for post {post.id}")
            
        except Exception as e:
            logger.error(f"Error fetching comments for post {post.id}: {e}")
            post.comments = []

if __name__ == "__main__":
    # Test mode
    logging.basicConfig(level=logging.INFO)
    client = RedditClient()
    posts = client.get_new_posts('telescopes', limit=5)
    
    print(f"\nFetched {len(posts)} posts:")
    for post in posts:
        print(f"- {post.title} (r/{post.subreddit.display_name})")
