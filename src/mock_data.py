"""Mock data for testing without API keys"""

MOCK_VIDEOS = {
    "python programming": [
        {
            "id": "mock_python_1",
            "title": "Python Programming Tutorial for Beginners - Complete Course",
            "channel": "Programming with Mosh",
            "description": "Learn Python programming from scratch. This comprehensive tutorial covers variables, data types, functions, classes, and more.",
            "duration": "6:14:07",
            "view_count": 2847392,
            "like_count": 89234,
            "published_at": "2023-01-15T10:00:00Z",
            "thumbnail": "https://example.com/thumb1.jpg"
        },
        {
            "id": "mock_python_2", 
            "title": "Python Full Course for Beginners | Complete All-in-One Tutorial",
            "channel": "Bro Code",
            "description": "Python tutorial for beginners. Learn Python basics including syntax, variables, loops, functions, and object-oriented programming.",
            "duration": "12:00:54",
            "view_count": 1234567,
            "like_count": 45678,
            "published_at": "2023-02-20T14:30:00Z",
            "thumbnail": "https://example.com/thumb2.jpg"
        },
        {
            "id": "mock_python_3",
            "title": "Learn Python in 1 Hour - Python Basics for Absolute Beginners",
            "channel": "Programming with Mosh",
            "description": "Quick Python tutorial covering the fundamentals. Perfect for beginners who want to get started quickly.",
            "duration": "1:00:05",
            "view_count": 987654,
            "like_count": 32145,
            "published_at": "2023-03-10T09:15:00Z",
            "thumbnail": "https://example.com/thumb3.jpg"
        }
    ],
    "data structures": [
        {
            "id": "mock_ds_1",
            "title": "Data Structures and Algorithms Course - Complete Tutorial",
            "channel": "freeCodeCamp.org",
            "description": "Complete course on data structures and algorithms. Covers arrays, linked lists, stacks, queues, trees, and graphs.",
            "duration": "8:00:00",
            "view_count": 3456789,
            "like_count": 123456,
            "published_at": "2023-01-05T12:00:00Z",
            "thumbnail": "https://example.com/thumb4.jpg"
        },
        {
            "id": "mock_ds_2",
            "title": "Data Structures Explained - Arrays, Linked Lists, Stacks & Queues",
            "channel": "CS Dojo",
            "description": "Learn the fundamental data structures every programmer should know. Includes practical examples and implementations.",
            "duration": "45:30",
            "view_count": 876543,
            "like_count": 28765,
            "published_at": "2023-02-12T16:45:00Z",
            "thumbnail": "https://example.com/thumb5.jpg"
        }
    ],
    "machine learning": [
        {
            "id": "mock_ml_1",
            "title": "Machine Learning Explained - Complete Beginner's Guide",
            "channel": "3Blue1Brown",
            "description": "Introduction to machine learning concepts including supervised learning, neural networks, and deep learning fundamentals.",
            "duration": "3:22:15",
            "view_count": 4567890,
            "like_count": 187654,
            "published_at": "2023-01-20T11:30:00Z",
            "thumbnail": "https://example.com/thumb6.jpg"
        },
        {
            "id": "mock_ml_2",
            "title": "Machine Learning Course for Beginners - Python & Scikit-learn",
            "channel": "Tech With Tim",
            "description": "Learn machine learning with Python. Covers linear regression, classification, clustering, and model evaluation.",
            "duration": "2:45:30",
            "view_count": 1987654,
            "like_count": 76543,
            "published_at": "2023-03-05T13:20:00Z",
            "thumbnail": "https://example.com/thumb7.jpg"
        }
    ]
}

MOCK_TRANSCRIPTS = {
    "mock_python_1": "Welcome to this comprehensive Python programming tutorial. In this course, we'll cover everything you need to know to get started with Python programming. We'll begin with variables and data types, then move on to control structures like loops and conditionals. Python is a versatile programming language that's perfect for beginners.",
    "mock_ds_1": "Data structures are fundamental concepts in computer science. Today we'll explore arrays, which are collections of elements stored in contiguous memory locations. Arrays provide constant time access to elements using indices. We'll also cover linked lists, which are dynamic data structures.",
    "mock_ml_1": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data. We'll start with supervised learning, where we train models on labeled data to make predictions on new, unseen data."
}

MOCK_COMMENTS = {
    "mock_python_1": [
        "This tutorial is amazing! Finally understood Python basics.",
        "Great explanation of variables and functions. Very helpful!",
        "Perfect for beginners. The examples are clear and easy to follow.",
        "Thanks for this comprehensive tutorial. Learned a lot!",
        "Best Python tutorial I've found. Highly recommend!"
    ],
    "mock_ds_1": [
        "Excellent explanation of data structures. Very clear!",
        "This helped me understand arrays and linked lists finally.",
        "Great course! The visualizations make it easy to understand.",
        "Perfect for computer science students. Thank you!",
        "Clear explanations and good examples. Very helpful!"
    ],
    "mock_ml_1": [
        "Amazing introduction to machine learning concepts!",
        "This made ML much less intimidating. Great work!",
        "Perfect starting point for machine learning journey.",
        "Clear explanations of complex topics. Excellent!",
        "Best ML tutorial for beginners. Highly recommended!"
    ]
}

def get_mock_videos_for_topic(topic: str, max_results: int = 10):
    """Get mock videos for a given topic"""
    topic_lower = topic.lower()
    
    # Simple keyword matching
    if "python" in topic_lower:
        return MOCK_VIDEOS["python programming"][:max_results]
    elif "data structure" in topic_lower or "algorithm" in topic_lower:
        return MOCK_VIDEOS["data structures"][:max_results]
    elif "machine learning" in topic_lower or "ml" in topic_lower or "ai" in topic_lower:
        return MOCK_VIDEOS["machine learning"][:max_results]
    else:
        # Return a mix for unknown topics
        all_videos = []
        for videos in MOCK_VIDEOS.values():
            all_videos.extend(videos)
        return all_videos[:max_results]

def get_mock_transcript(video_id: str):
    """Get mock transcript for a video"""
    return MOCK_TRANSCRIPTS.get(video_id, "This is a sample transcript for educational content.")

def get_mock_comments(video_id: str):
    """Get mock comments for a video"""
    return MOCK_COMMENTS.get(video_id, [
        "Great tutorial! Very helpful.",
        "Thanks for the clear explanation.",
        "This helped me understand the topic better.",
        "Excellent content. Highly recommend!",
        "Perfect for learning this subject."
    ])