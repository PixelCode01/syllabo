# Syllabo

A comprehensive educational resource finder that helps students discover the best learning materials for their course syllabus. Features real-time YouTube video scraping and educational course discovery from major platforms like Coursera, Udemy, and freeCodeCamp.

## Key Features

### Real-Time Content Discovery
- **YouTube Video & Playlist Scraping**: Find relevant educational videos and playlists without API keys
- **Comprehensive Resource Discovery**: Automatically detects both individual videos and structured playlists
- **Course Platform Integration**: Discover courses from Coursera, Udemy, and freeCodeCamp
- **Syllabus Processing**: Extract topics from complete course syllabi
- **Multi-Format Input**: Support for text input, file loading, and sample syllabi
- **Interactive Interface**: User-friendly command-line interface

### Spaced Repetition Learning System
- **Intelligent Review Scheduling**: Uses the scientifically-proven Leitner algorithm to optimize retention
- **Automatic Topic Integration**: Add syllabus topics directly to your review schedule
- **Progress Tracking**: Monitor mastery levels and success rates across all topics
- **Desktop Notifications**: Get reminded when topics are due for review
- **Standalone CLI Tool**: Use `forgetmenot.py` for quick spaced repetition access

### Educational Resource Analysis
- **Intelligent Resource Scoring**: Multi-criteria analysis for both videos and playlists including relevance, quality, and engagement
- **Smart Learning Path Creation**: Automatically selects between individual videos and comprehensive playlists as primary resources
- **Playlist Analysis**: Evaluates playlist quality based on video count, total views, and educational value
- **Resource Categorization**: Free vs paid course filtering and recommendations
- **Coverage Analysis**: Shows which syllabus topics are well-covered by available resources

### Professional Output
- **Clean Interface**: Professional, emoji-free output following coding standards
- **Comprehensive Results**: Detailed analysis with direct links to courses and videos
- **Resource Recommendations**: Books, courses, documentation, and community resources
- **Export Options**: Multiple output formats for different use cases

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

**Main Application (Recommended):**
```bash
# Full-featured CLI with spaced repetition
python syllabo_enhanced.py analyze --file syllabus.pdf --search-videos --add-to-review --print-results
```

**Quick Spaced Repetition:**
```bash
# Standalone spaced repetition tool
forgetmenot add "Neural Networks" -d "Forward and backward pass"
forgetmenot list --urgent
forgetmenot review "Neural Networks" --success
```

**Interactive Interface:**
```bash
# User-friendly interactive interface
python interactive_scraper.py
```

See [USAGE.md](USAGE.md) for detailed usage instructions.

## Interactive Scraper Usage

The main feature is the interactive syllabus processor that finds real educational resources:

### Input Methods
1. **Enter syllabus text directly** - Type or paste your syllabus content
2. **Load syllabus from file** - Import from text or PDF files
3. **Use sample syllabus** - Try with built-in example
4. **Quick demo** - Test with a single topic
5. **Exit** - Clean exit option

### Resource Discovery
- **YouTube Videos**: Real-time scraping of educational videos
- **Coursera Courses**: Live course search with direct links
- **Udemy Courses**: Current course listings with pricing
- **freeCodeCamp**: Direct links to certification programs
- **Additional Resources**: Documentation, tutorials, and community resources

### Resource Filtering
- **Free resources only** - Focus on no-cost learning materials
- **Paid resources only** - Premium courses and content
- **Both free and paid** - Complete resource overview

## No API Keys Required

The application works completely without API keys by using web scraping to fetch real data from:
- **YouTube**: Video search and metadata extraction
- **Coursera**: Course listings and information
- **Udemy**: Course search and pricing data
- **freeCodeCamp**: Curriculum and certification links

### Optional Environment Variables (.env)
```bash
# Optional - for enhanced AI features in other components
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
├── syllabo_enhanced.py      # Main CLI application (RECOMMENDED)
├── forgetmenot.py          # Standalone spaced repetition CLI
├── interactive_scraper.py  # Interactive syllabus processor
├── src/                    # Core modules (don't run directly)
│   ├── ai_client.py        # AI integration
│   ├── database.py         # Database management
│   ├── export_system.py    # Export functionality
│   ├── spaced_repetition.py # Spaced repetition engine
│   ├── notification_system.py # Desktop notifications
│   └── ... (other core modules)
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
├── USAGE.md               # Usage instructions
└── SPACED_REPETITION_GUIDE.md # Spaced repetition guide
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

## Spaced Repetition System

Syllabo includes a powerful spaced repetition system that helps you retain what you've learned using scientifically-proven memory techniques.

### How It Works
The system uses the **Leitner algorithm** with these review intervals:
- **Day 1**: New topics (1 day interval)
- **Day 3**: First review (3 day interval)
- **Day 5**: Second review (5 day interval)
- **Day 11, 25, 44, 88**: Progressive intervals based on success

### Integration with Syllabo
```bash
# Analyze syllabus and add topics to review schedule
python syllabo_enhanced.py analyze --file syllabus.pdf --add-to-review

# Check what's due for review
python syllabo_enhanced.py review due --notify

# Mark a topic as successfully reviewed
python syllabo_enhanced.py review mark --topic "Neural Networks" --success
```

### Standalone Forget-Me-Not Tool
```bash
# Quick spaced repetition commands
forgetmenot add "Machine Learning" -d "Supervised and unsupervised learning"
forgetmenot list --urgent
forgetmenot review "Machine Learning" --success
forgetmenot stats
```

### Features
- **Automatic Scheduling**: Topics appear for review at optimal intervals
- **Progress Tracking**: Monitor success rates and mastery levels
- **Desktop Notifications**: Get reminded when reviews are due
- **Local Storage**: All data stored locally in JSON format
- **Cross-Platform**: Works on Windows, macOS, and Linux

See [SPACED_REPETITION_GUIDE.md](SPACED_REPETITION_GUIDE.md) for complete documentation.

## Advanced Features

### Playlist Integration
The system now automatically searches for and analyzes YouTube playlists alongside individual videos:

- **Automatic Playlist Detection**: Searches for educational playlists related to each topic
- **Playlist Quality Analysis**: Evaluates playlists based on video count, total views, and educational indicators
- **Smart Resource Selection**: Automatically chooses between individual videos and comprehensive playlists as primary learning resources
- **Mixed Recommendations**: Provides both individual videos and playlists in results when appropriate

Example output with playlist support:
```
Topic: Machine Learning Basics
------------------------------------------------------------

   1. [PLAYLIST] Complete Machine Learning Course 2024
      Channel: freeCodeCamp.org
      URL: https://youtube.com/playlist?list=PLWKjhJtqVAblQe2CCWqV4Zy3LY01Z8aF1
      Videos: 25 | Total Views: 1,250,000
      Relevance: 9.5/10 | Overall: 9.2/10
      Tags: Highly Relevant | Comprehensive Course

   2. [VIDEO] Machine Learning Explained in 10 Minutes
      Channel: Zach Star
      URL: https://youtube.com/watch?v=ukzFI9rgwfU
      Duration: 10:30 | Views: 847,392
      Relevance: 8.8/10 | Overall: 8.5/10
      Tags: Highly Relevant | Quick Review
```

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