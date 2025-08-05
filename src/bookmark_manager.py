from typing import Dict, List, Optional
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from .logger import SyllaboLogger

@dataclass
class Bookmark:
    """Represents a bookmark with timestamp and notes"""
    id: str
    video_id: str
    video_title: str
    timestamp: str  # Format: "MM:SS" or "HH:MM:SS"
    timestamp_seconds: int
    note: str
    tags: List[str]
    created_at: str
    topic: str
    importance: int  # 1-5 scale

class BookmarkManager:
    """Manage video bookmarks and timestamps"""
    
    def __init__(self):
        self.logger = SyllaboLogger("bookmark_manager")
        self.bookmarks_file = "data/bookmarks.json"
        self.bookmarks = self._load_bookmarks()
    
    def _load_bookmarks(self) -> Dict[str, Bookmark]:
        """Load bookmarks from file"""
        try:
            with open(self.bookmarks_file, 'r') as f:
                data = json.load(f)
                return {
                    bookmark_id: Bookmark(**bookmark_data)
                    for bookmark_id, bookmark_data in data.items()
                }
        except FileNotFoundError:
            return {}
    
    def _save_bookmarks(self):
        """Save bookmarks to file"""
        data = {bookmark_id: asdict(bookmark) for bookmark_id, bookmark in self.bookmarks.items()}
        with open(self.bookmarks_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_bookmark(self, video_id: str, video_title: str, timestamp: str,
                    note: str, topic: str, tags: List[str] = None, 
                    importance: int = 3) -> str:
        """Add a new bookmark"""
        bookmark_id = f"bookmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        timestamp_seconds = self._parse_timestamp(timestamp)
        
        bookmark = Bookmark(
            id=bookmark_id,
            video_id=video_id,
            video_title=video_title,
            timestamp=timestamp,
            timestamp_seconds=timestamp_seconds,
            note=note,
            tags=tags or [],
            created_at=datetime.now().isoformat(),
            topic=topic,
            importance=importance
        )
        
        self.bookmarks[bookmark_id] = bookmark
        self._save_bookmarks()
        
        self.logger.info(f"Added bookmark: {video_title} at {timestamp}")
        return bookmark_id
    
    def _parse_timestamp(self, timestamp: str) -> int:
        """Convert timestamp string to seconds"""
        try:
            parts = timestamp.split(':')
            if len(parts) == 2:  # MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            else:
                return 0
        except ValueError:
            return 0
    
    def get_bookmarks_by_video(self, video_id: str) -> List[Bookmark]:
        """Get all bookmarks for a specific video"""
        return [b for b in self.bookmarks.values() if b.video_id == video_id]
    
    def get_bookmarks_by_topic(self, topic: str) -> List[Bookmark]:
        """Get all bookmarks for a specific topic"""
        return [b for b in self.bookmarks.values() if b.topic.lower() == topic.lower()]
    
    def search_bookmarks(self, query: str) -> List[Bookmark]:
        """Search bookmarks by note content or tags"""
        query_lower = query.lower()
        results = []
        
        for bookmark in self.bookmarks.values():
            if (query_lower in bookmark.note.lower() or 
                any(query_lower in tag.lower() for tag in bookmark.tags) or
                query_lower in bookmark.video_title.lower()):
                results.append(bookmark)
        
        return results
    
    def get_important_bookmarks(self, min_importance: int = 4) -> List[Bookmark]:
        """Get bookmarks marked as important"""
        return [b for b in self.bookmarks.values() if b.importance >= min_importance]
    
    def organize_by_tags(self) -> Dict[str, List[Bookmark]]:
        """Organize bookmarks by tags"""
        tag_groups = {}
        
        for bookmark in self.bookmarks.values():
            for tag in bookmark.tags:
                if tag not in tag_groups:
                    tag_groups[tag] = []
                tag_groups[tag].append(bookmark)
        
        return tag_groups
    
    def export_bookmarks(self, format_type: str = "json") -> str:
        """Export bookmarks to different formats"""
        if format_type == "json":
            return self._export_json()
        elif format_type == "csv":
            return self._export_csv()
        elif format_type == "markdown":
            return self._export_markdown()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _export_json(self) -> str:
        """Export bookmarks as JSON"""
        filename = f"bookmarks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "total_bookmarks": len(self.bookmarks),
            "bookmarks": [asdict(bookmark) for bookmark in self.bookmarks.values()]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename
    
    def _export_csv(self) -> str:
        """Export bookmarks as CSV"""
        import csv
        
        filename = f"bookmarks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Video Title', 'Timestamp', 'Note', 'Topic', 'Tags', 'Importance', 'Created'])
            
            for bookmark in self.bookmarks.values():
                writer.writerow([
                    bookmark.video_title,
                    bookmark.timestamp,
                    bookmark.note,
                    bookmark.topic,
                    ', '.join(bookmark.tags),
                    bookmark.importance,
                    bookmark.created_at
                ])
        
        return filename
    
    def _export_markdown(self) -> str:
        """Export bookmarks as Markdown"""
        filename = f"bookmarks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Video Bookmarks\n\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Group by topic
            topics = {}
            for bookmark in self.bookmarks.values():
                if bookmark.topic not in topics:
                    topics[bookmark.topic] = []
                topics[bookmark.topic].append(bookmark)
            
            for topic, bookmarks in topics.items():
                f.write(f"## {topic}\n\n")
                
                for bookmark in sorted(bookmarks, key=lambda x: x.timestamp_seconds):
                    f.write(f"### {bookmark.video_title}\n")
                    f.write(f"**Timestamp:** {bookmark.timestamp}\n\n")
                    f.write(f"**Note:** {bookmark.note}\n\n")
                    if bookmark.tags:
                        f.write(f"**Tags:** {', '.join(bookmark.tags)}\n\n")
                    f.write(f"**Importance:** {'⭐' * bookmark.importance}\n\n")
                    f.write("---\n\n")
        
        return filename
    
    def get_study_session_bookmarks(self, topic: str, max_bookmarks: int = 10) -> List[Bookmark]:
        """Get most important bookmarks for a study session"""
        topic_bookmarks = self.get_bookmarks_by_topic(topic)
        
        # Sort by importance and recency
        sorted_bookmarks = sorted(
            topic_bookmarks,
            key=lambda x: (x.importance, x.created_at),
            reverse=True
        )
        
        return sorted_bookmarks[:max_bookmarks]
    
    def suggest_review_bookmarks(self) -> List[Bookmark]:
        """Suggest bookmarks that should be reviewed"""
        # Get important bookmarks that haven't been accessed recently
        important_bookmarks = self.get_important_bookmarks()
        
        # In a real implementation, would track last access time
        return important_bookmarks[:5]
    
    def get_all_bookmarks(self) -> List[Bookmark]:
        """Get all bookmarks"""
        return list(self.bookmarks.values())