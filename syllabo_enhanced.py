#!/usr/bin/env python3

import os
import sys
import json
import argparse
import asyncio
import time
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.syllabus_parser import SyllabusParser
from src.youtube_client import YouTubeClient
from src.ai_client import AIClient
from src.video_analyzer import VideoAnalyzer
from src.database import SyllaboDatabase
from src.logger import SyllaboLogger
from src.terminal_display import TerminalDisplay

class EnhancedSyllaboCLI: 
    def __init__(self):
        load_dotenv()
        self.logger = SyllaboLogger("cli")
        self.db = SyllaboDatabase()
        self.ai_client = AIClient()
        self.youtube_client = YouTubeClient()
        self.video_analyzer = VideoAnalyzer(self.ai_client)
        self.syllabus_parser = SyllabusParser()
        self.display = TerminalDisplay()
    
    def print_banner(self):
        self.display.print_banner("SYLLABO ENHANCED")
    
    async def run(self, args):
        self.print_banner()
        
        if args.command == 'analyze':
            await self.analyze_syllabus(args)
        elif args.command == 'search':
            await self.search_videos(args)
        elif args.command == 'history':
            self.show_history(args)
        elif args.command == 'export':
            await self.export_results(args)
        else:
            self.show_help()
    
    async def analyze_syllabus(self, args):
        """Analyze syllabus and extract topics"""
        start_time = time.time()
        
        if args.file:
            if not os.path.exists(args.file):
                print(f"Error: File '{args.file}' not found")
                return
            print(f"\nLoading syllabus from file: {args.file}")
            syllabus_content = self.syllabus_parser.load_from_file(args.file)
            syllabus_title = os.path.basename(args.file)
        elif args.text:
            syllabus_content = args.text
            syllabus_title = f"Direct input - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            print(f"\nAnalyzing provided text content...")
        else:
            print("Error: Please provide either --file or --text")
            return
        
        print("Extracting topics using AI...")
        topics = await self.syllabus_parser.extract_topics(syllabus_content, self.ai_client)
        
        missing_topics = await self._identify_missing_topics(syllabus_content, topics)
        
        self.display.print_topic_analysis_summary(topics, missing_topics, syllabus_title)
        
        if not topics:
            print("No clear topics found. Try refining your syllabus content.")
            return
        
        syllabus_id = self.db.save_syllabus(syllabus_title, syllabus_content)
        topic_ids = self.db.save_topics(syllabus_id, topics)
        
        if args.search_videos:
            print("Searching for videos...")
            topic_results = await self.search_for_topics_enhanced(topics, topic_ids, args.max_videos)
            
            if args.print_results:
                self.display.print_top_video_recommendations(topic_results, args.max_videos)
                self.display.print_quick_links_summary(topic_results)
                
                topic_names = [t['name'] for t in topics]
                self.display.print_topic_coverage_analysis(topic_names, topic_results)
            
            total_videos = sum(len(videos) for videos in topic_results.values())
            processing_time = time.time() - start_time
            self.display.print_completion_summary(len(topics), total_videos, processing_time)
            
            if args.save or args.export_format:
                await self.save_comprehensive_results(topic_results, syllabus_title, args.export_format or 'json')
        else:
            print(f"\nTo search for videos, add --search-videos flag")
            print(f"To see results in terminal, add --print-results flag")
    
    async def search_videos(self, args):
        """Search for videos for a specific topic"""
        if not args.topic:
            print("Error: Please provide a topic to search for")
            return
        
        start_time = time.time()
        print(f"Searching videos for: {args.topic}")
        
        enhanced_query = f"{args.topic} tutorial explained"
        videos = await self.youtube_client.search_videos(enhanced_query, args.max_videos)
        
        if not videos:
            print("No videos found")
            print("Try a different topic name or check your internet connection")
            return
        
        print(f"Found {len(videos)} videos, analyzing with AI...")
        
        analyzed_videos = await self.video_analyzer.analyze_videos(videos, args.topic)
        
        quality_videos = [v for v in analyzed_videos if v.get('relevance_score', 0) >= 3.0]
        
        if not quality_videos:
            print("No high-quality videos found for this topic")
            print("Try refining your topic or search for a broader term")
            return
        
        topic_results = {args.topic: quality_videos}
        
        self.display.print_top_video_recommendations(topic_results, min(args.max_videos, 10))
        self.display.print_quick_links_summary(topic_results)
        
        processing_time = time.time() - start_time
        self.display.print_completion_summary(1, len(quality_videos), processing_time)
        
        if args.save:
            await self.save_video_results(quality_videos, args.topic, args.export_format or 'json')
    
    async def _identify_missing_topics(self, syllabus_content: str, found_topics: List[Dict]) -> List[str]:
        """Identify topics that might have been missed by AI extraction"""
        # Use AI to identify potentially missed topics
        found_topic_names = [t['name'] for t in found_topics]
        found_topics_str = ", ".join(found_topic_names)
        
        prompt = f"""Analyze this syllabus content and identify any important topics that might have been missed.
        
Already found topics: {found_topics_str}

Syllabus content:
{syllabus_content[:1500]}

List any additional important topics that seem to be mentioned but weren't captured in the found topics.
Respond with a simple list, one topic per line, or "None" if no additional topics are found."""
        
        try:
            response = await self.ai_client.get_completion(prompt)
            if response.strip().lower() == "none" or "error:" in response.lower():
                return []
            
            # Parse the response into a list
            missing_topics = [line.strip() for line in response.split('\n') if line.strip() and not line.strip().startswith('-')]
            return missing_topics[:5]  # Limit to 5 additional topics
        except Exception as e:
            self.logger.error(f"Failed to identify missing topics: {e}")
            return []
    
    async def search_for_topics_enhanced(self, topics: List[Dict], topic_ids: List[int], max_videos: int) -> Dict[str, List[Dict]]:
        """Search for videos across all topics"""
        all_results = {}
        
        for i, (topic, topic_id) in enumerate(zip(topics, topic_ids)):
            topic_name = topic['name']
            
            self.display.print_video_search_progress(i + 1, len(topics), topic_name)
            
            try:
                enhanced_query = self._enhance_search_query(topic_name, topic.get('subtopics', []))
                videos = await self.youtube_client.search_videos(enhanced_query, max_videos)
                
                if videos:
                    print(f"   Found {len(videos)} videos, analyzing relevance...")
                    analyzed_videos = await self.video_analyzer.analyze_videos(videos, topic_name)
                    
                    quality_videos = [v for v in analyzed_videos if v.get('relevance_score', 0) >= 4.0]
                    
                    for video in quality_videos:
                        self.db.save_video(video)
                        self.db.link_topic_video(topic_id, video['id'], video['relevance_score'])
                    
                    all_results[topic_name] = quality_videos
                    
                    if quality_videos:
                        top_video = quality_videos[0]
                        print(f"   Top result: {top_video['title'][:50]}... (Relevance: {top_video['relevance_score']:.1f}/10)")
                    else:
                        print(f"   No high-quality videos found (all below 4.0 relevance)")
                else:
                    print(f"   No videos found")
                    all_results[topic_name] = []
                    
            except Exception as e:
                self.logger.error(f"Failed to search videos for {topic_name}: {e}")
                print(f"   Error searching for {topic_name}: {str(e)}")
                all_results[topic_name] = []
        
        return all_results
    
    def _enhance_search_query(self, topic_name: str, subtopics: List[str]) -> str:
        """Build better search query with subtopics"""
        query_parts = [topic_name, "tutorial", "explained"]
        
        if subtopics:
            main_subtopic = subtopics[0]
            query_parts.insert(1, main_subtopic)
        
        enhanced_query = " ".join(query_parts)
        return enhanced_query[:100]
    
    async def search_for_topics(self, topics: List[Dict], topic_ids: List[int], max_videos: int):
        """Search videos for all topics"""
        all_results = {}
        
        for i, (topic, topic_id) in enumerate(zip(topics, topic_ids)):
            topic_name = topic['name']
            print(f"\n🔍 Searching videos for topic {i+1}/{len(topics)}: {topic_name}")
            
            try:
                # Search YouTube
                videos = await self.youtube_client.search_videos(topic_name, max_videos)
                
                if videos:
                    print(f"📹 Analyzing {len(videos)} videos...")
                    analyzed_videos = await self.video_analyzer.analyze_videos(videos, topic_name)
                    
                    # Save to database
                    for video in analyzed_videos:
                        self.db.save_video(video)
                        self.db.link_topic_video(topic_id, video['id'], video['relevance_score'])
                    
                    all_results[topic_name] = analyzed_videos
                    
                    # Show top result
                    if analyzed_videos:
                        top_video = analyzed_videos[0]
                        print(f"   🏆 Top result: {top_video['title'][:60]}... (Score: {top_video['composite_score']:.1f})")
                else:
                    print(f"   ❌ No videos found for {topic_name}")
                    
            except Exception as e:
                self.logger.error(f"Failed to search videos for {topic_name}: {e}")
                print(f"   ❌ Error searching for {topic_name}")
        
        # Display summary
        print(f"\n📊 Search Summary:")
        print("-" * 50)
        total_videos = sum(len(videos) for videos in all_results.values())
        print(f"Total topics processed: {len(topics)}")
        print(f"Total videos found: {total_videos}")
        print(f"Average videos per topic: {total_videos/len(topics):.1f}")
        
        # Save comprehensive results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"syllabo_comprehensive_{timestamp}.json"
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "topics_count": len(topics),
            "total_videos": total_videos,
            "results": {}
        }
        
        for topic_name, videos in all_results.items():
            export_data["results"][topic_name] = [
                {
                    "title": v["title"],
                    "channel": v["channel"],
                    "url": f"https://youtube.com/watch?v={v['id']}",
                    "duration": v["duration"],
                    "relevance_score": v["relevance_score"],
                    "composite_score": v["composite_score"],
                    "view_count": v.get("view_count", 0)
                }
                for v in videos[:5]  # Top 5 per topic
            ]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {filename}")
    

    
    async def save_video_results(self, videos: List[Dict], topic: str, format_type: str = 'json'):
        """Save video results to file"""
        from src.export_system import ExportSystem
        
        export_system = ExportSystem()
        
        try:
            if format_type == 'json':
                filename = export_system.export_to_json(videos, topic)
            elif format_type == 'csv':
                filename = export_system.export_to_csv(videos, topic)
            elif format_type == 'markdown':
                filename = export_system.export_to_markdown(videos, topic)
            elif format_type == 'html':
                filename = export_system.export_to_html(videos, topic)
            else:
                filename = export_system.export_to_json(videos, topic)
            
            print(f"Results saved to: {filename}")
            print(f"Format: {format_type.upper()}")
            
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            print(f"Failed to save results: {e}")
    
    async def save_comprehensive_results(self, topic_results: Dict[str, List[Dict]], 
                                       syllabus_title: str, format_type: str = 'json'):
        """Save comprehensive results for all topics"""
        from src.export_system import ExportSystem
        
        export_system = ExportSystem()
        
        try:
            filename = export_system.export_comprehensive(topic_results, format_type)
            print(f"Comprehensive results saved to: {filename}")
            print(f"Format: {format_type.upper()}")
            print(f"Syllabus: {syllabus_title}")
            
        except Exception as e:
            self.logger.error(f"Failed to save comprehensive results: {e}")
            print(f"Failed to save comprehensive results: {e}")
    
    def show_history(self, args):
        """Show recent syllabi and searches"""
        print("\nRecent Syllabi:")
        print("-" * 50)
        
        recent_syllabi = self.db.get_recent_syllabi(args.limit)
        
        if not recent_syllabi:
            print("No syllabi found in database")
            return
        
        for i, syllabus in enumerate(recent_syllabi, 1):
            print(f"{i}. {syllabus['title']}")
            print(f"   Created: {syllabus['created_at']}")
            print()
    
    async def export_results(self, args):
        """Export results in various formats"""
        print("Export functionality coming soon...")
    
    def show_help(self):
        """Show help information"""
        print("\nSyllabo Enhanced - Usage Examples:")
        print("-" * 60)
        print("Analyze syllabus with video search and terminal display:")
        print("  python syllabo_enhanced.py analyze --file syllabus.pdf --search-videos --print-results")
        print()
        print("Analyze and save results in HTML format:")
        print("  python syllabo_enhanced.py analyze --text 'Week 1: AI...' --search-videos --save --export-format html")
        print()
        print("Search videos for specific topic:")
        print("  python syllabo_enhanced.py search --topic 'Machine Learning' --max-videos 10 --save")
        print()
        print("View search history:")
        print("  python syllabo_enhanced.py history --limit 10")
        print()
        print("Key Features:")
        print("  • --print-results: Show detailed results in terminal")
        print("  • --save: Save results to file")
        print("  • --export-format: Choose json, csv, markdown, or html")
        print("  • --max-videos: Control number of videos per topic")
        print()

