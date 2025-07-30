# Syllabo Enhanced

An AI-powered Python application that helps students find the most relevant YouTube videos for their course syllabus topics. Works without YouTube API keys using web scraping and includes AI-generated study materials.

## Key Features

### AI-Powered Analysis
- **Smart Topic Extraction**: AI extracts topics and subtopics from syllabus text/PDF
- **Multi-Criteria Video Scoring**: Relevance, quality, engagement, and sentiment analysis
- **Study Materials Generation**: AI creates personalized notes, questions, and key concepts
- **No API Keys Required**: Works without YouTube API using web scraping
- **Intelligent Caching**: Reduces API calls and improves performance
- **Enhanced Error Handling**: Graceful degradation when services are unavailable

### Comprehensive Video Analysis & Study Materials
- **Relevance Scoring**: How well videos match your topics (1-10 scale)
- **Quality Assessment**: Duration, view count, like ratio analysis
- **Engagement Metrics**: Comment analysis and interaction rates
- **Sentiment Analysis**: AI analyzes comments for educational value
- **Study Notes Generation**: AI creates concise study notes from video content
- **Practice Questions**: Generates review questions to test understanding
- **Key Concepts Extraction**: Identifies important terms and concepts
- **Study Tips**: Provides personalized learning recommendations

### Data Persistence
- **SQLite Database**: Stores syllabi, topics, videos, and user feedback
- **Search History**: Track and revisit previous analyses
- **User Feedback System**: Rate videos and improve recommendations

### Multiple Export Formats
- **JSON**: Structured data for further processing
- **CSV**: Spreadsheet-compatible format
- **Markdown**: Human-readable documentation
- **HTML**: Beautiful web reports with styling

### Multiple Interfaces
- **Enhanced CLI**: Advanced command-line interface with rich features
- **Terminal UI**: Interactive textual interface (original)
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## Quick Start

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd syllabo

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Basic Usage
```bash
# Demo without API keys - shows web scraping and study materials
python demo_no_api.py

# Simple CLI with study materials generation
python syllabo_cli.py

# Test the new features
python test_new_cli.py

# Enhanced CLI with full features
python syllabo_enhanced.py analyze --file syllabus.pdf --search-videos --print-results

# Search specific topic and save results
python syllabo_enhanced.py search --topic "Machine Learning" --max-videos 10 --save --export-format html
```

## Enhanced CLI Usage

### Analyze Syllabus
```bash
# Complete analysis with terminal display and HTML export
python syllabo_enhanced.py analyze --file syllabus.pdf --search-videos --print-results --save --export-format html

# From text input with detailed results
python syllabo_enhanced.py analyze --text "Week 1: AI Basics, Week 2: ML..." --search-videos --print-results

# Quick topic extraction only
python syllabo_enhanced.py analyze --file syllabus.txt

# Analyze with custom video limits
python syllabo_enhanced.py analyze --file syllabus.pdf --search-videos --max-videos 8 --print-results
```

### Search Videos for Specific Topics
```bash
# Search for specific topic
python syllabo_enhanced.py search --topic "Machine Learning" --max-videos 10 --save

# Search with custom parameters
python syllabo_enhanced.py search --topic "Data Structures" --max-videos 15
```

### View History and Export
```bash
# View recent syllabi
python syllabo_enhanced.py history --limit 10

# Export results (coming soon)
python syllabo_enhanced.py export --format html
```

## API Requirements

### No API Keys Required for Basic Functionality
The app now works without any API keys by using web scraping to fetch real YouTube data.

### Optional (for Enhanced Features)
- **Gemini API**: For enhanced AI analysis (falls back to Hack Club AI if not provided)
- **YouTube Data API**: For additional metadata (app works without it)

### Environment Variables (.env)
```bash
# Optional - app works without these
GEMINI_API_KEY="your_gemini_api_key_here_optional"
YOUTUBE_API_KEY="your_youtube_api_key_here_optional"
```

## Video Scoring System

Each video receives multiple scores:

### Relevance Score (1-10)
- AI analyzes title, description, and transcript
- Considers topic alignment and content depth
- **Weight: 40%** in composite score

### Quality Score (1-10)
- Duration optimization (10-60 min preferred)
- View count and engagement metrics
- Transcript availability bonus
- **Weight: 20%** in composite score

### Sentiment Score (1-10)
- AI analyzes comment sentiment
- Educational value assessment
- Viewer satisfaction indicators
- **Weight: 25%** in composite score

