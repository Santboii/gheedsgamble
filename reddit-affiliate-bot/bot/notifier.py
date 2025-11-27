"""
Notification System

Sends notifications about relevant Reddit posts via email, webhook, or console output.
"""

import os
import json
from typing import Dict, List
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests


class Notifier:
    """Sends notifications about opportunities via various channels."""
    
    def __init__(self):
        """Initialize the notifier with configuration from environment."""
        self.email_enabled = os.getenv('NOTIFICATION_EMAIL_ENABLED', 'false').lower() == 'true'
        self.webhook_enabled = os.getenv('NOTIFICATION_WEBHOOK_ENABLED', 'false').lower() == 'true'
        self.console_enabled = os.getenv('NOTIFICATION_CONSOLE_ENABLED', 'true').lower() == 'true'
        
        # Email configuration
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.notification_email = os.getenv('NOTIFICATION_EMAIL', '')
        
        # Webhook configuration
        self.webhook_url = os.getenv('WEBHOOK_URL', '')
    
    def send_opportunity(self, opportunity: Dict):
        """
        Send a notification about a single opportunity.
        
        Args:
            opportunity: Dict containing:
                - post_id: Reddit post ID
                - post_title: Post title
                - post_url: URL to the post
                - subreddit: Subreddit name
                - author: Post author
                - analysis: AI analysis results
                - analysis: AI analysis results
                - recommended_routes: Recommended website routes
                - suggested_response: Draft response
        """
        if self.console_enabled:
            self._send_console(opportunity)
        
        if self.email_enabled and self.notification_email:
            self._send_email(opportunity)
        
        if self.webhook_enabled and self.webhook_url:
            self._send_webhook(opportunity)
    
    def send_digest(self, opportunities: List[Dict]):
        """
        Send a digest of multiple opportunities.
        
        Args:
            opportunities: List of opportunity dicts
        """
        if not opportunities:
            if self.console_enabled:
                print("\n📭 No new opportunities found in this run.")
            return
        
        if self.console_enabled:
            self._send_console_digest(opportunities)
        
        if self.email_enabled and self.notification_email:
            self._send_email_digest(opportunities)
        
        if self.webhook_enabled and self.webhook_url:
            self._send_webhook_digest(opportunities)
    
    def _send_console(self, opp: Dict):
        """Print opportunity to console."""
        print("\n" + "="*70)
        print("🎯 NEW OPPORTUNITY FOUND")
        print("="*70)
        print(f"📍 Subreddit: r/{opp['subreddit']}")
        print(f"👤 Author: u/{opp['author']}")
        print(f"📝 Title: {opp['post_title']}")
        print(f"🔗 URL: {opp['post_url']}")
        print(f"\n📊 Analysis:")
        print(f"   Confidence: {opp['analysis'].get('confidence', 0):.2f}")
        print(f"   Experience: {opp['analysis'].get('experience_level', 'unknown')}")
        print(f"   Budget: {opp['analysis'].get('budget_range', 'unknown')}")
        print(f"   Intent: {opp['analysis'].get('intent', 'N/A')}")
        print(f"   Intent: {opp['analysis'].get('intent', 'N/A')}")
        print(f"\n🎁 Recommended Routes ({len(opp.get('recommended_routes', []))}):")
        for i, route in enumerate(opp.get('recommended_routes', []), 1):
            print(f"   {i}. {route}")
        print(f"\n💬 Suggested Response:")
        print("   " + "-"*66)
        print("   " + opp['suggested_response'].replace("\n", "\n   "))
        print("   " + "-"*66)
        print("="*70 + "\n")
    
    def _send_console_digest(self, opportunities: List[Dict]):
        """Print digest to console."""
        print("\n" + "="*70)
        print(f"📊 OPPORTUNITY DIGEST - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"Found {len(opportunities)} opportunities")
        print("="*70)
        
        for i, opp in enumerate(opportunities, 1):
            print(f"\n{i}. r/{opp['subreddit']} - {opp['post_title'][:50]}...")
            print(f"   🔗 {opp['post_url']}")
            print(f"   📊 Confidence: {opp['analysis'].get('confidence', 0):.2f}")
            print(f"   🎁 {len(opp.get('recommended_routes', []))} routes recommended")
        
        print("\n" + "="*70 + "\n")
    
    def _send_email(self, opp: Dict):
        """Send opportunity via email."""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎯 New Reddit Opportunity: r/{opp['subreddit']}"
            msg['From'] = self.smtp_user
            msg['To'] = self.notification_email
            
            # Create HTML email
            html = self._format_opportunity_html(opp)
            msg.attach(MIMEText(html, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            print(f"   ✅ Email notification sent to {self.notification_email}")
        except Exception as e:
            print(f"   ❌ Failed to send email: {e}")
    
    def _send_email_digest(self, opportunities: List[Dict]):
        """Send digest via email."""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Reddit Opportunities Digest - {len(opportunities)} found"
            msg['From'] = self.smtp_user
            msg['To'] = self.notification_email
            
            # Create HTML email
            html = self._format_digest_html(opportunities)
            msg.attach(MIMEText(html, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            print(f"   ✅ Digest email sent to {self.notification_email}")
        except Exception as e:
            print(f"   ❌ Failed to send digest email: {e}")
    
    def _send_webhook(self, opp: Dict):
        """Send opportunity via webhook (Slack, Discord, etc.)."""
        try:
            payload = {
                "text": f"🎯 New Reddit Opportunity",
                "blocks": [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "🎯 New Reddit Opportunity"}
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Subreddit:*\nr/{opp['subreddit']}"},
                            {"type": "mrkdwn", "text": f"*Author:*\nu/{opp['author']}"},
                            {"type": "mrkdwn", "text": f"*Confidence:*\n{opp['analysis'].get('confidence', 0):.0%}"},
                            {"type": "mrkdwn", "text": f"*Routes:*\n{len(opp.get('recommended_routes', []))} recommended"}
                        ]
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": f"*{opp['post_title']}*\n<{opp['post_url']}|View Post>"}
                    }
                ]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            print(f"   ✅ Webhook notification sent")
        except Exception as e:
            print(f"   ❌ Failed to send webhook: {e}")
    
    def _send_webhook_digest(self, opportunities: List[Dict]):
        """Send digest via webhook."""
        try:
            text = f"📊 Found {len(opportunities)} Reddit opportunities:\n\n"
            for opp in opportunities[:5]:  # Limit to 5 for brevity
                text += f"• r/{opp['subreddit']}: {opp['post_title'][:50]}...\n"
                text += f"  {opp['post_url']}\n\n"
            
            payload = {"text": text}
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            print(f"   ✅ Digest webhook sent")
        except Exception as e:
            print(f"   ❌ Failed to send digest webhook: {e}")
    
    def _format_opportunity_html(self, opp: Dict) -> str:
        """Format opportunity as HTML email."""
        routes_html = ""
        for route in opp.get('recommended_routes', []):
            routes_html += f"<li><a href='{route}'>{route}</a></li>"
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #FF4500;">🎯 New Reddit Opportunity</h2>
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Subreddit:</strong> r/{opp['subreddit']}</p>
                <p><strong>Author:</strong> u/{opp['author']}</p>
                <p><strong>Title:</strong> {opp['post_title']}</p>
                <p><strong>URL:</strong> <a href="{opp['post_url']}">{opp['post_url']}</a></p>
            </div>
            <h3>📊 Analysis</h3>
            <ul>
                <li><strong>Confidence:</strong> {opp['analysis'].get('confidence', 0):.0%}</li>
                <li><strong>Experience Level:</strong> {opp['analysis'].get('experience_level', 'unknown')}</li>
                <li><strong>Budget:</strong> {opp['analysis'].get('budget_range', 'unknown')}</li>
                <li><strong>Intent:</strong> {opp['analysis'].get('intent', 'N/A')}</li>
            </ul>
            <h3>🎁 Recommended Routes</h3>
            <ul>{routes_html}</ul>
            <h3>💬 Suggested Response</h3>
            <div style="background: #f9f9f9; padding: 15px; border-left: 4px solid #FF4500; margin: 20px 0;">
                <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">{opp['suggested_response']}</pre>
            </div>
        </body>
        </html>
        """
    
    def _format_digest_html(self, opportunities: List[Dict]) -> str:
        """Format digest as HTML email."""
        items_html = ""
        for i, opp in enumerate(opportunities, 1):
            items_html += f"""
            <div style="background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h3 style="margin-top: 0;">{i}. {opp['post_title']}</h3>
                <p><strong>Subreddit:</strong> r/{opp['subreddit']} | 
                   <strong>Confidence:</strong> {opp['analysis'].get('confidence', 0):.0%} | 
                   <strong>Routes:</strong> {len(opp.get('recommended_routes', []))}</p>
                <p><a href="{opp['post_url']}" style="color: #FF4500;">View Post →</a></p>
            </div>
            """
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #FF4500;">📊 Reddit Opportunities Digest</h2>
            <p>Found <strong>{len(opportunities)}</strong> opportunities on {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            {items_html}
        </body>
        </html>
        """
