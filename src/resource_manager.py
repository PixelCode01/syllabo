#!/usr/bin/env python3
"""
Enhanced Resource Manager - Provides direct links and persistent storage
Addresses user feedback about linking and saving resources
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from .logger import SyllaboLogger

class ResourceManager:
    """Enhanced resource manager with direct linking and persistent storage"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.resources_dir = self.data_dir / "resources"
        self.exports_dir = Path("exports")
        self.logger = SyllaboLogger("resource_manager")
        
        # Create directories
        self.resources_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
    
    def save_learning_resources(self, topic: str, resources: Dict, 
                              include_links: bool = True) -> Dict[str, str]:
        """Save resources with direct links to multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = self._sanitize_filename(topic)
        
        saved_files = {}
        
        # Save as JSON (structured data)
        json_file = self.resources_dir / f"{safe_topic}_{timestamp}.json"
        enhanced_resources = self._enhance_resources_with_links(resources)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'topic': topic,
                'generated_at': datetime.now().isoformat(),
                'resources': enhanced_resources,
                'total_count': self._count_total_resources(enhanced_resources)
            }, f, indent=2, ensure_ascii=False)
        
        saved_files['json'] = str(json_file)
        
        # Save as readable text file
        txt_file = self.exports_dir / f"{safe_topic}_resources_{timestamp}.txt"
        self._save_as_readable_text(txt_file, topic, enhanced_resources)
        saved_files['text'] = str(txt_file)
        
        # Save as CSV for spreadsheet use
        csv_file = self.exports_dir / f"{safe_topic}_resources_{timestamp}.csv"
        self._save_as_csv(csv_file, enhanced_resources)
        saved_files['csv'] = str(csv_file)
        
        # Save as HTML with clickable links
        html_file = self.exports_dir / f"{safe_topic}_resources_{timestamp}.html"
        self._save_as_html(html_file, topic, enhanced_resources)
        saved_files['html'] = str(html_file)
        
        self.logger.info(f"Saved resources for '{topic}' in {len(saved_files)} formats")
        return saved_files
    
    def _enhance_resources_with_links(self, resources: Dict) -> Dict:
        """Add direct clickable links to all resources"""
        enhanced = {}
        
        # Process videos with direct YouTube links
        if 'videos' in resources:
            enhanced['videos'] = []
            for video in resources['videos']:
                enhanced_video = video.copy()
                if 'id' in video:
                    enhanced_video['direct_link'] = f"https://www.youtube.com/watch?v={video['id']}"
                    enhanced_video['embed_link'] = f"https://www.youtube.com/embed/{video['id']}"
                enhanced['videos'].append(enhanced_video)
        
        # Process playlists with direct links
        if 'playlists' in resources:
            enhanced['playlists'] = []
            for playlist in resources['playlists']:
                enhanced_playlist = playlist.copy()
                if 'id' in playlist:
                    enhanced_playlist['direct_link'] = f"https://www.youtube.com/playlist?list={playlist['id']}"
                enhanced['playlists'].append(enhanced_playlist)
        
        # Process books with search links
        if 'books' in resources:
            enhanced['books'] = []
            for book in resources['books']:
                enhanced_book = book.copy()
                title = book.get('title', '')
                author = book.get('author', '')
                
                # Add search links
                enhanced_book['amazon_search'] = f"https://www.amazon.com/s?k={self._url_encode(f'{title} {author}')}"
                enhanced_book['google_books'] = f"https://books.google.com/books?q={self._url_encode(f'{title} {author}')}"
                enhanced_book['goodreads_search'] = f"https://www.goodreads.com/search?q={self._url_encode(title)}"
                
                enhanced['books'].append(enhanced_book)
        
        # Process courses with platform links
        if 'courses' in resources:
            enhanced['courses'] = []
            for course in resources['courses']:
                enhanced_course = course.copy()
                title = course.get('title', '')
                platform = course.get('platform', '').lower()
                
                # Add platform-specific search links
                if 'coursera' in platform:
                    enhanced_course['platform_search'] = f"https://www.coursera.org/search?query={self._url_encode(title)}"
                elif 'udemy' in platform:
                    enhanced_course['platform_search'] = f"https://www.udemy.com/courses/search/?q={self._url_encode(title)}"
                elif 'edx' in platform:
                    enhanced_course['platform_search'] = f"https://www.edx.org/search?q={self._url_encode(title)}"
                else:
                    enhanced_course['google_search'] = f"https://www.google.com/search?q={self._url_encode(f'{title} {platform} course')}"
                
                enhanced['courses'].append(enhanced_course)
        
        # Copy other resource types
        for key, value in resources.items():
            if key not in ['videos', 'playlists', 'books', 'courses']:
                enhanced[key] = value
        
        return enhanced
    
    def _save_as_readable_text(self, file_path: Path, topic: str, resources: Dict):
        """Save resources as a readable text file with direct links"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"LEARNING RESOURCES FOR: {topic.upper()}\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # YouTube Videos Section
            if 'videos' in resources and resources['videos']:
                f.write("🎥 YOUTUBE VIDEOS\n")
                f.write("-" * 30 + "\n")
                for i, video in enumerate(resources['videos'], 1):
                    f.write(f"{i}. {video.get('title', 'Unknown Title')}\n")
                    f.write(f"   Channel: {video.get('channel', 'Unknown')}\n")
                    f.write(f"   Duration: {video.get('duration', 'Unknown')}\n")
                    f.write(f"   Views: {video.get('view_count', 0):,}\n")
                    if 'direct_link' in video:
                        f.write(f"   🔗 DIRECT LINK: {video['direct_link']}\n")
                    if video.get('description'):
                        desc = video['description'][:200] + "..." if len(video['description']) > 200 else video['description']
                        f.write(f"   Description: {desc}\n")
                    f.write("\n")
            
            # YouTube Playlists Section
            if 'playlists' in resources and resources['playlists']:
                f.write("📚 YOUTUBE PLAYLISTS\n")
                f.write("-" * 30 + "\n")
                for i, playlist in enumerate(resources['playlists'], 1):
                    f.write(f"{i}. {playlist.get('title', 'Unknown Playlist')}\n")
                    f.write(f"   Channel: {playlist.get('channel', 'Unknown')}\n")
                    f.write(f"   Videos: {playlist.get('video_count', 0)} videos\n")
                    f.write(f"   Total Views: {playlist.get('total_views', 0):,}\n")
                    if 'direct_link' in playlist:
                        f.write(f"   🔗 DIRECT LINK: {playlist['direct_link']}\n")
                    f.write("\n")
            
            # Books Section
            if 'books' in resources and resources['books']:
                f.write("📖 RECOMMENDED BOOKS\n")
                f.write("-" * 30 + "\n")
                for i, book in enumerate(resources['books'], 1):
                    f.write(f"{i}. {book.get('title', 'Unknown Title')}\n")
                    f.write(f"   Author: {book.get('author', 'Unknown')}\n")
                    f.write(f"   Price: {book.get('price', 'Check price')}\n")
                    f.write(f"   Type: {book.get('type', 'Unknown').title()}\n")
                    
                    # Add search links
                    if 'amazon_search' in book:
                        f.write(f"   🛒 Amazon: {book['amazon_search']}\n")
                    if 'google_books' in book:
                        f.write(f"   📚 Google Books: {book['google_books']}\n")
                    f.write("\n")
            
            # Courses Section
            if 'courses' in resources and resources['courses']:
                f.write("🎓 ONLINE COURSES\n")
                f.write("-" * 30 + "\n")
                for i, course in enumerate(resources['courses'], 1):
                    f.write(f"{i}. {course.get('title', 'Unknown Course')}\n")
                    f.write(f"   Platform: {course.get('platform', 'Unknown')}\n")
                    f.write(f"   Price: {course.get('price', 'Check platform')}\n")
                    f.write(f"   Type: {course.get('type', 'Unknown').title()}\n")
                    
                    # Add platform links
                    if 'platform_search' in course:
                        f.write(f"   🔗 Platform Link: {course['platform_search']}\n")
                    elif 'google_search' in course:
                        f.write(f"   🔍 Search: {course['google_search']}\n")
                    f.write("\n")
            
            # Study Plan Section
            if 'coverage_analysis' in resources:
                f.write("📋 RECOMMENDED STUDY PLAN\n")
                f.write("-" * 30 + "\n")
                coverage = resources['coverage_analysis']
                
                if 'recommended_study_order' in coverage:
                    total_time = 0
                    for i, item in enumerate(coverage['recommended_study_order'], 1):
                        resource = item.get('resource', {})
                        purpose = item.get('purpose', 'Study material')
                        duration = item.get('estimated_minutes', 0)
                        total_time += duration
                        
                        f.write(f"{i}. {resource.get('title', 'Unknown')}\n")
                        f.write(f"   Purpose: {purpose}\n")
                        f.write(f"   Time: {duration} minutes\n")
                        if 'direct_link' in resource:
                            f.write(f"   Link: {resource['direct_link']}\n")
                        f.write("\n")
                    
                    f.write(f"Total Estimated Study Time: {total_time} minutes ({total_time/60:.1f} hours)\n\n")
            
            # Footer
            f.write("=" * 60 + "\n")
            f.write("💡 TIP: Copy and paste the links above into your browser\n")
            f.write("📱 Save this file for future reference\n")
            f.write("🔄 Use Syllabo to generate quizzes from these resources\n")
    
    def _save_as_csv(self, file_path: Path, resources: Dict):
        """Save resources as CSV for spreadsheet applications"""
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Type', 'Title', 'Author/Channel', 'Duration/Price', 'Direct Link', 'Description'])
            
            # Videos
            if 'videos' in resources:
                for video in resources['videos']:
                    writer.writerow([
                        'YouTube Video',
                        video.get('title', ''),
                        video.get('channel', ''),
                        video.get('duration', ''),
                        video.get('direct_link', ''),
                        video.get('description', '')[:100] + '...' if len(video.get('description', '')) > 100 else video.get('description', '')
                    ])
            
            # Playlists
            if 'playlists' in resources:
                for playlist in resources['playlists']:
                    writer.writerow([
                        'YouTube Playlist',
                        playlist.get('title', ''),
                        playlist.get('channel', ''),
                        f"{playlist.get('video_count', 0)} videos",
                        playlist.get('direct_link', ''),
                        playlist.get('description', '')
                    ])
            
            # Books
            if 'books' in resources:
                for book in resources['books']:
                    writer.writerow([
                        'Book',
                        book.get('title', ''),
                        book.get('author', ''),
                        book.get('price', ''),
                        book.get('amazon_search', ''),
                        f"Topics: {', '.join(book.get('topics', []))}"
                    ])
            
            # Courses
            if 'courses' in resources:
                for course in resources['courses']:
                    writer.writerow([
                        'Online Course',
                        course.get('title', ''),
                        course.get('platform', ''),
                        course.get('price', ''),
                        course.get('platform_search', ''),
                        f"Topics: {', '.join(course.get('topics', []))}"
                    ])
    
    def _save_as_html(self, file_path: Path, topic: str, resources: Dict):
        """Save resources as HTML with clickable links"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learning Resources: {topic}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .section {{ margin-bottom: 30px; }}
        .resource-card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .resource-card:hover {{ background-color: #f9f9f9; }}
        .link-button {{ background: #3498db; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; margin: 5px; display: inline-block; }}
        .link-button:hover {{ background: #2980b9; }}
        .video {{ border-left: 4px solid #e74c3c; }}
        .playlist {{ border-left: 4px solid #9b59b6; }}
        .book {{ border-left: 4px solid #f39c12; }}
        .course {{ border-left: 4px solid #27ae60; }}
        .stats {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Learning Resources: {topic}</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
"""
        
        # Videos section
        if 'videos' in resources and resources['videos']:
            html_content += """
    <div class="section">
        <h2>🎥 YouTube Videos</h2>
"""
            for video in resources['videos']:
                html_content += f"""
        <div class="resource-card video">
            <h3>{video.get('title', 'Unknown Title')}</h3>
            <div class="stats">
                📺 {video.get('channel', 'Unknown')} • ⏱️ {video.get('duration', 'Unknown')} • 👁️ {video.get('view_count', 0):,} views
            </div>
            <p>{video.get('description', 'No description available')[:200]}...</p>
            <a href="{video.get('direct_link', '#')}" class="link-button" target="_blank">▶️ Watch Video</a>
        </div>
"""
            html_content += "    </div>\n"
        
        # Playlists section
        if 'playlists' in resources and resources['playlists']:
            html_content += """
    <div class="section">
        <h2>📚 YouTube Playlists</h2>
"""
            for playlist in resources['playlists']:
                html_content += f"""
        <div class="resource-card playlist">
            <h3>{playlist.get('title', 'Unknown Playlist')}</h3>
            <div class="stats">
                📺 {playlist.get('channel', 'Unknown')} • 📹 {playlist.get('video_count', 0)} videos • 👁️ {playlist.get('total_views', 0):,} total views
            </div>
            <p>{playlist.get('description', 'No description available')}</p>
            <a href="{playlist.get('direct_link', '#')}" class="link-button" target="_blank">📚 View Playlist</a>
        </div>
"""
            html_content += "    </div>\n"
        
        # Books section
        if 'books' in resources and resources['books']:
            html_content += """
    <div class="section">
        <h2>📖 Recommended Books</h2>
"""
            for book in resources['books']:
                html_content += f"""
        <div class="resource-card book">
            <h3>{book.get('title', 'Unknown Title')}</h3>
            <div class="stats">
                ✍️ {book.get('author', 'Unknown')} • 💰 {book.get('price', 'Check price')} • 📊 {book.get('type', 'Unknown').title()}
            </div>
            <p>Topics: {', '.join(book.get('topics', []))}</p>
            <a href="{book.get('amazon_search', '#')}" class="link-button" target="_blank">🛒 Amazon</a>
            <a href="{book.get('google_books', '#')}" class="link-button" target="_blank">📚 Google Books</a>
        </div>
"""
            html_content += "    </div>\n"
        
        # Courses section
        if 'courses' in resources and resources['courses']:
            html_content += """
    <div class="section">
        <h2>🎓 Online Courses</h2>
"""
            for course in resources['courses']:
                html_content += f"""
        <div class="resource-card course">
            <h3>{course.get('title', 'Unknown Course')}</h3>
            <div class="stats">
                🏫 {course.get('platform', 'Unknown')} • 💰 {course.get('price', 'Check platform')} • 📊 {course.get('type', 'Unknown').title()}
            </div>
            <p>Topics: {', '.join(course.get('topics', []))}</p>
            <a href="{course.get('platform_search', course.get('google_search', '#'))}" class="link-button" target="_blank">🔗 Find Course</a>
        </div>
"""
            html_content += "    </div>\n"
        
        html_content += """
    <div class="section">
        <h2>💡 Tips</h2>
        <ul>
            <li>Click the links above to go directly to the resources</li>
            <li>Bookmark this page for future reference</li>
            <li>Use Syllabo to generate quizzes based on these resources</li>
        </ul>
    </div>
</body>
</html>
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def get_saved_resources(self, topic: Optional[str] = None) -> List[Dict]:
        """Get list of saved resource files"""
        saved_resources = []
        
        for json_file in self.resources_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if topic is None or topic.lower() in data.get('topic', '').lower():
                    saved_resources.append({
                        'file': str(json_file),
                        'topic': data.get('topic', 'Unknown'),
                        'generated_at': data.get('generated_at', ''),
                        'total_count': data.get('total_count', 0)
                    })
            except Exception as e:
                self.logger.error(f"Error reading {json_file}: {e}")
        
        return sorted(saved_resources, key=lambda x: x['generated_at'], reverse=True)
    
    def load_saved_resources(self, file_path: str) -> Optional[Dict]:
        """Load previously saved resources"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading resources from {file_path}: {e}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for cross-platform compatibility"""
        import re
        # Remove invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limit length
        return sanitized[:50]
    
    def _url_encode(self, text: str) -> str:
        """URL encode text for search links"""
        import urllib.parse
        return urllib.parse.quote_plus(text)
    
    def _count_total_resources(self, resources: Dict) -> int:
        """Count total number of resources"""
        count = 0
        for key in ['videos', 'playlists', 'books', 'courses']:
            if key in resources:
                count += len(resources[key])
        return count