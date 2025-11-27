from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os
from datetime import datetime

# Add parent directory to path to import bot modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.database import BotDatabase

app = Flask(__name__)
db = BotDatabase()

@app.route('/')
def index():
    """Render the dashboard."""
    status = request.args.get('status', 'new')
    opportunities = db.get_opportunities(status=status)
    stats = db.get_stats()
    return render_template('index.html', opportunities=opportunities, stats=stats, current_status=status)

@app.route('/api/opportunity/<post_id>/status', methods=['POST'])
def update_status(post_id):
    """Update opportunity status."""
    data = request.json
    status = data.get('status')
    if status in ['new', 'replied', 'skipped']:
        db.update_opportunity_status(post_id, status)
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid status'}), 400

@app.template_filter('timeago')
def timeago(value):
    """Format datetime as time ago."""
    if not value:
        return ""
    
    # Handle string timestamp from SQLite
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return value
            
    now = datetime.now()
    diff = now - value
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600}h ago"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60}m ago"
    else:
        return "just now"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
