# Syllabo - Complete Usage Guide

## Overview
Syllabo is an AI-powered study guide generator that finds relevant YouTube videos and creates personalized study materials. **No API keys required** - it works through web scraping and AI.

## Key Features

### Real Data Without APIs
- Scrapes YouTube search results in real-time
- Extracts video metadata (title, channel, duration, views)
- Gets video transcripts when available
- No YouTube API key needed

### AI-Generated Study Materials
- **Study Notes**: Concise, focused notes from video content
- **Practice Questions**: Review questions to test understanding
- **Key Concepts**: Important terms and principles
- **Study Tips**: Personalized learning recommendations

### Smart Topic Extraction
- Automatically extracts topics from syllabus text
- Handles various formats (weeks, chapters, modules)
- Works with unstructured text input

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Main Application
```bash
python syllabo_final.py
```

### 3. Test Individual Components
```bash
# Test YouTube scraping
python test_youtube_scraping.py

# Test study materials generation
python demo_study_materials.py
```

## How to Use

### Input Your Syllabus
When you run the app, you can:
1. **Paste text directly**: Copy your syllabus content
2. **Type 'demo'**: Use sample content to test
3. **Type 'END'**: When finished entering content

### Example Input Formats

**Structured Syllabus:**
```
Week 1: Introduction to Machine Learning
- Supervised Learning
- Unsupervised Learning

Week 2: Neural Networks
- Perceptrons
- Deep Learning
```

**Simple Topic List:**
```
Machine Learning Fundamentals
K-means Clustering
Neural Networks
Data Preprocessing
```

**Unstructured Text:**
```
This course covers machine learning, including clustering algorithms like k-means, neural networks, and data preprocessing techniques.
```

## What You Get

### For Each Topic:
1. **3 Educational Videos**
   - Real YouTube videos found through scraping
   - Video titles, channels, durations
   - View counts and direct links

2. **AI Study Materials**
   - 5-8 study notes covering key points
   - 6-10 practice questions for review
   - 4-6 key concepts to remember
   - Study tips and recommendations

3. **Complete Study Guide**
   - Saved as JSON file with timestamp
   - All videos and materials organized by topic
   - Ready for review and studying

## Example Output

```
Processing: Machine Learning Fundamentals
--------------------------------------------------
Searching YouTube for educational videos...
Found 3 videos

Videos found:
1. Machine Learning Explained - Complete Tutorial
   Channel: TechEd
   Duration: 45:30
   Views: 1,234,567

Generating AI study materials...
Video transcript found - generating detailed materials

STUDY MATERIALS FOR: Machine Learning Fundamentals
==================================================

STUDY NOTES:
1. Machine learning is a subset of AI that enables computers to learn from data
2. Supervised learning uses labeled data to train predictive models
3. Unsupervised learning finds patterns in data without labels
4. Common algorithms include linear regression, decision trees, and clustering

PRACTICE QUESTIONS:
1. What is the difference between supervised and unsupervised learning?
2. How does machine learning relate to artificial intelligence?
3. What are some common applications of machine learning?
4. When would you use clustering algorithms?

KEY CONCEPTS:
• Supervised Learning
• Unsupervised Learning
• Training Data
• Model Prediction
```

## Files Created

### Main Applications
- `syllabo_final.py` - Complete working application
- `test_youtube_scraping.py` - Test YouTube scraping
- `demo_study_materials.py` - Test AI study materials

### Core Components
- `src/youtube_client.py` - YouTube scraping (no API)
- `src/notes_generator.py` - AI study materials generator
- `src/ai_client.py` - AI client with caching

## Technical Details

### YouTube Scraping
- Parses YouTube search results HTML
- Extracts video metadata from page source
- Gets additional details from video pages
- Handles rate limiting and errors gracefully

### AI Study Materials
- Uses AI to analyze video content and transcripts
- Generates human-like, professional study materials
- Creates different types of learning content
- Follows educational best practices

### No API Keys Required
- Works immediately without setup
- Uses web scraping for YouTube data
- Falls back to free AI services
- Handles errors and missing data

## Troubleshooting

### Common Issues

**No videos found:**
- Check internet connection
- Try broader topic names
- Ensure topics are educational subjects

**AI generation fails:**
- Check internet connection
- Try simpler topic names
- The app will continue with available data

**Slow performance:**
- Normal for web scraping
- Each topic takes 30-60 seconds
- Progress is shown during processing

### Tips for Best Results

1. **Use clear topic names**: "Machine Learning" vs "ML stuff"
2. **Educational subjects work best**: Academic topics get better results
3. **Be patient**: Web scraping takes time but gets real data
4. **Check the JSON output**: Complete results saved for later use

## Advanced Usage

### Customize Video Search
Edit `src/youtube_client.py` to modify:
- Number of videos per topic
- Search query enhancement
- Video filtering criteria

### Customize Study Materials
Edit `src/notes_generator.py` to modify:
- Number of notes/questions generated
- AI prompts for different content types
- Study material formatting

### Add New Features
The modular design makes it easy to add:
- Different export formats
- Additional AI analysis
- Video quality scoring
- User feedback systems

## Benefits

### For Students
- **Saves time**: Finds relevant videos automatically
- **Improves learning**: AI-generated study materials
- **No setup**: Works immediately without API keys
- **Comprehensive**: Complete study guide for any topic

### For Educators
- **Course preparation**: Quick video curation
- **Study guides**: Automated material generation
- **No cost**: Free to use without API fees
- **Customizable**: Easy to modify for specific needs

## Support

If you encounter issues:
1. Check your internet connection
2. Try simpler topic names
3. Look at the example outputs
4. Check the generated JSON files

The app is designed to work reliably without external dependencies or API keys, making it accessible to everyone.