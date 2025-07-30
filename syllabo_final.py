#!/usr/bin/env python3

import os
import sys
import json
import asyncio
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_client import AIClient
from src.youtube_client import YouTubeClient
from src.notes_generator import NotesGenerator

def print_banner():
    print("=" * 60)
    print("                    SYLLABO")
    print("         YouTube Video Finder for Students")
    print("              (Real Data - No API Required)")
    print("=" * 60)

def extract_topics(text):
    """Extract topics from syllabus text"""
    lines = text.split('\n')
    topics = []
    current_topic = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Look for topic indicators
        if any(keyword in line.lower() for keyword in ['week', 'chapter', 'unit', 'topic', 'lesson', 'module']):
            if current_topic:
                topics.append(current_topic)
            current_topic = {"name": line, "subtopics": []}
        elif current_topic and line.startswith('-'):
            current_topic["subtopics"].append(line[1:].strip())
        elif len(line.split()) <= 6 and not current_topic:
            # Treat short lines as topics if no current topic
            topics.append({"name": line, "subtopics": []})
    
    if current_topic:
        topics.append(current_topic)
    
    # If no structured topics found, create from each meaningful line
    if not topics:
        for line in lines:
            line = line.strip()
            if line and len(line) > 3:
                topics.append({"name": line, "subtopics": []})
    
    return topics[:5]  # Limit to 5 topics for demo

async def process_single_topic(topic_name, youtube_client, notes_generator):
    """Process one topic completely"""
    print(f"\nProcessing: {topic_name}")
    print("-" * 50)
    
    try:
        # Search for videos
        print("Searching YouTube for educational videos...")
        videos = await youtube_client.search_videos(f"{topic_name} tutorial explanation", max_results=3)
        
        if not videos:
            print("No videos found for this topic")
            return None
        
        print(f"Found {len(videos)} videos")
        
        # Show videos found
        print("\nVideos found:")
        for i, video in enumerate(videos, 1):
            print(f"{i}. {video['title']}")
            print(f"   Channel: {video['channel']}")
            print(f"   Duration: {video['duration']}")
            print(f"   Views: {video.get('view_count', 0):,}")
            print(f"   URL: https://youtube.com/watch?v={video['id']}")
        
        # Generate study materials for the best video
        print("\nGenerating AI study materials...")
        top_video = videos[0]
        
        # Try to get transcript
        transcript = youtube_client.get_transcript(top_video['id'])
        if transcript:
            print("Video transcript found - generating detailed materials")
        else:
            print("No transcript available - using video metadata")
        
        # Generate study materials
        study_materials = await notes_generator.generate_study_notes(
            topic_name, top_video, transcript
        )
        
        # Display study materials
        print(f"\nSTUDY MATERIALS FOR: {topic_name}")
        print("=" * 50)
        
        if study_materials.get('notes'):
            print("\nSTUDY NOTES:")
            for i, note in enumerate(study_materials['notes'], 1):
                print(f"{i}. {note}")
        
        if study_materials.get('questions'):
            print("\nPRACTICE QUESTIONS:")
            for i, question in enumerate(study_materials['questions'], 1):
                print(f"{i}. {question}")
        
        if study_materials.get('key_concepts'):
            print("\nKEY CONCEPTS:")
            for concept in study_materials['key_concepts']:
                print(f"• {concept}")
        
        return {
            'topic': topic_name,
            'videos': videos,
            'study_materials': study_materials
        }
        
    except Exception as e:
        print(f"Error processing {topic_name}: {e}")
        return None

def save_study_guide(results, filename=None):
    """Save complete study guide to JSON"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"study_guide_{timestamp}.json"
    
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "total_topics": len(results),
        "topics": {}
    }
    
    for result in results:
        if result:
            topic_name = result['topic']
            export_data["topics"][topic_name] = {
                "videos": [
                    {
                        "title": v['title'],
                        "channel": v['channel'],
                        "url": f"https://youtube.com/watch?v={v['id']}",
                        "duration": v['duration'],
                        "view_count": v.get('view_count', 0)
                    }
                    for v in result['videos']
                ],
                "study_materials": result['study_materials']
            }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return filename

async def main():
    print_banner()
    
    print("\nWelcome! This app finds real YouTube videos and generates study materials.")
    print("No API keys required - everything works through web scraping and AI.")
    print()
    
    # Get syllabus input
    print("Enter your syllabus content below.")
    print("You can paste multiple lines. Type 'END' when finished.")
    print("Or type 'demo' to use sample content.")
    print("-" * 40)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            elif line.strip().lower() == 'demo':
                lines = [
                    "Machine Learning Fundamentals",
                    "K-means Clustering Algorithm", 
                    "Neural Networks Introduction",
                    "Data Preprocessing Techniques"
                ]
                print("Using demo content...")
                break
            else:
                lines.append(line)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return
    
    if not lines:
        print("No content provided. Exiting.")
        return
    
    # Extract topics
    text = '\n'.join(lines)
    topics = extract_topics(text)
    
    if not topics:
        print("Could not extract topics from the content. Please try again.")
        return
    
    print(f"\nExtracted {len(topics)} topics:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic['name']}")
    
    print(f"\nInitializing YouTube scraper and AI systems...")
    
    # Initialize clients
    youtube_client = YouTubeClient()
    ai_client = AIClient()
    notes_generator = NotesGenerator(ai_client)
    
    print("Ready! Processing topics...")
    
    # Process each topic
    all_results = []
    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*60}")
        print(f"TOPIC {i}/{len(topics)}")
        print(f"{'='*60}")
        
        result = await process_single_topic(topic['name'], youtube_client, notes_generator)
        if result:
            all_results.append(result)
    
    # Save results
    if all_results:
        filename = save_study_guide(all_results)
        
        print(f"\n{'='*60}")
        print("COMPLETE STUDY GUIDE GENERATED!")
        print(f"{'='*60}")
        print(f"Successfully processed {len(all_results)} topics")
        print(f"Study guide saved to: {filename}")
        print()
        print("Your study guide includes:")
        print("- Real YouTube videos (scraped without API)")
        print("- AI-generated study notes")
        print("- Practice questions for each topic")
        print("- Key concepts to remember")
        print("- Complete video information and links")
        print()
        print("Open the JSON file to see all materials or use them for studying!")
    else:
        print("\nNo topics were successfully processed. Please check your internet connection.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check your internet connection and try again.")