# Reddit Affiliate Bot - Setup & Deployment Guide

## 📋 Quick Setup

### 1. Install Dependencies

```bash
cd reddit-affiliate-bot
pip install -r requirements.txt
```

### 2. Get API Credentials

#### Reddit API
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - **Name**: Your bot name (e.g., "TelescopeHelper")
   - **App type**: Select "script"
   - **Description**: Brief description
   - **About URL**: Leave blank
   - **Redirect URI**: http://localhost:8080
4. Click "Create app"
5. Note your **client ID** (under the app name) and **client secret**

#### OpenAI API
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and save the key (you won't see it again!)

#### Amazon Affiliate
1. Sign up at https://affiliate-program.amazon.com/
2. Get your affiliate tag from your account dashboard

### 3. Configure Environment

Copy the template and fill in your credentials:

```bash
cp env.template .env
```

Edit `.env` with your actual credentials:

```env
REDDIT_CLIENT_ID=your_actual_client_id
REDDIT_CLIENT_SECRET=your_actual_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=AffiliateBot/1.0 by u/your_username

OPENAI_API_KEY=sk-your-actual-key

AMAZON_AFFILIATE_TAG=your-tag-20

# Start with dry run mode for testing
DRY_RUN=true
```

### 4. Test in Dry Run Mode

Run the bot once without posting to Reddit:

```bash
BOT_MODE=once DRY_RUN=true python main.py
```

This will:
- ✅ Fetch recent posts from configured subreddits
- ✅ Analyze them with AI
- ✅ Find matching products
- ✅ Generate responses
- ✅ Show what it would post (without actually posting)

### 5. Run Locally

Once you're satisfied with the dry run results:

```bash
# Run once
BOT_MODE=once DRY_RUN=false python main.py

# Run continuously (checks every 15 minutes)
python main.py
```

---

## 🚀 Deploy to Google Cloud Run

### Prerequisites

1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Create a Google Cloud project
3. Enable Cloud Run API

### Deployment Steps

```bash
# 1. Authenticate with Google Cloud
gcloud auth login

# 2. Set your project
gcloud config set project YOUR_PROJECT_ID

# 3. Build and deploy
gcloud run deploy reddit-affiliate-bot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars REDDIT_CLIENT_ID=your_id \
  --set-env-vars REDDIT_CLIENT_SECRET=your_secret \
  --set-env-vars REDDIT_USERNAME=your_username \
  --set-env-vars REDDIT_PASSWORD=your_password \
  --set-env-vars REDDIT_USER_AGENT="AffiliateBot/1.0" \
  --set-env-vars OPENAI_API_KEY=your_key \
  --set-env-vars AMAZON_AFFILIATE_TAG=your_tag \
  --set-env-vars BOT_MODE=continuous \
  --set-env-vars DRY_RUN=false
```

**Important**: The bot will run continuously in Cloud Run. You'll be charged for the time it's running.

### Alternative: Use Cloud Scheduler + Cloud Run Jobs

For cost optimization, run the bot periodically instead of continuously:

```bash
# Deploy as a job instead of service
gcloud run jobs create reddit-affiliate-bot \
  --source . \
  --region us-central1 \
  --set-env-vars BOT_MODE=once \
  --set-env-vars [other env vars...]

# Schedule it to run every 15 minutes
gcloud scheduler jobs create http reddit-bot-trigger \
  --location us-central1 \
  --schedule="*/15 * * * *" \
  --uri="https://YOUR_CLOUD_RUN_JOB_URL"
```

---

## 🎯 Adding New Niches

1. Create a new product catalog in `products/your-niche.json`:

```json
{
  "niche": "your-niche",
  "subreddits": ["subreddit1", "subreddit2"],
  "products": [
    {
      "id": "product-1",
      "name": "Product Name",
      "category": "beginner",
      "price_range": "$50-$100",
      "amazon_asin": "B0XXXXXXXXX",
      "description": "Brief product description",
      "use_cases": ["keyword1", "keyword2", "keyword3"],
      "image_url": "https://..."
    }
  ]
}
```

2. The bot will automatically load and monitor the new subreddits!

---

## ⚙️ Configuration

Edit `config/config.yaml` to customize bot behavior:

```yaml
bot:
  check_interval_minutes: 15    # How often to check
  max_posts_per_run: 10         # Posts per subreddit
  confidence_threshold: 0.7     # AI confidence minimum

safety:
  max_responses_per_hour: 4     # Rate limiting
  min_time_between_responses: 10
```

---

## 🔍 Monitoring

### Check Bot Logs

```bash
# Local
tail -f bot.log

# Cloud Run
gcloud run logs read reddit-affiliate-bot --region us-central1
```

### Database

The bot uses SQLite to track processed posts. Check it with:

```bash
sqlite3 bot.db "SELECT * FROM processed_posts ORDER BY processed_at DESC LIMIT 10;"
```

---

## ⚠️ Important Notes

### Reddit Rules
- Always disclose affiliate relationships
- Provide genuine value, not spam
- Follow subreddit rules
- Monitor your bot regularly

### Rate Limits
- Reddit: ~60 requests per minute
- OpenAI: Depends on your tier
- The bot includes delays to stay within limits

### Costs
- **OpenAI**: ~$0.001 per post analysis + response
- **Google Cloud Run**: ~$0.00002 per second (if running continuously)
- **Reddit API**: Free
- **Amazon Affiliate**: Free (you earn commissions!)

### Testing
Always test in dry run mode first:
```bash
DRY_RUN=true python main.py
```

---

## 🐛 Troubleshooting

### "Invalid credentials" error
- Double-check your Reddit API credentials
- Make sure you're using a "script" type app, not "web app"

### "Rate limit exceeded"
- Increase `CHECK_INTERVAL_MINUTES` in config
- Reduce `MAX_POSTS_PER_RUN`

### Bot not responding to posts
- Check `CONFIDENCE_THRESHOLD` (try lowering to 0.5)
- Verify your product catalogs have relevant keywords
- Check logs for AI analysis results

### No products found
- Ensure your subreddit is listed in a product catalog
- Add more relevant keywords to product `use_cases`

---

## 📊 Expected Performance

With default settings:
- **Posts analyzed**: ~40 per hour (10 posts × 4 subreddits × 1 check)
- **Responses posted**: ~2-4 per hour (depends on relevance)
- **Cost**: ~$0.10-$0.20 per day (OpenAI + Cloud Run)

---

## 🎓 Next Steps

1. ✅ Test in dry run mode
2. ✅ Run locally for a few hours
3. ✅ Monitor results and adjust confidence threshold
4. ✅ Add more product catalogs for other niches
5. ✅ Deploy to Cloud Run for 24/7 operation
6. ✅ Monitor affiliate earnings!

---

## 📝 License

MIT - Use responsibly and ethically!
