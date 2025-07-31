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

from src.spaced_repetition import SpacedRepetitionEngine
from src.notification_system import NotificationSystem

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress

class EnhancedSyllaboCLI: 
    def __init__(self):
        load_dotenv()
        self.logger = SyllaboLogger("cli")
        self.db = SyllaboDatabase()
        self.ai_client = AIClient()
        self.youtube_client = YouTubeClient()
        self.video_analyzer = VideoAnalyzer(self.ai_client)
        self.syllabus_parser = SyllabusParser()

        self.console = Console()
        self.spaced_repetition = SpacedRepetitionEngine()
        self.notifications = NotificationSystem()
    
    def print_banner(self):
        self.console.print(Panel.fit("[bold cyan]SYLLABO ENHANCED[/bold cyan]", subtitle="AI-Powered YouTube Video Finder"))
    
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
        elif args.command == 'review':
            self.handle_review_commands(args)
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
        
        print(f"\nTopic Analysis Summary for: {syllabus_title}")
        print(f"Found {len(topics)} topics")
        if missing_topics:
            print(f"Potentially missed topics: {', '.join(missing_topics[:3])}")
        
        if not topics:
            print("No clear topics found. Try refining your syllabus content.")
            return
        
        syllabus_id = self.db.save_syllabus(syllabus_title, syllabus_content)
        topic_ids = self.db.save_topics(syllabus_id, topics)
        
        if args.search_videos:
            print("Searching for videos...")
            topic_results = await self.search_for_topics_enhanced(topics, topic_ids, args.max_videos)
            
            if args.print_results:
                self.print_video_results(topic_results, args.max_videos)
            
            total_videos = sum(len(videos) for videos in topic_results.values())
            processing_time = time.time() - start_time
            print(f"\nCompleted analysis: {len(topics)} topics, {total_videos} videos found in {processing_time:.1f}s")
            
            if args.save or args.export_format:
                await self.save_comprehensive_results(topic_results, syllabus_title, args.export_format or 'json')
            
            # Add topics to spaced repetition if requested
            if args.add_to_review:
                self.add_topics_to_spaced_repetition(topics)
        else:
            print(f"\nTo search for videos, add --search-videos flag")
            print(f"To see results in terminal, add --print-results flag")
            
            # Still offer to add topics to spaced repetition
            if args.add_to_review:
                self.add_topics_to_spaced_repetition(topics)
    
    async def search_videos(self, args):
        """Search for videos and playlists for a specific topic"""
        if not args.topic:
            print("Error: Please provide a topic to search for")
            return
        
        start_time = time.time()
        print(f"Searching videos and playlists for: {args.topic}")
        
        enhanced_query = f"{args.topic} tutorial explained"
        videos = await self.youtube_client.search_videos(enhanced_query, args.max_videos)
        playlists = await self.youtube_client.search_playlists(enhanced_query, max(2, args.max_videos // 3))
        
        if not videos and not playlists:
            print("No videos or playlists found")
            print("Try a different topic name or check your internet connection")
            return
        
        print(f"Found {len(videos)} videos and {len(playlists)} playlists, analyzing with AI...")
        
        analysis_result = await self.video_analyzer.analyze_videos_and_playlists(videos, playlists, args.topic)
        
        # Extract all resources from the analysis result
        all_resources = []
        
        # Add primary resource
        if analysis_result.get('primary_resource'):
            all_resources.append(analysis_result['primary_resource'])
        
        # Add supplementary videos
        all_resources.extend(analysis_result.get('supplementary_videos', []))
        
        # Add supplementary playlists
        all_resources.extend(analysis_result.get('supplementary_playlists', []))
        
        quality_resources = [r for r in all_resources if r.get('relevance_score', 0) >= 3.0]
        
        if not quality_resources:
            print("No high-quality resources found for this topic")
            print("Try refining your topic or search for a broader term")
            return
        
        topic_results = {args.topic: quality_resources}
        
        self.print_video_results(topic_results, min(args.max_videos, 10))
        
        processing_time = time.time() - start_time
        print(f"\nCompleted search: 1 topic, {len(quality_resources)} videos found in {processing_time:.1f}s")
        
        if args.save:
            await self.save_video_results(quality_resources, args.topic, args.export_format or 'json')
    
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
        """Search for videos and playlists across all topics"""
        all_results = {}

        with Progress(console=self.console) as progress:
            task = progress.add_task("[cyan]Searching for videos and playlists...", total=len(topics))

            for i, (topic, topic_id) in enumerate(zip(topics, topic_ids)):
                topic_name = topic['name']
                progress.update(task, advance=1, description=f"Searching for: {topic_name}")

                try:
                    enhanced_query = self._enhance_search_query(topic_name, topic.get('subtopics', []))
                    
                    # Search both videos and playlists
                    videos = await self.youtube_client.search_videos(enhanced_query, max_videos)
                    playlists = await self.youtube_client.search_playlists(enhanced_query, max(2, max_videos // 3))

                    if videos or playlists:
                        # Use the new comprehensive analysis method
                        analysis_result = await self.video_analyzer.analyze_videos_and_playlists(videos, playlists, topic_name)
                        
                        # Extract all resources from the analysis result
                        all_resources = []
                        
                        # Add primary resource
                        if analysis_result.get('primary_resource'):
                            all_resources.append(analysis_result['primary_resource'])
                        
                        # Add supplementary videos
                        all_resources.extend(analysis_result.get('supplementary_videos', []))
                        
                        # Add supplementary playlists
                        all_resources.extend(analysis_result.get('supplementary_playlists', []))
                        
                        # Filter for quality
                        quality_resources = [r for r in all_resources if r.get('relevance_score', 0) >= 4.0]

                        # Save to database
                        for resource in quality_resources:
                            self.db.save_video(resource)  # This method can handle both videos and playlists
                            self.db.link_topic_video(topic_id, resource['id'], resource['relevance_score'])

                        all_results[topic_name] = quality_resources
                    else:
                        all_results[topic_name] = []

                except Exception as e:
                    self.logger.error(f"Failed to search resources for {topic_name}: {e}")
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
        self.console.print("[bold]Recent Syllabi[/bold]")
        recent_syllabi = self.db.get_recent_syllabi(args.limit)

        if not recent_syllabi:
            self.console.print("No syllabi found in database")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Title")
        table.add_column("Created At", justify="right")

        for syllabus in recent_syllabi:
            table.add_row(
                str(syllabus['id']),
                syllabus['title'],
                syllabus['created_at']
            )
        self.console.print(table)
    
    async def export_results(self, args):
        """Export results for a given syllabus ID"""
        if not args.syllabus_id:
            print("Error: Please provide a syllabus ID to export.")
            self.show_history(argparse.Namespace(limit=5))
            return

        print(f"Exporting results for syllabus ID: {args.syllabus_id}")
        syllabus = self.db.get_syllabus_by_id(args.syllabus_id)
        if not syllabus:
            print(f"Error: Syllabus with ID {args.syllabus_id} not found.")
            return

        topics = self.db.get_topics_by_syllabus_id(args.syllabus_id)
        if not topics:
            print(f"No topics found for syllabus: {syllabus['title']}")
            return

        topic_results = {}
        for topic in topics:
            videos = self.db.get_topic_videos(topic['id'])
            if videos:
                topic_results[topic['name']] = videos

        if not topic_results:
            print("No video results found for this syllabus.")
            return

        await self.save_comprehensive_results(topic_results, syllabus['title'], args.format)
    
    def print_video_results(self, topic_results: Dict[str, List[Dict]], max_videos: int):
        """Print video results in a clean format"""
        print("\nTop Video Recommendations:")
        print("=" * 60)
        
        for topic_name, videos in topic_results.items():
            if not videos:
                continue
                
            print(f"\nTopic: {topic_name}")
            print("-" * 50)
            
            for i, video in enumerate(videos[:max_videos], 1):
                title = video.get('title', 'Unknown Title')[:60]
                channel = video.get('channel', 'Unknown Channel')
                score = video.get('relevance_score', 0)
                url = f"https://youtube.com/watch?v={video.get('id', '')}"
                
                print(f"{i}. {title}")
                print(f"   Channel: {channel}")
                print(f"   Score: {score:.1f}/10")
                print(f"   URL: {url}")
                print()
    
    def add_topics_to_spaced_repetition(self, topics: List[Dict]):
        """Add extracted topics to spaced repetition system"""
        added_count = 0
        
        for topic in topics:
            topic_name = topic['name']
            description = topic.get('description', '')
            
            if self.spaced_repetition.add_topic(topic_name, description):
                added_count += 1
                print(f"Added to review schedule: {topic_name}")
            else:
                print(f"Already in review schedule: {topic_name}")
        
        if added_count > 0:
            print(f"\nAdded {added_count} topics to spaced repetition schedule")
            print("Use 'python syllabo_enhanced.py review list' to see your review schedule")
        else:
            print("\nAll topics were already in your review schedule")
    
    def handle_review_commands(self, args):
        """Handle all review-related commands"""
        if args.review_action == 'add':
            self.add_review_topic(args)
        elif args.review_action == 'list':
            self.list_review_topics(args)
        elif args.review_action == 'due':
            self.show_due_reviews(args)
        elif args.review_action == 'mark':
            self.mark_topic_review(args)
        elif args.review_action == 'stats':
            self.show_review_stats(args)
        elif args.review_action == 'remove':
            self.remove_review_topic(args)
        else:
            self.show_review_help()
    
    def add_review_topic(self, args):
        """Add a topic to spaced repetition manually"""
        if not args.topic:
            print("Error: Please provide a topic name with --topic")
            return
        
        description = args.description or ""
        
        if self.spaced_repetition.add_topic(args.topic, description):
            print(f"Added '{args.topic}' to review schedule")
            print(f"First review scheduled for tomorrow")
        else:
            print(f"Topic '{args.topic}' is already in your review schedule")
    
    def list_review_topics(self, args):
        """List all topics in spaced repetition"""
        topics = self.spaced_repetition.get_all_topics()
        
        if not topics:
            print("No topics in your review schedule")
            print("Add topics with: python syllabo_enhanced.py review add --topic 'Topic Name'")
            return
        
        self.console.print("[bold]Your Review Schedule[/bold]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Topic", style="cyan", width=30)
        table.add_column("Mastery", justify="center", width=12)
        table.add_column("Success Rate", justify="center", width=12)
        table.add_column("Next Review", justify="center", width=12)
        table.add_column("Interval", justify="center", width=10)
        
        for topic in sorted(topics, key=lambda x: x['days_until_review']):
            mastery_color = {
                'Learning': 'red',
                'Beginner': 'yellow',
                'Intermediate': 'blue',
                'Advanced': 'green',
                'Mastered': 'bright_green'
            }.get(topic['mastery_level'], 'white')
            
            days_until = topic['days_until_review']
            if days_until <= 0:
                next_review_text = f"[red]Due now[/red]"
            elif days_until == 1:
                next_review_text = "Tomorrow"
            else:
                next_review_text = f"{days_until} days"
            
            table.add_row(
                topic['topic_name'][:28] + "..." if len(topic['topic_name']) > 28 else topic['topic_name'],
                f"[{mastery_color}]{topic['mastery_level']}[/{mastery_color}]",
                f"{topic['success_rate']}%",
                next_review_text,
                f"{topic['current_interval']}d"
            )
        
        self.console.print(table)
        
        # Show summary
        summary = self.spaced_repetition.get_study_summary()
        print(f"\nSummary: {summary['total_topics']} topics, {summary['due_now']} due now, {summary['mastered_topics']} mastered")
    
    def show_due_reviews(self, args):
        """Show topics that are due for review"""
        due_topics = self.spaced_repetition.get_due_topics()
        
        if not due_topics:
            print("No topics are due for review right now")
            
            # Show upcoming reviews
            upcoming = self.spaced_repetition.get_upcoming_topics(3)
            if upcoming:
                print("\nUpcoming reviews in the next 3 days:")
                for item in upcoming[:5]:
                    days_until = (datetime.fromisoformat(item.next_review) - datetime.now()).days
                    print(f"  • {item.topic_name} - in {days_until} day{'s' if days_until != 1 else ''}")
            return
        
        print(f"You have {len(due_topics)} topic{'s' if len(due_topics) != 1 else ''} due for review:")
        print()
        
        for i, item in enumerate(due_topics, 1):
            overdue_days = (datetime.now() - datetime.fromisoformat(item.next_review)).days
            overdue_text = f" (overdue by {overdue_days} day{'s' if overdue_days != 1 else ''})" if overdue_days > 0 else ""
            
            print(f"{i}. {item.topic_name}{overdue_text}")
            if item.description:
                print(f"   Description: {item.description}")
            print(f"   Success rate: {(item.total_successes/item.total_reviews*100):.1f}% ({item.total_successes}/{item.total_reviews})")
            print()
        
        print("To mark a review, use:")
        print("  python syllabo_enhanced.py review mark --topic 'Topic Name' --success")
        print("  python syllabo_enhanced.py review mark --topic 'Topic Name' --failure")
        
        # Send notification if enabled
        if args.notify:
            self.notifications.notify_due_reviews(len(due_topics))
    
    def mark_topic_review(self, args):
        """Mark a topic as reviewed"""
        if not args.topic:
            print("Error: Please provide a topic name with --topic")
            return
        
        if not args.success and not args.failure:
            print("Error: Please specify --success or --failure")
            return
        
        success = args.success
        
        if self.spaced_repetition.mark_review(args.topic, success):
            result_text = "successful" if success else "failed"
            print(f"Marked '{args.topic}' as {result_text} review")
            
            # Show updated stats
            stats = self.spaced_repetition.get_topic_stats(args.topic)
            if stats:
                print(f"Next review in {stats['current_interval']} days ({stats['next_review_date']})")
                print(f"Success rate: {stats['success_rate']}% - {stats['mastery_level']}")
        else:
            print(f"Topic '{args.topic}' not found in review schedule")
    
    def show_review_stats(self, args):
        """Show detailed review statistics"""
        if args.topic:
            # Show stats for specific topic
            stats = self.spaced_repetition.get_topic_stats(args.topic)
            if not stats:
                print(f"Topic '{args.topic}' not found in review schedule")
                return
            
            print(f"Statistics for: {stats['topic_name']}")
            print("-" * 50)
            print(f"Description: {stats['description'] or 'No description'}")
            print(f"Mastery Level: {stats['mastery_level']}")
            print(f"Success Rate: {stats['success_rate']}%")
            print(f"Success Streak: {stats['success_streak']}")
            print(f"Total Reviews: {stats['total_reviews']}")
            print(f"Current Interval: {stats['current_interval']} days")
            print(f"Next Review: {stats['next_review_date']} ({stats['days_until_review']} days)")
        else:
            # Show overall stats
            summary = self.spaced_repetition.get_study_summary()
            
            print("Overall Review Statistics")
            print("-" * 50)
            print(f"Total Topics: {summary['total_topics']}")
            print(f"Due Now: {summary['due_now']}")
            print(f"Due Today: {summary['due_today']}")
            print(f"Mastered Topics: {summary['mastered_topics']}")
            print(f"Average Success Rate: {summary['average_success_rate']}%")
            
            if summary['total_topics'] > 0:
                mastery_rate = (summary['mastered_topics'] / summary['total_topics']) * 100
                print(f"Mastery Rate: {mastery_rate:.1f}%")
    
    def remove_review_topic(self, args):
        """Remove a topic from spaced repetition"""
        if not args.topic:
            print("Error: Please provide a topic name with --topic")
            return
        
        if self.spaced_repetition.remove_topic(args.topic):
            print(f"Removed '{args.topic}' from review schedule")
        else:
            print(f"Topic '{args.topic}' not found in review schedule")
    
    def show_review_help(self):
        """Show help for review commands"""
        print("\nSpaced Repetition Review Commands:")
        print("-" * 50)
        print("Add topic to review schedule:")
        print("  python syllabo_enhanced.py review add --topic 'Neural Networks' --description 'Forward/backward pass'")
        print()
        print("List all topics in review schedule:")
        print("  python syllabo_enhanced.py review list")
        print()
        print("Show topics due for review:")
        print("  python syllabo_enhanced.py review due --notify")
        print()
        print("Mark a topic as reviewed:")
        print("  python syllabo_enhanced.py review mark --topic 'Neural Networks' --success")
        print("  python syllabo_enhanced.py review mark --topic 'Neural Networks' --failure")
        print()
        print("Show review statistics:")
        print("  python syllabo_enhanced.py review stats")
        print("  python syllabo_enhanced.py review stats --topic 'Neural Networks'")
        print()
        print("Remove topic from review schedule:")
        print("  python syllabo_enhanced.py review remove --topic 'Neural Networks'")
        print()
    
    def show_help(self):
        """Show help information"""
        print("\nSyllabo Enhanced - Usage Examples:")
        print("-" * 60)
        print("Analyze syllabus with video search and add to review schedule:")
        print("  python syllabo_enhanced.py analyze --file syllabus.pdf --search-videos --print-results --add-to-review")
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
        print("Spaced repetition review:")
        print("  python syllabo_enhanced.py review due")
        print("  python syllabo_enhanced.py review list")
        print()
        print("Key Features:")
        print("  • --print-results: Show detailed results in terminal")
        print("  • --save: Save results to file")
        print("  • --export-format: Choose json, csv, markdown, or html")
        print("  • --max-videos: Control number of videos per topic")
        print("  • --add-to-review: Add topics to spaced repetition schedule")
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
    analyze_parser.add_argument('--add-to-review', action='store_true', help='Add topics to spaced repetition schedule')
    
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
    export_parser.add_argument('--syllabus-id', type=int, help='Syllabus ID to export')
    
    # Review command (spaced repetition)
    review_parser = subparsers.add_parser('review', help='Spaced repetition review system')
    review_subparsers = review_parser.add_subparsers(dest='review_action', help='Review actions')
    
    # Review add
    add_review_parser = review_subparsers.add_parser('add', help='Add topic to review schedule')
    add_review_parser.add_argument('--topic', required=True, help='Topic name to add')
    add_review_parser.add_argument('--description', '-d', help='Topic description')
    
    # Review list
    list_review_parser = review_subparsers.add_parser('list', help='List all topics in review schedule')
    
    # Review due
    due_review_parser = review_subparsers.add_parser('due', help='Show topics due for review')
    due_review_parser.add_argument('--notify', action='store_true', help='Send desktop notification')
    
    # Review mark
    mark_review_parser = review_subparsers.add_parser('mark', help='Mark topic as reviewed')
    mark_review_parser.add_argument('--topic', required=True, help='Topic name to mark')
    mark_group = mark_review_parser.add_mutually_exclusive_group(required=True)
    mark_group.add_argument('--success', action='store_true', help='Mark review as successful')
    mark_group.add_argument('--failure', action='store_true', help='Mark review as failed')
    
    # Review stats
    stats_review_parser = review_subparsers.add_parser('stats', help='Show review statistics')
    stats_review_parser.add_argument('--topic', help='Show stats for specific topic')
    
    # Review remove
    remove_review_parser = review_subparsers.add_parser('remove', help='Remove topic from review schedule')
    remove_review_parser.add_argument('--topic', required=True, help='Topic name to remove')
    
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