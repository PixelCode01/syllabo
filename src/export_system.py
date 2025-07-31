import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from .logger import SyllaboLogger

class ExportSystem:
    def __init__(self):
        self.logger = SyllaboLogger("export_system")
    
    def _get_resource_url(self, resource: Dict) -> str:
        """Get the appropriate URL for a video or playlist"""
        resource_type = resource.get('type', 'video')
        if resource_type == 'playlist':
            return f"https://youtube.com/playlist?list={resource['id']}"
        else:
            return f"https://youtube.com/watch?v={resource['id']}"
    
    def export_to_csv(self, videos: List[Dict], topic: str, filename: Optional[str] = None) -> str:
        """Export video results to CSV format"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"syllabo_export_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'topic', 'title', 'channel', 'url', 'type', 'duration', 
                    'view_count', 'video_count', 'relevance_score', 'composite_score',
                    'transcript_available'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for video in videos:
                    writer.writerow({
                        'topic': topic,
                        'title': video['title'],
                        'channel': video['channel'],
                        'url': self._get_resource_url(video),
                        'type': video.get('type', 'video'),
                        'duration': video.get('duration', ''),
                        'view_count': video.get('view_count', 0),
                        'video_count': video.get('video_count', 0) if video.get('type') == 'playlist' else '',
                        'relevance_score': video.get('relevance_score', 0),
                        'composite_score': video.get('composite_score', 0),
                        'transcript_available': video.get('transcript_available', False)
                    })
            
            self.logger.info(f"Exported {len(videos)} videos to CSV: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"CSV export failed: {e}")
            raise
    
    def export_to_json(self, videos: List[Dict], topic: str, filename: Optional[str] = None) -> str:
        """Export video results to JSON format"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"syllabo_export_{timestamp}.json"
        
        try:
            export_data = {
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "video_count": len(videos),
                "resources": [
                    {
                        "title": v["title"],
                        "channel": v["channel"],
                        "url": self._get_resource_url(v),
                        "type": v.get("type", "video"),
                        "duration": v.get("duration", ""),
                        "view_count": v.get("view_count", 0),
                        "video_count": v.get("video_count", 0) if v.get("type") == "playlist" else None,
                        "relevance_score": v.get("relevance_score", 0),
                        "composite_score": v.get("composite_score", 0),
                        "transcript_available": v.get("transcript_available", False),
                        "description": v.get("description", "")[:200] + "..." if len(v.get("description", "")) > 200 else v.get("description", "")
                    }
                    for v in videos
                ]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Exported {len(videos)} videos to JSON: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"JSON export failed: {e}")
            raise
    
    def export_to_markdown(self, videos: List[Dict], topic: str, filename: Optional[str] = None) -> str:
        """Export video results to Markdown format"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"syllabo_export_{timestamp}.md"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Video Recommendations for: {topic}\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total videos: {len(videos)}\n\n")
                
                for i, video in enumerate(videos, 1):
                    resource_type = video.get('type', 'video')
                    type_indicator = "[PLAYLIST]" if resource_type == 'playlist' else "[VIDEO]"
                    
                    f.write(f"## {i}. {type_indicator} {video['title']}\n\n")
                    f.write(f"**Channel:** {video['channel']}\n\n")
                    
                    if resource_type == 'playlist':
                        f.write(f"**URL:** [View Playlist on YouTube]({self._get_resource_url(video)})\n\n")
                        f.write(f"**Videos in Playlist:** {video.get('video_count', 0)}\n\n")
                        f.write(f"**Total Views:** {video.get('total_views', 0):,}\n\n")
                    else:
                        f.write(f"**URL:** [Watch on YouTube]({self._get_resource_url(video)})\n\n")
                        f.write(f"**Duration:** {video.get('duration', 'Unknown')}\n\n")
                        f.write(f"**Views:** {video.get('view_count', 0):,}\n\n")
                    
                    f.write(f"**Relevance Score:** {video.get('relevance_score', 0):.1f}/10\n\n")
                    f.write(f"**Overall Score:** {video.get('composite_score', 0):.1f}/10\n\n")
                    
                    if resource_type == 'video':
                        if video.get('transcript_available'):
                            f.write("**Transcript:** Available ✅\n\n")
                        else:
                            f.write("**Transcript:** Not available ❌\n\n")
                    
                    if video.get('description'):
                        desc = video['description'][:300] + "..." if len(video['description']) > 300 else video['description']
                        f.write(f"**Description:** {desc}\n\n")
                    
                    f.write("---\n\n")
            
            self.logger.info(f"Exported {len(videos)} videos to Markdown: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Markdown export failed: {e}")
            raise 
   def export_to_html(self, videos: List[Dict], topic: str, filename: Optional[str] = None) -> str:
        """Export video results to HTML format"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"syllabo_export_{timestamp}.html"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Recommendations: {topic}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; }}
        .video-card {{ border: 1px solid #ddd; margin: 20px 0; padding: 20px; border-radius: 8px; background: #fafafa; }}
        .video-title {{ color: #2c3e50; font-size: 1.3em; font-weight: bold; margin-bottom: 10px; }}
        .video-meta {{ color: #666; margin: 5px 0; }}
        .score {{ background: #3498db; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.9em; }}
        .high-score {{ background: #27ae60; }}
        .medium-score {{ background: #f39c12; }}
        .low-score {{ background: #e74c3c; }}
        .description {{ margin-top: 10px; font-style: italic; color: #555; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat {{ background: #ecf0f1; padding: 10px; border-radius: 5px; text-align: center; }}
        a {{ color: #e74c3c; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Video Recommendations for: {topic}</h1>
        <div class="stats">
            <div class="stat">
                <strong>{len(videos)}</strong><br>Total Videos
            </div>
            <div class="stat">
                <strong>{datetime.now().strftime('%Y-%m-%d')}</strong><br>Generated
            </div>
            <div class="stat">
                <strong>{sum(1 for v in videos if v.get('transcript_available'))}</strong><br>With Transcripts
            </div>
        </div>
""")
                
                for i, video in enumerate(videos, 1):
                    score = video.get('composite_score', 0)
                    score_class = 'high-score' if score >= 7 else 'medium-score' if score >= 5 else 'low-score'
                    resource_type = video.get('type', 'video')
                    type_indicator = "[PLAYLIST]" if resource_type == 'playlist' else "[VIDEO]"
                    
                    f.write(f"""
        <div class="video-card">
            <div class="video-title">{i}. {type_indicator} {video['title']}</div>
            <div class="video-meta">📺 <strong>Channel:</strong> {video['channel']}</div>
            <div class="video-meta">🔗 <strong>URL:</strong> <a href="{self._get_resource_url(video)}" target="_blank">{'View Playlist' if resource_type == 'playlist' else 'Watch Video'} on YouTube</a></div>""")
                    
                    if resource_type == 'playlist':
                        f.write(f"""
            <div class="video-meta">📹 <strong>Videos:</strong> {video.get('video_count', 0)}</div>
            <div class="video-meta">👀 <strong>Total Views:</strong> {video.get('total_views', 0):,}</div>""")
                    else:
                        f.write(f"""
            <div class="video-meta">⏱️ <strong>Duration:</strong> {video.get('duration', 'Unknown')}</div>
            <div class="video-meta">👀 <strong>Views:</strong> {video.get('view_count', 0):,}</div>""")
                    
                    f.write(f"""
            <div class="video-meta">
                📊 <strong>Scores:</strong> 
                <span class="score">Relevance: {video.get('relevance_score', 0):.1f}/10</span>
                <span class="score {score_class}">Overall: {score:.1f}/10</span>
            </div>""")
                    
                    if resource_type == 'video':
                        f.write(f"""
            <div class="video-meta">📝 <strong>Transcript:</strong> {'Available ✅' if video.get('transcript_available') else 'Not available ❌'}</div>""")
                    
                    if video.get('description'):
                        desc = video['description'][:400] + "..." if len(video['description']) > 400 else video['description']
                        f.write(f'            <div class="description">{desc}</div>\n')
                    
                    f.write("        </div>\n")
                
                f.write("""
    </div>
</body>
</html>""")
            
            self.logger.info(f"Exported {len(videos)} videos to HTML: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"HTML export failed: {e}")
            raise
    
    def export_comprehensive(self, topics_videos: Dict[str, List[Dict]], 
                           format_type: str = 'json', filename: Optional[str] = None) -> str:
        """Export comprehensive results for multiple topics"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"syllabo_comprehensive_{timestamp}.{format_type}"
        
        if format_type == 'json':
            return self._export_comprehensive_json(topics_videos, filename)
        elif format_type == 'csv':
            return self._export_comprehensive_csv(topics_videos, filename)
        elif format_type == 'html':
            return self._export_comprehensive_html(topics_videos, filename)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _export_comprehensive_json(self, topics_videos: Dict[str, List[Dict]], filename: str) -> str:
        """Export comprehensive JSON"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "topics_count": len(topics_videos),
            "total_videos": sum(len(videos) for videos in topics_videos.values()),
            "topics": {}
        }
        
        for topic, videos in topics_videos.items():
            export_data["topics"][topic] = {
                "resource_count": len(videos),
                "resources": [
                    {
                        "title": v["title"],
                        "channel": v["channel"],
                        "url": self._get_resource_url(v),
                        "type": v.get("type", "video"),
                        "duration": v.get("duration", ""),
                        "view_count": v.get("view_count", 0),
                        "video_count": v.get("video_count", 0) if v.get("type") == "playlist" else None,
                        "relevance_score": v.get("relevance_score", 0),
                        "composite_score": v.get("composite_score", 0)
                    }
                    for v in videos
                ]
            }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filename