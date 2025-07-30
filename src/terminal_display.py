import os
from typing import List, Dict, Optional
from datetime import datetime

class TerminalDisplay:
    def __init__(self):
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'underline': '\033[4m',
            'end': '\033[0m'
        }
    
    def colorize(self, text: str, color: str) -> str:
        """Add color to text if terminal supports it"""
        if os.name == 'nt':  # Windows
            return text  # Skip colors on Windows for compatibility
        return f"{self.colors.get(color, '')}{text}{self.colors['end']}"
    
    def print_banner(self, title: str = "SYLLABO ENHANCED"):
        """Print a styled banner"""
        banner_width = 70
        print("=" * banner_width)
        print(f"{title:^{banner_width}}")
        print("AI-Powered YouTube Video Finder for Students".center(banner_width))
        print("=" * banner_width)
        print()
    
    def print_topic_analysis_summary(self, found_topics: List[Dict], 
                                   missing_topics: List[str], 
                                   syllabus_title: str):
        """Print topic analysis summary"""
        print(self.colorize("SYLLABUS ANALYSIS SUMMARY", 'bold'))
        print("-" * 50)
        print(f"Syllabus: {syllabus_title}")
        print(f"Analyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if found_topics:
            print(self.colorize(f"TOPICS FOUND ({len(found_topics)})", 'green'))
            print("-" * 30)
            for i, topic in enumerate(found_topics, 1):
                print(f"{i}. {self.colorize(topic['name'], 'cyan')}")
                subtopics = topic.get('subtopics', [])
                if subtopics:
                    for j, subtopic in enumerate(subtopics[:3], 1):
                        print(f"   {j}. {subtopic}")
                    if len(subtopics) > 3:
                        print(f"   ... and {len(subtopics) - 3} more subtopics")
                print()
        else:
            print(self.colorize("NO TOPICS FOUND", 'red'))
            print("The AI couldn't extract clear topics from the syllabus.")
            print()
        
        if missing_topics:
            print(self.colorize(f"UNCLEAR/MISSING TOPICS ({len(missing_topics)})", 'yellow'))
            print("-" * 35)
            for topic in missing_topics:
                print(f"• {topic}")
            print()
            print(self.colorize("Tip:", 'blue'), "These topics might need manual refinement")
            print()
    
    def print_video_search_progress(self, current_topic: int, total_topics: int, 
                                  topic_name: str):
        """Print search progress for current topic"""
        progress = f"[{current_topic}/{total_topics}]"
        print(f"\n{progress} Searching videos for: {self.colorize(topic_name, 'cyan')}")
        print("   " + "▓" * (current_topic * 30 // total_topics) + 
              "░" * (30 - (current_topic * 30 // total_topics)))
    
    def print_top_video_recommendations(self, topic_results: Dict[str, List[Dict]], 
                                      show_top_n: int = 3):
        """Print top video recommendations for each topic"""
        print(self.colorize("\nTOP VIDEO RECOMMENDATIONS", 'bold'))
        print("=" * 70)
        
        if not topic_results:
            print(self.colorize("No video recommendations found", 'red'))
            return
        
        for topic_name, videos in topic_results.items():
            print(f"\nTopic: {self.colorize(topic_name, 'cyan')}")
            print("-" * 60)
            
            if not videos:
                print(self.colorize("   No videos found for this topic", 'red'))
                continue
            
            top_videos = videos[:show_top_n]
            for i, video in enumerate(top_videos, 1):
                self._print_video_card(video, i)
            
            if len(videos) > show_top_n:
                print(f"   ... and {len(videos) - show_top_n} more videos available")
            print()
    
    def _print_video_card(self, video: Dict, rank: int):
        """Print a single video card"""
        title = video['title'][:65] + "..." if len(video['title']) > 65 else video['title']
        print(f"\n   {self.colorize(f'{rank}.', 'bold')} {self.colorize(title, 'white')}")
        
        print(f"      Channel: {video['channel']}")
        video_url = f"https://youtube.com/watch?v={video['id']}"
        print(f"      URL: {self.colorize(video_url, 'blue')}")
        
        duration = video.get('duration', 'Unknown')
        views = video.get('view_count', 0)
        print(f"      Duration: {duration} | Views: {views:,}")
        
        relevance = video.get('relevance_score', 0)
        composite = video.get('composite_score', 0)
        
        relevance_color = self._get_score_color(relevance)
        composite_color = self._get_score_color(composite)
        
        print(f"      Relevance: {self.colorize(f'{relevance:.1f}/10', relevance_color)} | "
              f"Overall: {self.colorize(f'{composite:.1f}/10', composite_color)}")
        
        transcript_status = "Available" if video.get('transcript_available') else "Not available"
        print(f"      Transcript: {transcript_status}")
        
        quality_indicators = []
        if video.get('relevance_score', 0) >= 8:
            quality_indicators.append("Highly Relevant")
        if video.get('sentiment_score', 0) >= 7:
            quality_indicators.append("Well Received")
        if video.get('transcript_available'):
            quality_indicators.append("Has Transcript")
        
        if quality_indicators:
            print(f"      Tags: {' | '.join(quality_indicators)}")
    
    def _get_score_color(self, score: float) -> str:
        """Get color based on score value"""
        if score >= 8:
            return 'green'
        elif score >= 6:
            return 'yellow'
        else:
            return 'red'
    
    def print_quick_links_summary(self, topic_results: Dict[str, List[Dict]]):
        """Print a quick summary with just the top links"""
        print(self.colorize("\nQUICK LINKS - TOP RECOMMENDATIONS", 'bold'))
        print("=" * 60)
        
        for topic_name, videos in topic_results.items():
            if videos:
                top_video = videos[0]
                print(f"\n{self.colorize(topic_name, 'cyan')}")
                print(f"   Best: {top_video['title'][:50]}...")
                print(f"   Link: {self.colorize(f'https://youtube.com/watch?v={top_video['id']}', 'blue')}")
                print(f"   Score: {top_video.get('relevance_score', 0):.1f}/10")
    
    def print_topic_coverage_analysis(self, requested_topics: List[str], 
                                    found_videos: Dict[str, List[Dict]]):
        """Analyze and display topic coverage"""
        print(self.colorize("\nTOPIC COVERAGE ANALYSIS", 'bold'))
        print("-" * 50)
        
        covered_topics = []
        partially_covered = []
        not_covered = []
        
        for topic in requested_topics:
            videos = found_videos.get(topic, [])
            if not videos:
                not_covered.append(topic)
            elif len(videos) < 3 or (videos and videos[0].get('relevance_score', 0) < 6):
                partially_covered.append(topic)
            else:
                covered_topics.append(topic)
        
        total_topics = len(requested_topics)
        coverage_percent = (len(covered_topics) / total_topics * 100) if total_topics > 0 else 0
        
        print(f"Overall Coverage: {self.colorize(f'{coverage_percent:.1f}%', 'green' if coverage_percent >= 70 else 'yellow')}")
        print(f"Topics Analysis:")
        print(f"   Well Covered: {len(covered_topics)}")
        print(f"   Partially Covered: {len(partially_covered)}")
        print(f"   Not Covered: {len(not_covered)}")
        print()
        
        if covered_topics:
            print(self.colorize("WELL COVERED TOPICS:", 'green'))
            for topic in covered_topics:
                video_count = len(found_videos.get(topic, []))
                avg_score = sum(v.get('relevance_score', 0) for v in found_videos.get(topic, [])) / video_count if video_count > 0 else 0
                print(f"   • {topic} ({video_count} videos, avg score: {avg_score:.1f})")
            print()
        
        if partially_covered:
            print(self.colorize("PARTIALLY COVERED TOPICS:", 'yellow'))
            for topic in partially_covered:
                video_count = len(found_videos.get(topic, []))
                print(f"   • {topic} ({video_count} videos found)")
            print()
        
        if not_covered:
            print(self.colorize("NOT COVERED TOPICS:", 'red'))
            for topic in not_covered:
                print(f"   • {topic}")
            print(f"\nSuggestion: Try searching these topics manually or refine the topic names")
            print()
    
    def print_export_options(self, available_formats: List[str]):
        """Print available export options"""
        print(self.colorize("\n💾 EXPORT OPTIONS", 'bold'))
        print("-" * 30)
        print("Save your results in multiple formats:")
        for fmt in available_formats:
            print(f"   • {fmt.upper()}: Structured data export")
        print(f"\n💡 Use: python syllabo_enhanced.py export --format [format]")
        print()
    
    def print_completion_summary(self, total_topics: int, total_videos: int, 
                               processing_time: float):
        """Print final completion summary"""
        print(self.colorize("\nANALYSIS COMPLETE!", 'bold'))
        print("=" * 50)
        print(f"Topics Processed: {total_topics}")
        print(f"Videos Analyzed: {total_videos}")
        print(f"Processing Time: {processing_time:.1f} seconds")
        print(f"Average Videos per Topic: {total_videos/total_topics:.1f}" if total_topics > 0 else "")
        print()
        print(self.colorize("Next Steps:", 'blue'))
        print("   • Click on the video links to watch")
        print("   • Export results for future reference")
        print("   • Rate videos to improve future recommendations")
        print()