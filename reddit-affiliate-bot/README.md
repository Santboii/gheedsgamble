# Reddit Opportunity Finder

An AI-powered tool that monitors Reddit subreddits and **notifies you** about relevant posts where you can provide helpful product recommendations. Designed to help you find opportunities for manual engagement while staying compliant with Reddit's Terms of Service.

## 🎯 What It Does

- 🔍 **Monitors** multiple subreddits for relevant posts
- 🤖 **Analyzes** posts with AI to determine if they're asking for product recommendations
- 🎁 **Matches** user needs with products from your catalog
- ✍️ **Generates** suggested responses for you to review
- 📬 **Notifies** you about opportunities via console, email, or webhook
- ✅ **Tracks** processed posts to avoid duplicates

## ⚠️ Important: No Auto-Posting

This tool **does NOT automatically post to Reddit**. It finds opportunities and notifies you, so you can:
- Review each opportunity manually
- Customize responses with your expertise
- Build authentic community presence
- Stay compliant with Reddit's Terms of Service

## Features

- 🤖 **AI-Powered Analysis**: Uses OpenAI to understand user intent and needs
- 🎯 **Multi-Niche Support**: Easily monitor multiple subreddits across different niches
- 📊 **Smart Product Matching**: Keyword-based scoring algorithm
- 💬 **Response Suggestions**: AI-generated draft responses to save time
- 📬 **Flexible Notifications**: Console output, email, or webhooks (Slack/Discord)
- 📈 **Opportunity Tracking**: SQLite database prevents duplicate alerts

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the template and add your credentials:

```bash
cp env.template .env
```

Edit `.env`:
- Add your **OpenAI API key** (required)
- Add your **Reddit API credentials** (required)
- Configure **notification preferences** (optional)

### 3. Run the Opportunity Finder

```bash
# Run once to test
BOT_MODE=once python3 main.py

# Run continuously (checks every 15 minutes)
python3 main.py
```

### 4. Run the Web Dashboard

```bash
# Run the dashboard (frontend)
python3 web/app.py
```

Visit http://localhost:5000 to view your opportunities.

## Notification Options

### Console Output (Default)
Opportunities are printed to the terminal with full details:
- Post title, URL, and author
- AI analysis results
- Recommended products
- Suggested response

### Email Notifications
Set in `.env`:
```bash
NOTIFICATION_EMAIL_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
NOTIFICATION_EMAIL=your_email@gmail.com
```

### Webhook Notifications (Slack/Discord)
Set in `.env`:
```bash
NOTIFICATION_WEBHOOK_ENABLED=true
WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Digest Mode
Get a summary of all opportunities instead of individual notifications:
```bash
SEND_DIGEST=true
```

## Adding New Niches

Create a new product catalog in `products/your-niche.json`:

```json
{
  "niche": "your-niche",
  "subreddits": ["subreddit1", "subreddit2"],
  "products": [
    {
      "id": "product-id",
      "name": "Product Name",
      "category": "beginner|intermediate|advanced",
      "price_range": "$X-$Y",
      "amazon_asin": "AMAZON_ASIN",
      "description": "Product description",
      "use_cases": ["keyword1", "keyword2"]
    }
  ]
}
```

The tool will automatically load all JSON files from the `products/` directory.

## How to Respond Manually

When you receive a notification:

1. **Review the opportunity**: Check the post, analysis, and suggested response
2. **Customize the response**: Add your personal expertise and insights
3. **Visit Reddit**: Go to the post URL
4. **Post your response**: Copy/paste and edit the suggested response
5. **Be genuine**: Make it conversational and helpful

## Best Practices

✅ **Do:**
- Provide genuine value and expertise
- Disclose your affiliation with the website
- Engage in conversations beyond just recommendations
- Build karma and trust in communities first
- Follow each subreddit's specific rules

❌ **Don't:**
- Post the exact same response multiple times
- Respond to every single post
- Ignore community feedback
- Spam or be overly promotional

## Configuration

Edit `config/config.yaml` to customize:
- Check interval and post limits
- Confidence threshold for opportunities
- Response style preferences
- Safety and rate limiting settings

## Deployment

### Local Development
```bash
python main.py
```

### Google Cloud Run (24/7 Monitoring)
```bash
gcloud run deploy reddit-opportunity-finder \
  --source . \
  --set-env-vars [your env vars...]
```

See `SETUP.md` for detailed deployment instructions.

## Cost Estimates

With default settings (checking every 15 minutes):
- **OpenAI API**: ~$0.05-$0.10/day
- **Google Cloud Run**: ~$0.05-$0.10/day (if deployed)
- **Reddit API**: Free
- **Total**: ~$0.10-$0.20/day

## Legal & Ethical Considerations

⚠️ **Important:**
- This tool is designed to help you find opportunities, not spam Reddit
- Always follow Reddit's Terms of Service and community guidelines
- Provide genuine value, not just promotional content
- Disclose affiliate relationships when posting
- Use responsibly and ethically

## License

MIT - Use responsibly!
