# Gemini AI Integration Setup Guide

This guide will help you integrate Google Gemini AI into TerraEngine for enhanced crop recommendations.

## Overview

TerraEngine uses Google's Gemini AI to provide intelligent insights for Mars crop recommendations. The system works in two modes:

1. **AI Mode** (when Gemini is configured): Provides AI-enhanced recommendations with detailed insights
2. **Fallback Mode** (without Gemini): Uses algorithmic scoring for recommendations

## Setup Steps

### 1. Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy your API key (keep it secure!)

### 2. Configure the API Key

You have two options:

#### Option A: Environment Variable (Recommended)

Create or edit `.env` file in the backend directory:

```bash
cd /Users/joker2307/Desktop/TerraEngine/backend
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

Replace `your_api_key_here` with your actual API key.

#### Option B: System Environment Variable

**On macOS/Linux:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**On Windows:**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

### 3. Install Required Package

```bash
cd /Users/joker2307/Desktop/TerraEngine/backend
pip3 install google-generativeai==0.3.2
```

Or install from requirements.txt:
```bash
pip3 install -r requirements.txt
```

### 4. Activate Gemini Integration

Open `backend/api/gemini_integration.py` and uncomment the Gemini initialization code (lines marked with `# TODO`):

```python
# Change this:
# import google.generativeai as genai
# genai.configure(api_key=self.api_key)
# self.model = genai.GenerativeModel('gemini-pro')

# To this:
import google.generativeai as genai
genai.configure(api_key=self.api_key)
self.model = genai.GenerativeModel('gemini-pro')
```

### 5. Restart the Server

```bash
cd /Users/joker2307/Desktop/TerraEngine/backend
python3 manage.py runserver
```

## API Endpoints

### Standard Recommendations (Algorithmic)
```bash
GET /api/crops/match_crop/?crop=tomato&top_n=5
```

Returns top 5 regions based on algorithmic scoring.

### AI-Enhanced Recommendations
```bash
POST /api/crops/recommend_with_ai/
Content-Type: application/json

{
  "crop": "tomato",
  "top_n": 5
}
```

Returns recommendations with Gemini AI insights.

## Testing

Test if Gemini is working:

```bash
# Check if API key is configured
python3 -c "import os; print('Gemini configured!' if os.getenv('GEMINI_API_KEY') else 'No API key found')"

# Test the AI endpoint
curl -X POST http://localhost:8000/api/crops/recommend_with_ai/ \
  -H "Content-Type: application/json" \
  -d '{"crop": "tomato", "top_n": 5}'
```

## Response Format

### Without Gemini (Fallback)
```json
{
  "crop": "Tomato",
  "recommendations": [...],
  "ai_insights": {
    "enabled": false,
    "message": "Gemini AI not configured",
    "recommendation": "Basic algorithmic recommendation text"
  }
}
```

### With Gemini (AI-Enhanced)
```json
{
  "crop": "Tomato",
  "recommendations": [...],
  "ai_insights": {
    "enabled": true,
    "insights": "Detailed AI-generated insights...",
    "analysis": {
      "summary": "Brief summary...",
      "full_text": "Complete analysis..."
    },
    "confidence": "high"
  }
}
```

## Features

When Gemini is enabled, you get:

- ✅ Natural language insights about crop suitability
- ✅ Detailed analysis of each recommended region
- ✅ Specific recommendations for soil preparation
- ✅ Challenges and mitigation strategies
- ✅ Success probability estimates
- ✅ Contextual understanding of Mars agriculture constraints

## Troubleshooting

### Error: "Gemini AI not configured"
- Check that your API key is set correctly
- Verify the environment variable with: `echo $GEMINI_API_KEY`
- Make sure you restart the server after setting the key

### Error: "Could not initialize Gemini AI"
- Ensure `google-generativeai` package is installed
- Check that the import statements are uncommented
- Verify your API key is valid

### Error: API quota exceeded
- Gemini has usage limits on the free tier
- System automatically falls back to algorithmic mode
- Consider upgrading your Google AI quota

## Security Notes

⚠️ **Never commit your API key to Git!**

Add to `.gitignore`:
```
.env
*.env
.env.local
```

## Cost Considerations

- Gemini API has a generous free tier
- Each recommendation request makes 1 API call
- Monitor usage at [Google AI Studio](https://makersuite.google.com/)

## Support

For issues with:
- **TerraEngine**: Check backend logs
- **Gemini API**: Visit [Google AI documentation](https://ai.google.dev/docs)

---

**Status**: Ready to integrate ✨
**Last Updated**: October 5, 2025
