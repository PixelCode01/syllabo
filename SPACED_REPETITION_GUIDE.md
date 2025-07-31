# Spaced Repetition Integration Guide

Syllabo now includes an intelligent spaced repetition system to help you retain what you've learned from your study materials. This system uses the scientifically-proven Leitner algorithm to optimize your review schedule.

## Core Concept

The spaced repetition system automatically schedules reviews of topics at increasing intervals based on how well you remember them. Successfully reviewed topics get longer intervals, while failed reviews reset to shorter intervals.

## Review Intervals

The system uses these intervals (in days):
- **Level 0**: 1 day (new topics)
- **Level 1**: 3 days
- **Level 2**: 5 days  
- **Level 3**: 11 days
- **Level 4**: 25 days
- **Level 5**: 44 days
- **Level 6**: 88 days (mastered)

## Integration with Syllabo

### Adding Topics from Syllabus Analysis

When analyzing a syllabus, you can automatically add extracted topics to your review schedule:

```bash
# Analyze syllabus and add topics to spaced repetition
python syllabo_enhanced.py analyze --file syllabus.pdf --add-to-review

# Or with text input
python syllabo_enhanced.py analyze --text "Week 1: Neural Networks..." --add-to-review
```

### Using the Review System

#### View Your Review Schedule
```bash
# List all topics with their status
python syllabo_enhanced.py review list
```

#### Check What's Due
```bash
# Show topics due for review
python syllabo_enhanced.py review due

# With desktop notification
python syllabo_enhanced.py review due --notify
```

#### Mark Reviews
```bash
# Mark successful review (increases interval)
python syllabo_enhanced.py review mark --topic "Neural Networks" --success

# Mark failed review (decreases interval)
python syllabo_enhanced.py review mark --topic "Neural Networks" --failure
```

#### Add Topics Manually
```bash
# Add a topic with description
python syllabo_enhanced.py review add --topic "Backpropagation" --description "Forward and backward pass calculations"
```

#### View Statistics
```bash
# Overall statistics
python syllabo_enhanced.py review stats

# Specific topic statistics
python syllabo_enhanced.py review stats --topic "Neural Networks"
```

#### Remove Topics
```bash
# Remove a topic from review schedule
python syllabo_enhanced.py review remove --topic "Neural Networks"
```

## Standalone Forget-Me-Not CLI

For quick access to spaced repetition features, use the standalone `forgetmenot.py` script:

### Basic Commands

```bash
# Add new study topic
forgetmenot add "Neural Networks" -d "Forward/backward pass"

# Mark review as successful (doubles interval)
forgetmenot review "Neural Networks" --success

# Mark review as failed (halves interval)  
forgetmenot review "Neural Networks" --failure

# List upcoming reviews
forgetmenot list --urgent

# Show all topics
forgetmenot list

# View study statistics
forgetmenot stats

# Send desktop notifications for due topics
forgetmenot remind
```

### Example Workflow

```bash
# Day 0: Add topic
forgetmenot add "Calculus" -d "Derivatives and integrals"
# → Next review: 1 day

# Day 1: Successful review
forgetmenot review "Calculus" --success
# → Next review: 3 days (Day 4)

# Day 4: Successful review
forgetmenot review "Calculus" --success  
# → Next review: 5 days (Day 9)

# Day 9: Failed review
forgetmenot review "Calculus" --failure
# → Next review: 3 days (Day 12)
```

## Mastery Levels

The system tracks your progress with these mastery levels:

- **Learning**: Just started (interval 0-1)
- **Beginner**: Basic familiarity (interval 1-2)
- **Intermediate**: Good understanding (interval 2-3, 60%+ success rate)
- **Advanced**: Strong knowledge (interval 3-5, 70%+ success rate)
- **Mastered**: Expert level (interval 5+, 80%+ success rate)

## Desktop Notifications

The system can send desktop notifications to remind you of due reviews:

### Windows
- Uses Windows 10 toast notifications
- Automatically installs `win10toast` package

### macOS
- Uses built-in `osascript` for notifications
- No additional installation required

### Linux
- Uses `notify-send` command
- Install with: `sudo apt-get install libnotify-bin`

## Data Storage

Review data is stored locally in `spaced_repetition.json`:

```json
{
  "Neural Networks": {
    "topic_name": "Neural Networks",
    "description": "Forward and backward pass calculations",
    "last_review": "2025-07-21T10:30:00",
    "next_review": "2025-07-24T10:30:00",
    "interval_index": 1,
    "review_count": 3,
    "success_streak": 2,
    "total_successes": 2,
    "total_reviews": 3,
    "created_at": "2025-07-20T09:00:00"
  }
}
```

## Best Practices

### Daily Review Routine
1. Check due topics: `forgetmenot list --urgent`
2. Review each topic thoroughly
3. Mark honestly based on your recall
4. Don't skip reviews - consistency is key

### Topic Management
- Use descriptive topic names
- Add helpful descriptions for context
- Break complex topics into smaller subtopics
- Remove topics you no longer need to study

### Success Criteria
- Mark as **success** if you can explain the concept clearly
- Mark as **failure** if you struggle to recall key points
- Be honest - the system adapts to your actual retention

## Integration Examples

### Complete Syllabus Workflow
```bash
# 1. Analyze syllabus and add to review schedule
python syllabo_enhanced.py analyze --file "AI_Course_Syllabus.pdf" --search-videos --add-to-review --print-results

# 2. Daily review routine
forgetmenot list --urgent
forgetmenot review "Neural Networks" --success
forgetmenot review "Backpropagation" --failure

# 3. Track progress
forgetmenot stats
python syllabo_enhanced.py review stats
```

### Automated Reminders
Set up a daily cron job or scheduled task:
```bash
# Linux/macOS cron job (runs at 9 AM daily)
0 9 * * * /path/to/forgetmenot remind

# Windows Task Scheduler
# Create task to run: python forgetmenot.py remind
```

## Troubleshooting

### Common Issues

**Topics not appearing in review list**
- Check if topics were added successfully
- Verify the data file exists: `spaced_repetition.json`

**Notifications not working**
- Windows: Install win10toast: `pip install win10toast`
- Linux: Install notify-send: `sudo apt-get install libnotify-bin`
- macOS: Ensure osascript is available

**Data file corruption**
- Backup your `spaced_repetition.json` file regularly
- The system will recreate the file if corrupted

### Reset System
To start fresh, simply delete `spaced_repetition.json` and restart.

## Scientific Background

This implementation is based on:
- **Leitner System**: Proven spaced repetition algorithm
- **Forgetting Curve**: Ebbinghaus's research on memory decay
- **Cognitive Load Theory**: Optimal spacing for long-term retention

The intervals are designed to present information just before you're likely to forget it, maximizing retention efficiency.