### Engagement Score (1-10)
- Comment-to-view ratio
- Like-to-view ratio
- Community interaction level
- **Weight: 15%** in composite score

## Project Structure

```
syllabo/
├── src/
│   ├── ai_client.py          # Enhanced AI client with caching
│   ├── app.py               # Original terminal UI
│   ├── database.py          # SQLite database management
│   ├── export_system.py     # Multi-format export system
│   ├── feedback_system.py   # User feedback and ratings
│   ├── logger.py            # Comprehensive logging
│   ├── notes_generator.py   # AI-powered study materials generator
│   ├── syllabus_parser.py   # PDF/text parsing with AI
│   ├── utils.py             # Utility functions
│   ├── video_analyzer.py    # Enhanced video analysis
│   └── youtube_client.py    # Web scraping YouTube client (no API needed)
├── main.py                  # Original entry point
├── syllabo_cli.py           # Simple CLI with study materials
├── syllabo_enhanced.py      # Enhanced CLI interface
├── demo_no_api.py          # Demo without API keys
├── test_new_cli.py         # Test new features
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Study Materials Generation

The app now generates comprehensive study materials for each topic:

### Study Notes
- Concise, focused notes extracted from video content
- Key information organized for easy review
- Professional, human-like writing style

### Practice Questions
- Review questions to test understanding
- Range from basic recall to critical thinking
- Help with memorization and concept application

### Key Concepts
- Important terms and principles highlighted
- Essential vocabulary for each topic
- Core concepts students should remember

### Study Tips
- Personalized learning recommendations
- Best practices for studying each topic
- Guidance on how to use the materials effectively

## Example Output

### Study Materials Example
```
STUDY NOTES:
• Python is a high-level programming language known for its simplicity and readability
• Variables in Python are created by assigning values and don't need explicit declaration
• Python supports multiple data types including strings, integers, floats, and booleans
• Functions in Python are defined using the 'def' keyword followed by the function name

STUDY QUESTIONS:
? What are the main advantages of using Python for programming?
? How do you create and assign values to variables in Python?
? What are the different data types available in Python?
? How do you define and call functions in Python?

KEY CONCEPTS:
- High-level programming language
- Dynamic typing system
- Object-oriented programming
- Interpreted language execution
```

### Enhanced Terminal Display
```
SYLLABUS ANALYSIS SUMMARY
--------------------------------------------------
Syllabus: CS101_syllabus.pdf
Analyzed: 2025-01-30 14:30:25

TOPICS FOUND (3)
------------------------------
1. Machine Learning Basics
   1. Supervised Learning
   2. Unsupervised Learning
   3. Neural Networks

2. Data Structures
   1. Arrays and Lists
   2. Trees and Graphs

TOP VIDEO RECOMMENDATIONS
======================================================================

Topic: Machine Learning Basics
------------------------------------------------------------

   1. Machine Learning Explained | Complete Tutorial for Beginners
      Channel: edureka!
      URL: https://youtube.com/watch?v=ukzFI9rgwfU
      Duration: 45:30 | Views: 2,847,392
      Relevance: 9.2/10 | Overall: 8.7/10
      Transcript: Available
      Tags: Highly Relevant | Well Received | Has Transcript

QUICK LINKS - TOP RECOMMENDATIONS
============================================================

Machine Learning Basics
   Best: Machine Learning Explained | Complete Tutorial...
   Link: https://youtube.com/watch?v=ukzFI9rgwfU
   Score: 9.2/10

TOPIC COVERAGE ANALYSIS
--------------------------------------------------
Overall Coverage: 85.7%
Topics Analysis:
   Well Covered: 2
   Partially Covered: 1
   Not Covered: 0
```

## Advanced Features

### Batch Processing
- Process multiple topics concurrently
- Intelligent rate limiting for API calls
- Progress tracking for long operations

### Caching System
- AI response caching (1-hour TTL)
- Reduces API costs and improves speed
- Automatic cache invalidation

### Error Recovery
- Exponential backoff for API failures
- Graceful degradation when services are down
- Comprehensive error logging

### Database Features
- Persistent storage of all analyses
- Topic-video relationship tracking
- User feedback and rating system
- Search history and favorites

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- YouTube Data API for video search capabilities
- Hack Club AI for free AI analysis
- Google Gemini for enhanced AI features
- Textual library for the terminal UI