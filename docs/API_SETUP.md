# API Setup Guide

The system works fully without any API keys. This guide is for users who want enhanced AI analysis.

## No API Keys Required

The system provides full functionality without any external APIs:
- **Text Analysis**: Intelligent topic extraction using keyword matching and pattern recognition
- **Content Discovery**: Real YouTube video search via web scraping
- **Reading Materials**: Curated educational content from real sources
- **Relevance Scoring**: Algorithmic content analysis based on keyword overlap
- **Spaced Repetition**: Complete learning system with no external dependencies

## Optional API Enhancement

### 1. Gemini API (Optional Enhancement)
For enhanced AI-powered analysis:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 2. YouTube API (Optional Enhancement)
For additional YouTube metadata:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API key)
5. Add it to your `.env` file:
   ```
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

## System Behavior

**Without API keys** (Default - Full Functionality):
- Intelligent text-based topic extraction
- Real YouTube video search and analysis
- Algorithmic relevance scoring
- Curated educational content recommendations
- Complete spaced repetition system

**With API keys** (Enhanced):
- AI-powered topic extraction and analysis
- Enhanced content relevance scoring
- Additional YouTube metadata

## Testing Your Setup

Run the application and check the logs:
- Without APIs: "No API keys configured - will use intelligent fallback responses"
- With Gemini API: "Using Gemini API"

The system provides complete functionality in both modes.