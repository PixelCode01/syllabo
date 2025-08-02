import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from .logger import SyllaboLogger

class SyllaboDatabase:
    def __init__(self, db_path: str = "data/syllabo.db"):
        self.db_path = db_path
        self.logger = SyllaboLogger("database")
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            # Create data directory if it doesn't exist
            import os
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS syllabi (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        syllabus_id INTEGER,
                        name TEXT NOT NULL,
                        subtopics TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (syllabus_id) REFERENCES syllabi (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS videos (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        channel TEXT,
                        description TEXT,
                        duration TEXT,
                        view_count INTEGER,
                        like_count INTEGER,
                        relevance_score REAL,
                        sentiment_score REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS topic_videos (
                        topic_id INTEGER,
                        video_id TEXT,
                        relevance_score REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (topic_id, video_id),
                        FOREIGN KEY (topic_id) REFERENCES topics (id),
                        FOREIGN KEY (video_id) REFERENCES videos (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        video_id TEXT,
                        topic_id INTEGER,
                        rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                        comment TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (video_id) REFERENCES videos (id),
                        FOREIGN KEY (topic_id) REFERENCES topics (id)
                    )
                ''')
                
                conn.commit()
                self.logger.info("Database initialized successfully")
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
    
    def save_syllabus(self, title: str, content: str) -> int:
        """Save syllabus and return its ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO syllabi (title, content) VALUES (?, ?)",
                    (title, content)
                )
                return cursor.lastrowid
        except Exception as e:
            self.logger.error(f"Failed to save syllabus: {e}")
            return -1
    
    def save_topics(self, syllabus_id: int, topics: List[Dict]) -> List[int]:
        """Save topics and return their IDs"""
        topic_ids = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for topic in topics:
                    subtopics_json = json.dumps(topic.get("subtopics", []))
                    cursor.execute(
                        "INSERT INTO topics (syllabus_id, name, subtopics) VALUES (?, ?, ?)",
                        (syllabus_id, topic["name"], subtopics_json)
                    )
                    topic_ids.append(cursor.lastrowid)
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to save topics: {e}")
        return topic_ids
    
    def save_video(self, video: Dict) -> bool:
        """Save or update video information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO videos 
                    (id, title, channel, description, duration, view_count, like_count, relevance_score, sentiment_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    video['id'], video['title'], video['channel'], 
                    video.get('description', ''), video.get('duration', ''),
                    video.get('view_count', 0), video.get('like_count', 0),
                    video.get('relevance_score', 0), video.get('sentiment_score', 0)
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Failed to save video: {e}")
            return False
    
    def link_topic_video(self, topic_id: int, video_id: str, relevance_score: float):
        """Link a topic with a video"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO topic_videos (topic_id, video_id, relevance_score) VALUES (?, ?, ?)",
                    (topic_id, video_id, relevance_score)
                )
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to link topic-video: {e}")
    
    def get_syllabus_by_id(self, syllabus_id: int) -> Optional[Dict]:
        """Get a single syllabus by its ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM syllabi WHERE id = ?",
                    (syllabus_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Failed to get syllabus by ID: {e}")
            return None

    def get_topics_by_syllabus_id(self, syllabus_id: int) -> List[Dict]:
        """Get all topics for a given syllabus ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM topics WHERE syllabus_id = ?",
                    (syllabus_id,)
                )
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Failed to get topics by syllabus ID: {e}")
            return []

    def get_recent_syllabi(self, limit: int = 10) -> List[Dict]:
        """Get recent syllabi"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, title, created_at FROM syllabi ORDER BY created_at DESC LIMIT ?",
                    (limit,)
                )
                return [{"id": row[0], "title": row[1], "created_at": row[2]} for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Failed to get recent syllabi: {e}")
            return []
    
    def get_recent_analyses(self, limit: int = 10) -> List[Dict]:
        """Get recent analyses with topic counts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT s.id, s.title, s.created_at, COUNT(t.id) as topic_count
                    FROM syllabi s
                    LEFT JOIN topics t ON s.id = t.syllabus_id
                    GROUP BY s.id, s.title, s.created_at
                    ORDER BY s.created_at DESC
                    LIMIT ?
                ''', (limit,))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        'id': row[0],
                        'title': row[1],
                        'created_at': row[2],
                        'topic_count': row[3]
                    })
                return results
        except Exception as e:
            self.logger.error(f"Failed to get recent analyses: {e}")
            return []
    
    def get_analysis_by_id(self, analysis_id: int) -> Optional[Dict]:
        """Get complete analysis data by ID"""
        try:
            syllabus = self.get_syllabus_by_id(analysis_id)
            if not syllabus:
                return None
            
            topics = self.get_topics_by_syllabus_id(analysis_id)
            
            return {
                'syllabus': syllabus,
                'topics': topics,
                'id': analysis_id
            }
        except Exception as e:
            self.logger.error(f"Failed to get analysis by ID: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT 1')
                return True
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            return False
    
    def get_topic_videos(self, topic_id: int, limit: int = 10) -> List[Dict]:
        """Get videos for a specific topic"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT v.*, tv.relevance_score 
                    FROM videos v 
                    JOIN topic_videos tv ON v.id = tv.video_id 
                    WHERE tv.topic_id = ? 
                    ORDER BY tv.relevance_score DESC 
                    LIMIT ?
                ''', (topic_id, limit))
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Failed to get topic videos: {e}")
            return []