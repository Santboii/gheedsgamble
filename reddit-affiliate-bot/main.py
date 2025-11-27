"""
Reddit Opportunity Finder

Monitors subreddits for relevant posts and sends notifications about opportunities
for manual response. Does NOT auto-post to avoid Reddit ToS violations.
"""

import os
import time
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

from bot.reddit_client import RedditClient
from bot.llm_analyzer import LLMAnalyzer
from bot.website_response_generator import WebsiteResponseGenerator
from bot.database import BotDatabase
from bot.notifier import Notifier


class OpportunityFinder:
    """Finds and notifies about Reddit opportunities for manual response."""
    
    def __init__(self):
        """Initialize the opportunity finder with all components."""
        load_dotenv()
        
        # Initialize components
        self.reddit = RedditClient.from_env()
        self.analyzer = LLMAnalyzer()
        self.generator = WebsiteResponseGenerator()
        self.db = BotDatabase()
        self.notifier = Notifier()
        
        # Configuration
        self.affiliate_tag = os.getenv('AMAZON_AFFILIATE_TAG', 'stargazer019-20')
        self.check_interval = int(os.getenv('CHECK_INTERVAL_MINUTES', '15'))
        self.max_posts_per_run = int(os.getenv('MAX_POSTS_PER_RUN', '10'))
        self.confidence_threshold = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))
        self.send_digest = os.getenv('SEND_DIGEST', 'true').lower() == 'true'
        
        print("🔍 Reddit Opportunity Finder initialized")
        print(f"   Check interval: {self.check_interval} minutes")
        print(f"   Confidence threshold: {self.confidence_threshold}")
        print(f"   Digest mode: {self.send_digest}")
    
    def get_monitored_subreddits(self) -> List[str]:
        """Get list of subreddits to monitor."""
        # Hardcoded list of relevant subreddits
        return ['telescopes', 'astronomy', 'astrophotography', 'Astronomer']
    
    def analyze_post(self, post: Dict) -> Dict:
        """
        Analyze a single post and create an opportunity if relevant.
        
        Args:
            post: Reddit Submission object
            
        Returns:
            Opportunity dict if relevant, None otherwise
        """
        post_id = post.id
        subreddit = post.subreddit.display_name
        
        # Check if already processed
        if self.db.is_post_processed(post_id):
            return None
        
        # Fetch comments for additional context
        self.reddit.fetch_post_comments(post, max_comments=5)
        
        # Analyze post (including comments)
        comments_text = post.get_top_comments(max_comments=5)
        analysis = self.analyzer.analyze_post(
            post.title,
            post.selftext,
            subreddit,
            comments=comments_text
        )
        
        if not self.analyzer.should_respond(analysis, self.confidence_threshold):
            self.db.mark_post_processed(
                post_id,
                subreddit,
                post.title,
                str(post.author),
                responded=False
            )
            return None
        
        # Generate suggested response with website links
        suggested_response = self.generator.generate_response(
            post.title,
            post.selftext,
            analysis
        )
        
        # Get recommended routes for database storage
        recommended_routes = self.generator.get_recommended_routes(analysis)
        
        if not suggested_response:
            self.db.mark_post_processed(
                post_id,
                subreddit,
                post.title,
                str(post.author),
                responded=False
            )
            return None
        
        # Mark as processed (but not responded to - you'll do that manually)
        self.db.mark_post_processed(
            post_id,
            subreddit,
            post.title,
            str(post.author),
            responded=False
        )
        
        # Create opportunity
        opportunity = {
            'post_id': post_id,
            'post_title': post.title,
            'post_url': f"https://reddit.com{post.permalink}",
            'post_body': post.selftext,
            'subreddit': subreddit,
            'author': str(post.author),
            'created_utc': post.created_utc,
            'analysis': analysis,
            'recommended_routes': recommended_routes,
            'suggested_response': suggested_response
        }
        
        # Save to database for dashboard
        self.db.add_opportunity(opportunity)
        
        return opportunity
    
    def run_once(self):
        """Run one iteration of the opportunity finder."""
        print(f"\n{'='*70}")
        print(f"🔄 Starting opportunity scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        subreddits = self.get_monitored_subreddits()
        print(f"📡 Monitoring subreddits: {', '.join(subreddits)}")
        
        all_opportunities = []
        
        for subreddit in subreddits:
            print(f"\n🔍 Checking r/{subreddit}...")
            
            posts = self.reddit.get_new_posts(
                subreddit,
                limit=self.max_posts_per_run
            )
            
            print(f"   Found {len(posts)} recent posts")
            
            for post in posts:
                opportunity = self.analyze_post(post)
                if opportunity:
                    all_opportunities.append(opportunity)
                    
                    # Send individual notification if not in digest mode
                    if not self.send_digest:
                        self.notifier.send_opportunity(opportunity)
                
                # Small delay to avoid rate limits
                time.sleep(1)
        
        # Send digest if enabled
        if self.send_digest and all_opportunities:
            self.notifier.send_digest(all_opportunities)
        
        print(f"\n{'='*70}")
        print(f"✅ Scan complete!")
        print(f"   Opportunities found: {len(all_opportunities)}")
        print(f"{'='*70}\n")
        
        return all_opportunities
    
    def run_continuous(self):
        """Run the opportunity finder continuously with configured interval."""
        print(f"🚀 Starting continuous mode (checking every {self.check_interval} minutes)")
        print("   Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.run_once()
                
                print(f"😴 Sleeping for {self.check_interval} minutes...")
                time.sleep(self.check_interval * 60)
                
        except KeyboardInterrupt:
            print("\n\n👋 Opportunity finder stopped by user")
        except Exception as e:
            print(f"\n\n❌ Opportunity finder crashed: {e}")
            raise


def main():
    """Main entry point."""
    finder = OpportunityFinder()
    
    # Check if running as one-shot or continuous
    mode = os.getenv('BOT_MODE', 'continuous').lower()
    
    if mode == 'once':
        finder.run_once()
    else:
        finder.run_continuous()


if __name__ == '__main__':
    main()