def main():
    parser = argparse.ArgumentParser(description='Syllabo Enhanced - AI-Powered YouTube Video Finder')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze syllabus and extract topics')
    analyze_parser.add_argument('--file', '-f', help='Syllabus file path (PDF or text)')
    analyze_parser.add_argument('--text', '-t', help='Syllabus text directly')
    analyze_parser.add_argument('--search-videos', action='store_true', help='Also search for videos')
    analyze_parser.add_argument('--max-videos', type=int, default=5, help='Max videos per topic')
    analyze_parser.add_argument('--print-results', action='store_true', help='Print detailed results in terminal')
    analyze_parser.add_argument('--save', action='store_true', help='Save results to file')
    analyze_parser.add_argument('--export-format', choices=['json', 'csv', 'markdown', 'html'], 
                              default='json', help='Export format for saved results')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search videos for a specific topic')
    search_parser.add_argument('--topic', required=True, help='Topic to search for')
    search_parser.add_argument('--max-videos', type=int, default=10, help='Maximum videos to find')
    search_parser.add_argument('--save', action='store_true', help='Save results to file')
    search_parser.add_argument('--export-format', choices=['json', 'csv', 'markdown', 'html'], 
                              default='json', help='Export format for saved results')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show recent syllabi and searches')
    history_parser.add_argument('--limit', type=int, default=10, help='Number of items to show')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export results in various formats')
    export_parser.add_argument('--format', choices=['csv', 'json', 'markdown', 'html'], 
                              default='json', help='Export format')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    if not youtube_api_key or youtube_api_key == "your_actual_api_key_here":
        print("Note: No valid YouTube API key found. Using mock data for demonstration.")
        print("To use real YouTube data, add a valid YOUTUBE_API_KEY to your .env file")
        print()
    else:
        print("YouTube API key found. Will attempt to use real data.")
        print()
    
    # Run the CLI
    cli = EnhancedSyllaboCLI()
    asyncio.run(cli.run(args))

if __name__ == "__main__":
    main()