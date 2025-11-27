from bot.database import BotDatabase
import time

db = BotDatabase()

sample_opp = {
    'post_id': 'sample_123',
    'post_title': 'Best beginner telescope for under $300?',
    'post_url': 'https://reddit.com/r/telescopes/comments/sample/best_beginner_telescope',
    'post_body': 'I want to get into astronomy but have a limited budget. Looking for something easy to use.',
    'subreddit': 'telescopes',
    'author': 'StarGazerTest',
    'created_utc': time.time(),
    'analysis': {
        'confidence': 0.95,
        'experience_level': 'beginner',
        'budget_range': 'budget ($100-$300)',
        'key_needs': ['easy to use', 'budget'],
        'intent': 'seeking_recommendation'
    },
    'recommended_routes': [
        'https://www.telescoped.space/telescopes/budget',
        'https://www.telescoped.space/stargazing-guide'
    ],
    'suggested_response': "hey! for a beginner on a budget, check out our budget telescope guide: https://www.telescoped.space/telescopes/budget - we've got some great options under $300. i'd also recommend reading through the stargazing guide: https://www.telescoped.space/stargazing-guide to get started!"
}

db.add_opportunity(sample_opp)
print("✅ Sample opportunity added to database!")
