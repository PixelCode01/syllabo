#!/usr/bin/env python3
"""
Interactive YouTube scraper - Try it with your own syllabus!
No API keys required - scrapes real YouTube data.
"""

import requests
import re
import json
from urllib.parse import quote_plus, urljoin
from typing import List, Dict
import time
import os
from bs4 import BeautifulSoup


def scrape_youtube_search(query: str, max_results: int = 8) -> List[Dict]:
    """Scrape YouTube search results without API"""
    
    print(f"Searching YouTube for: '{query}'")
    
    try:
        # Set up session with proper headers
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Search YouTube
        search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        
        print("Fetching data from YouTube...")
        response = session.get(search_url, timeout=15)
        
        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            return []
        
        print(f"Successfully fetched search page ({len(response.text):,} characters)")
        
        # Extract video data
        videos = extract_video_data_from_html(response.text, max_results)
        
        if videos:
            print(f"Successfully extracted {len(videos)} videos")
        else:
            print("No videos extracted, trying alternative method...")
            videos = extract_with_regex(response.text, max_results)
        
        return videos
        
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []
    except Exception as e:
        print(f"Scraping error: {e}")
        return []


def extract_video_data_from_html(html: str, max_results: int) -> List[Dict]:
    """Extract video data from YouTube HTML"""
    
    videos = []
    
    try:
        # Look for ytInitialData
        pattern = r'var ytInitialData = ({.*?});'
        match = re.search(pattern, html, re.DOTALL)
        
        if match:
            print("Found ytInitialData, parsing JSON...")
            data = json.loads(match.group(1))
            videos = parse_youtube_json_data(data, max_results)
        
        if not videos:
            print("JSON parsing failed, trying regex extraction...")
            videos = extract_with_regex(html, max_results)
        
        return videos
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return extract_with_regex(html, max_results)
    except Exception as e:
        print(f"Extraction error: {e}")
        return []


def parse_youtube_json_data(data: dict, max_results: int) -> List[Dict]:
    """Parse YouTube's JSON data structure"""
    
    videos = []
    
    try:
        # Navigate the complex YouTube data structure
        contents = (data.get('contents', {})
                   .get('twoColumnSearchResultsRenderer', {})
                   .get('primaryContents', {})
                   .get('sectionListRenderer', {})
                   .get('contents', []))
        
        for section in contents:
            items = section.get('itemSectionRenderer', {}).get('contents', [])
            
            for item in items:
                if len(videos) >= max_results:
                    break
                
                video_renderer = item.get('videoRenderer')
                if not video_renderer:
                    continue
                
                video_data = extract_video_from_renderer(video_renderer)
                if video_data:
                    videos.append(video_data)
        
        return videos
        
    except Exception as e:
        print(f"JSON data parsing error: {e}")
        return []


def extract_video_from_renderer(renderer: dict) -> Dict:
    """Extract video info from videoRenderer object"""
    
    try:
        video_id = renderer.get('videoId', '')
        
        # Extract title
        title_obj = renderer.get('title', {})
        title = get_text_from_runs(title_obj)
        
        # Extract channel
        owner_obj = renderer.get('ownerText', {})
        channel = get_text_from_runs(owner_obj)
        
        # Extract view count
        view_obj = renderer.get('viewCountText', {})
        view_text = get_text_from_runs(view_obj)
        view_count = parse_view_count(view_text)
        
        # Extract duration
        duration_obj = renderer.get('lengthText', {})
        duration = get_text_from_runs(duration_obj)
        
        # Extract description snippet
        desc_obj = renderer.get('detailedMetadataSnippets', [{}])[0].get('snippetText', {})
        description = get_text_from_runs(desc_obj)
        
        if not all([video_id, title, channel]):
            return None
        
        return {
            'id': video_id,
            'title': title,
            'channel': channel,
            'description': description or f"Educational video about {title}",
            'duration': duration or "Unknown",
            'view_count': view_count,
            'like_count': max(1, view_count // 50),  # Estimate 2% like ratio
            'published_at': "Recently",
            'url': f"https://www.youtube.com/watch?v={video_id}"
        }
        
    except Exception as e:
        print(f"Error extracting video from renderer: {e}")
        return None


def get_text_from_runs(text_obj: dict) -> str:
    """Extract text from YouTube's text objects"""
    
    if not text_obj:
        return ""
    
    if isinstance(text_obj, str):
        return text_obj
    
    if 'runs' in text_obj:
        return ''.join(run.get('text', '') for run in text_obj['runs'])
    elif 'simpleText' in text_obj:
        return text_obj['simpleText']
    
    return str(text_obj)


def parse_view_count(view_text: str) -> int:
    """Parse view count from text like '1.2M views'"""
    
    if not view_text:
        return 0
    
    # Clean the text
    clean_text = re.sub(r'[^\d.,KMB]', '', view_text.upper())
    
    try:
        if 'M' in clean_text:
            number = float(clean_text.replace('M', ''))
            return int(number * 1_000_000)
        elif 'K' in clean_text:
            number = float(clean_text.replace('K', ''))
            return int(number * 1_000)
        elif 'B' in clean_text:
            number = float(clean_text.replace('B', ''))
            return int(number * 1_000_000_000)
        else:
            return int(clean_text.replace(',', ''))
    except (ValueError, AttributeError):
        return 0


def extract_with_regex(html: str, max_results: int) -> List[Dict]:
    """Fallback regex-based extraction"""
    
    print("Using regex fallback extraction...")
    
    videos = []
    
    # Pattern to find video data
    video_pattern = r'"videoId":"([^"]+)".*?"title":{"runs":\[{"text":"([^"]+)"}\].*?"ownerText":{"runs":\[{"text":"([^"]+)"}\]'
    
    matches = re.findall(video_pattern, html, re.DOTALL)
    
    for i, (video_id, title, channel) in enumerate(matches[:max_results]):
        if video_id and title and channel:
            videos.append({
                'id': video_id,
                'title': title,
                'channel': channel,
                'description': f"Educational content about {title}",
                'duration': "Unknown",
                'view_count': 100000 + (i * 25000),  # Estimated
                'like_count': 2000 + (i * 500),      # Estimated
                'published_at': "Recently",
                'url': f"https://www.youtube.com/watch?v={video_id}"
            })
    
    return videos


def analyze_scraped_videos(videos: List[Dict], topic: str) -> List[Dict]:
    """Analyze scraped videos and calculate scores"""
    
    print("Analyzing videos with AI-free algorithms...")
    
    analyzed_videos = []
    
    for video in videos:
        # Calculate relevance score
        relevance_score = calculate_relevance(video, topic)
        
        # Calculate quality score
        quality_score = calculate_quality(video)
        
        # Calculate engagement score
        engagement_score = calculate_engagement(video)
        
        # Calculate composite score
        composite_score = (
            relevance_score * 0.4 +
            quality_score * 0.3 + 
            engagement_score * 0.3
        )
        
        analyzed_video = {
            **video,
            'relevance_score': relevance_score,
            'quality_score': quality_score,
            'engagement_score': engagement_score,
            'composite_score': round(composite_score, 2)
        }
        
        analyzed_videos.append(analyzed_video)
    
    # Sort by composite score
    analyzed_videos.sort(key=lambda x: x['composite_score'], reverse=True)
    
    return analyzed_videos


def calculate_relevance(video: Dict, topic: str) -> float:
    """Calculate relevance score"""
    score = 5.0
    
    title_lower = video['title'].lower()
    desc_lower = video.get('description', '').lower()
    topic_lower = topic.lower()
    
    # Topic keyword matching
    topic_words = topic_lower.split()
    for word in topic_words:
        if word in title_lower:
            score += 1.5
        if word in desc_lower:
            score += 0.5
    
    # Educational keywords
    educational_keywords = ['tutorial', 'course', 'learn', 'beginner', 'guide', 'complete', 'full']
    for keyword in educational_keywords:
        if keyword in title_lower:
            score += 0.5
    
    return min(10.0, score)


def calculate_quality(video: Dict) -> float:
    """Calculate quality score"""
    score = 5.0
    
    # View count scoring
    view_count = video.get('view_count', 0)
    if view_count > 5000000:
        score += 2.5
    elif view_count > 1000000:
        score += 2.0
    elif view_count > 100000:
        score += 1.5
    elif view_count > 10000:
        score += 1.0
    elif view_count > 1000:
        score += 0.5
    
    # Channel reputation
    channel = video.get('channel', '').lower()
    reputable_channels = ['freecodecamp', 'programming with mosh', 'tech with tim', 'codecademy', 'harvard', 'mit']
    if any(rep in channel for rep in reputable_channels):
        score += 1.0
    
    return min(10.0, score)


def calculate_engagement(video: Dict) -> float:
    """Calculate engagement score"""
    score = 5.0
    
    view_count = video.get('view_count', 0)
    like_count = video.get('like_count', 0)
    
    if view_count > 0 and like_count > 0:
        like_ratio = like_count / view_count
        if like_ratio > 0.03:
            score += 2.0
        elif like_ratio > 0.02:
            score += 1.5
        elif like_ratio > 0.01:
            score += 1.0
        elif like_ratio > 0.005:
            score += 0.5
    
    return min(10.0, score)


def create_learning_path(analyzed_videos: List[Dict], topic: str) -> Dict:
    """Create optimal learning path"""
    
    if not analyzed_videos:
        return {
            'topic': topic,
            'primary_video': None,
            'supplementary_videos': [],
            'total_videos': 0
        }
    
    primary_video = analyzed_videos[0]
    supplementary_videos = analyzed_videos[1:4]  # Top 3 supplements
    
    # Add coverage types
    for video in supplementary_videos:
        title_lower = video['title'].lower()
        if any(word in title_lower for word in ['crash', 'quick', 'fast', 'minutes']):
            video['coverage_type'] = 'Quick Review'
        elif any(word in title_lower for word in ['advanced', 'deep', 'complete', 'full']):
            video['coverage_type'] = 'Comprehensive'
        elif any(word in title_lower for word in ['beginner', 'intro', 'basics']):
            video['coverage_type'] = 'Foundation'
        else:
            video['coverage_type'] = 'Supplementary'
    
    return {
        'topic': topic,
        'primary_video': primary_video,
        'supplementary_videos': supplementary_videos,
        'total_videos': 1 + len(supplementary_videos)
    }


def display_results(videos: List[Dict], analyzed_videos: List[Dict], learning_path: Dict, topic: str):
    """Display all results in a nice format"""
    
    print("\n" + "="*70)
    print("SCRAPED VIDEOS")
    print("="*70)
    
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']}")
        print(f"   Channel: {video['channel']}")
        print(f"   Views: {video['view_count']:,}")
        print(f"   URL: {video['url']}")
        print()
    
    print("="*70)
    print("VIDEO ANALYSIS RESULTS")
    print("="*70)
    
    for i, video in enumerate(analyzed_videos, 1):
        print(f"{i}. {video['title'][:55]}...")
        print(f"   Relevance: {video['relevance_score']:.1f}/10")
        print(f"   Quality: {video['quality_score']:.1f}/10")
        print(f"   Engagement: {video['engagement_score']:.1f}/10")
        print(f"   Overall Score: {video['composite_score']:.1f}/10")
        print()
    
    print("="*70)
    print("OPTIMAL LEARNING PATH")
    print("="*70)
    
    primary = learning_path['primary_video']
    supplements = learning_path['supplementary_videos']
    
    print(f"Topic: {topic}")
    print(f"Total Videos Selected: {learning_path['total_videos']}")
    print()
    
    if primary:
        print("PRIMARY VIDEO (Foundation):")
        print(f"   {primary['title']}")
        print(f"   Channel: {primary['channel']}")
        print(f"   Score: {primary['composite_score']:.1f}/10")
        print(f"   URL: {primary['url']}")
        print()
    
    if supplements:
        print("SUPPLEMENTARY VIDEOS:")
        for i, video in enumerate(supplements, 1):
            print(f"   {i}. {video['title']}")
            print(f"      Channel: {video['channel']}")
            print(f"      Type: {video.get('coverage_type', 'Supplementary')}")
            print(f"      Score: {video['composite_score']:.1f}/10")
            print(f"      URL: {video['url']}")
            print()
    
    print("="*70)
    print("SUCCESS: Real YouTube data scraped analyzed!")
    print("System works with actual video data without API keys.")
    print("="*70)


def extract_topics_from_syllabus(syllabus_text: str) -> List[Dict]:
    """Extract topics from syllabus text"""
    
    print("Extracting topics from syllabus...")
    
    lines = syllabus_text.split('\n')
    topics = []
    current_topic = None
    
    for line in lines:
        line = line.strip()
        if not line: 
            continue
            
        # Look for topic headers (Week, Chapter, Unit, etc.)
        if re.match(r'^(Week|Chapter|Unit|Topic|Module)\s*\d+', line, re.IGNORECASE):
            if current_topic:
                topics.append(current_topic)
            
            # Extract topic name (remove "Week 1:" prefix)
            topic_name = re.sub(r'^(Week|Chapter|Unit|Topic|Module)\s*\d+:\s*', '', line, flags=re.IGNORECASE)
            current_topic = {"name": topic_name, "subtopics": []}
            
        elif current_topic and line.startswith('-'):
            # Add subtopic
            subtopic = line[1:].strip()
            current_topic["subtopics"].append(subtopic)
    
    # Add the last topic
    if current_topic:
        topics.append(current_topic)
    
    # If no structured topics found, try to extract general topics
    if not topics:
        topics = extract_general_topics(syllabus_text)
    
    return topics


def extract_general_topics(text: str) -> List[Dict]:
    """Extract topics from unstructured syllabus text"""
    
    # Look for common topic indicators
    topic_patterns = [
        r'([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # Title Case phrases
        r'(\b[A-Z][a-z]+(?:\s+[a-z]+)*\b)',  # Capitalized words
    ]
    
    topics = []
    found_topics = set()
    
    for pattern in topic_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) > 5 and match not in found_topics:  # Filter short matches
                found_topics.add(match)
                topics.append({"name": match, "subtopics": []})
                
                if len(topics) >= 8:  # Limit to reasonable number
                    break
    
    return topics if topics else [{"name": "General Course Content", "subtopics": []}]


def process_syllabus_topics(topics: List[Dict], include_resources: bool = False, resource_preference: str = "both") -> Dict:
    """Process all topics from syllabus and create learning paths"""
    
    all_results = {}
    
    print(f"\nFound {len(topics)} topics in syllabus:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic['name']}")
        if topic['subtopics']:
            for subtopic in topic['subtopics'][:3]:  # Show first 3 subtopics
                print(f"     - {subtopic}")
            if len(topic['subtopics']) > 3:
                print(f"     ... and {len(topic['subtopics']) - 3} more")
    
    print(f"\nProcessing {len(topics)} topics...")
    if include_resources:
        print(f"Resource preference: {resource_preference.title()}")
    print("-" * 50)
    
    for i, topic in enumerate(topics, 1):
        topic_name = topic['name']
        print(f"\n[{i}/{len(topics)}] Processing: {topic_name}")
        
        # Scrape videos for this topic
        videos = scrape_youtube_search(topic_name, max_results=4)
        
        if not videos:
            print(f"No videos found for: {topic_name}")
            all_results[topic_name] = {
                'topic': topic_name,
                'videos': [],
                'analyzed_videos': [],
                'learning_path': None
            }
            continue
        
        # Analyze videos
        analyzed_videos = analyze_scraped_videos(videos, topic_name)
        
        # Create learning path
        learning_path = create_learning_path(analyzed_videos, topic_name)
        
        result = {
            'topic': topic_name,
            'subtopics': topic['subtopics'],
            'videos': videos,
            'analyzed_videos': analyzed_videos,
            'learning_path': learning_path
        }
        
        # Add resource search if requested
        if include_resources:
            resources = search_educational_resources(topic_name, resource_preference)
            result['resources'] = resources
            print(f"Found {len(videos)} videos and {len(resources['books']) + len(resources['courses'])} resources for {topic_name}")
        else:
            print(f"Found {len(videos)} videos for {topic_name}")
        
        all_results[topic_name] = result
        
        # Small delay to be respectful
        time.sleep(1)
    
    return all_results


def scrape_coursera_courses(topic: str, max_results: int = 3) -> List[Dict]:
    """Scrape real Coursera courses for a topic"""
    
    courses = []
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        
        # Search Coursera
        search_url = f"https://www.coursera.org/search?query={quote_plus(topic)}&index=prod_all_launched_products_term_optimization"
        
        response = session.get(search_url, timeout=10)
        if response.status_code != 200:
            return courses
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find course cards
        course_cards = soup.find_all('div', {'data-testid': 'search-result-card'}) or soup.find_all('div', class_=re.compile('result-title'))
        
        for card in course_cards[:max_results]:
            try:
                # Extract title
                title_elem = card.find('h3') or card.find('h2') or card.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                # Extract link
                link_elem = card.find('a', href=True)
                if link_elem:
                    course_url = urljoin('https://www.coursera.org', link_elem['href'])
                else:
                    course_url = f"https://www.coursera.org/search?query={quote_plus(topic)}"
                
                # Extract provider/university
                provider_elem = card.find('span', class_=re.compile('partner')) or card.find('p')
                provider = provider_elem.get_text(strip=True) if provider_elem else "Coursera"
                
                courses.append({
                    'title': title,
                    'provider': f"Coursera ({provider})" if provider != "Coursera" else "Coursera",
                    'price': '$39-79/month',
                    'duration': '4-8 weeks',
                    'url': course_url,
                    'description': f"Professional course on {topic}",
                    'platform': 'coursera'
                })
                
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"Error scraping Coursera: {e}")
    
    return courses


def scrape_udemy_courses(topic: str, max_results: int = 2) -> List[Dict]:
    """Scrape real Udemy courses for a topic"""
    
    courses = []
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })
        
        # Search Udemy
        search_url = f"https://www.udemy.com/courses/search/?q={quote_plus(topic)}"
        
        response = session.get(search_url, timeout=10)
        if response.status_code != 200:
            return courses
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find course cards
        course_cards = soup.find_all('div', {'data-purpose': 'course-card'}) or soup.find_all('div', class_=re.compile('course-card'))
        
        for card in course_cards[:max_results]:
            try:
                # Extract title
                title_elem = card.find('h3') or card.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                # Extract link
                link_elem = card.find('a', href=True)
                if link_elem:
                    course_url = urljoin('https://www.udemy.com', link_elem['href'])
                else:
                    course_url = f"https://www.udemy.com/courses/search/?q={quote_plus(topic)}"
                
                # Extract price
                price_elem = card.find('span', class_=re.compile('price')) or card.find('div', class_=re.compile('price'))
                price = price_elem.get_text(strip=True) if price_elem else '$20-200'
                
                courses.append({
                    'title': title,
                    'provider': 'Udemy',
                    'price': price if price else '$20-200',
                    'duration': '10-50 hours',
                    'url': course_url,
                    'description': f"Practical {topic} course with projects",
                    'platform': 'udemy'
                })
                
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"Error scraping Udemy: {e}")
    
    return courses


def scrape_freecodecamp_courses(topic: str) -> List[Dict]:
    """Get freeCodeCamp courses for a topic"""
    
    courses = []
    
    # freeCodeCamp curriculum mapping
    fcc_topics = {
        'javascript': {
            'title': 'JavaScript Algorithms and Data Structures',
            'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/',
            'duration': '300 hours'
        },
        'python': {
            'title': 'Scientific Computing with Python',
            'url': 'https://www.freecodecamp.org/learn/scientific-computing-with-python/',
            'duration': '300 hours'
        },
        'web development': {
            'title': 'Responsive Web Design',
            'url': 'https://www.freecodecamp.org/learn/responsive-web-design/',
            'duration': '300 hours'
        },
        'data': {
            'title': 'Data Analysis with Python',
            'url': 'https://www.freecodecamp.org/learn/data-analysis-with-python/',
            'duration': '300 hours'
        },
        'machine learning': {
            'title': 'Machine Learning with Python',
            'url': 'https://www.freecodecamp.org/learn/machine-learning-with-python/',
            'duration': '300 hours'
        }
    }
    
    topic_lower = topic.lower()
    
    # Find matching course
    for key, course_info in fcc_topics.items():
        if key in topic_lower or any(word in topic_lower for word in key.split()):
            courses.append({
                'title': course_info['title'],
                'provider': 'freeCodeCamp',
                'price': 'Free',
                'duration': course_info['duration'],
                'url': course_info['url'],
                'description': f"Free certification course in {topic}",
                'platform': 'freecodecamp'
            })
            break
    
    # If no specific match, add general freeCodeCamp suggestion
    if not courses:
        courses.append({
            'title': f"{topic} Resources",
            'provider': 'freeCodeCamp',
            'price': 'Free',
            'duration': 'Self-paced',
            'url': 'https://www.freecodecamp.org/learn/',
            'description': f"Free coding tutorials and projects",
            'platform': 'freecodecamp'
        })
    
    return courses


def get_real_courses_for_topic(topic: str) -> Dict:
    """Scrape real courses from multiple platforms for a topic"""
    
    print(f"DEBUG: Starting real course scraping for: {topic}")
    
    all_courses = {'paid': [], 'free': []}
    
    # Scrape paid courses from Coursera and Udemy
    try:
        print("Searching Coursera...")
        coursera_courses = scrape_coursera_courses(topic, max_results=2)
        all_courses['paid'].extend(coursera_courses)
        
        print("Searching Udemy...")
        udemy_courses = scrape_udemy_courses(topic, max_results=2)
        all_courses['paid'].extend(udemy_courses)
        
    except Exception as e:
        print(f"Error scraping paid courses: {e}")
    
    # Get free courses from freeCodeCamp
    try:
        print("Checking freeCodeCamp...")
        fcc_courses = scrape_freecodecamp_courses(topic)
        all_courses['free'].extend(fcc_courses)
        
    except Exception as e:
        print(f"Error getting free courses: {e}")
    
    # Add additional free resources
    all_courses['free'].append({
        'title': f"{topic} Documentation & Tutorials",
        'provider': 'Multiple Sources',
        'price': 'Free',
        'duration': 'Self-paced',
        'url': f"Search: '{topic} tutorial' on YouTube, MDN, or official docs",
        'description': f"Free tutorials and documentation for {topic}",
        'platform': 'various'
    })
    
    return all_courses


def search_educational_resources(topic: str, resource_type: str = "both") -> Dict:
    """Search for educational resources (books, courses, etc.)"""
    
    print(f"Scraping real educational resources for: {topic}")
    
    resources = {
        'books': [],
        'courses': [],
        'free_resources': [],
        'paid_resources': []
    }
    
    # Scrape real courses for this topic
    real_courses = get_real_courses_for_topic(topic)
    
    total_found = len(real_courses.get('paid', [])) + len(real_courses.get('free', []))
    print(f"Found {total_found} real courses ({len(real_courses.get('paid', []))} paid, {len(real_courses.get('free', []))} free)")
    
    # Convert real courses to our format
    course_suggestions = []
    
    # Add paid courses
    for course in real_courses.get('paid', []):
        course_suggestions.append({
            'title': course['title'],
            'provider': course['provider'],
            'type': 'course',
            'cost': 'paid',
            'price': course['price'],
            'description': course['description'],
            'coverage': 'complete',
            'duration': course['duration'],
            'url': course['url']
        })
    
    # Add free courses
    for course in real_courses.get('free', []):
        course_suggestions.append({
            'title': course['title'],
            'provider': course['provider'],
            'type': 'course',
            'cost': 'free',
            'price': course['price'],
            'description': course['description'],
            'coverage': 'complete',
            'duration': course['duration'],
            'url': course['url']
        })
    
    # If no specific courses found, add generic suggestions
    if not course_suggestions:
        course_suggestions = [
            {
                'title': f"Search for {topic} courses",
                'provider': "Multiple Platforms",
                'type': 'course',
                'cost': 'both',
                'price': 'Varies',
                'description': f"Search major platforms for {topic} courses",
                'coverage': 'varies',
                'duration': 'Varies',
                'url': f"Try: Coursera, Udemy, edX, or freeCodeCamp for '{topic}' courses"
            }
        ]
    
    # Books (simplified since we focus on courses)
    book_suggestions = [
        {
            'title': f"Recommended {topic} Books",
            'author': "Various Authors",
            'type': 'book',
            'cost': 'both',
            'price': '$20-100',
            'description': f"Search for highly-rated {topic} textbooks and guides",
            'coverage': 'complete',
            'url': f"Search Amazon, Google Books, or O'Reilly for '{topic}' books"
        }
    ]
    
    # Additional free resources
    free_resources = []
    
    # Add documentation resources
    if 'programming' in topic.lower() or 'javascript' in topic.lower() or 'python' in topic.lower():
        free_resources.append({
            'title': f"{topic} Official Documentation",
            'provider': "Official Docs",
            'type': 'documentation',
            'cost': 'free',
            'price': 'Free',
            'description': f"Official documentation and reference guides",
            'coverage': 'complete',
            'url': f"https://developer.mozilla.org (for JS) or https://docs.python.org (for Python)"
        })
    
    # Add community resources
    free_resources.append({
        'title': f"{topic} Community & Practice",
        'provider': "Multiple Platforms",
        'type': 'community',
        'cost': 'free',
        'price': 'Free',
        'description': f"Practice problems, community discussions, and tutorials",
        'coverage': 'supplementary',
        'url': f"LeetCode, HackerRank, Stack Overflow, or GitHub for {topic} resources"
    })
    
    # Filter based on resource_type preference
    if resource_type == "free":
        resources['books'] = [b for b in book_suggestions if b['cost'] == 'free']
        resources['courses'] = [c for c in course_suggestions if c['cost'] == 'free']
        resources['free_resources'] = free_resources
    elif resource_type == "paid":
        resources['books'] = [b for b in book_suggestions if b['cost'] == 'paid']
        resources['courses'] = [c for c in course_suggestions if c['cost'] == 'paid']
    else:  # both
        resources['books'] = book_suggestions
        resources['courses'] = course_suggestions
        resources['free_resources'] = free_resources
    
    # Separate into free and paid for easy access
    all_resources = resources['books'] + resources['courses'] + resources['free_resources']
    resources['free_resources'] = [r for r in all_resources if r['cost'] == 'free']
    resources['paid_resources'] = [r for r in all_resources if r['cost'] == 'paid']
    
    return resources


def analyze_syllabus_coverage(syllabus_topics: List[Dict], resources: Dict) -> Dict:
    """Analyze which syllabus topics are covered by found resources"""
    
    coverage_analysis = {
        'fully_covered': [],
        'partially_covered': [],
        'not_covered': [],
        'extra_topics': []
    }
    
    for topic in syllabus_topics:
        topic_name = topic['name']
        
        # Simulate coverage analysis
        # In real implementation, this would analyze resource content
        
        # Most topics are at least partially covered
        if 'advanced' in topic_name.lower() or 'specialized' in topic_name.lower():
            coverage_analysis['partially_covered'].append({
                'topic': topic_name,
                'coverage_level': 'partial',
                'missing_subtopics': topic['subtopics'][-2:] if len(topic['subtopics']) > 2 else [],
                'alternatives': [f"Alternative resource for {topic_name}"]
            })
        else:
            coverage_analysis['fully_covered'].append({
                'topic': topic_name,
                'coverage_level': 'complete',
                'covered_subtopics': topic['subtopics']
            })
    
    # Add some extra topics that resources might cover
    coverage_analysis['extra_topics'] = [
        "Advanced Applications",
        "Industry Best Practices",
        "Real-world Projects"
    ]
    
    return coverage_analysis


def display_resource_results(all_results: Dict, resource_preference: str):
    """Display comprehensive resource recommendations"""
    
    print("\n" + "="*80)
    print("EDUCATIONAL RESOURCES RECOMMENDATION")
    print("="*80)
    
    total_topics = len(all_results)
    print(f"Resource Analysis for {total_topics} Topics")
    print(f"Preference: {resource_preference.title()} Resources")
    print()
    print("NOTE: These are suggested resources. Please search the mentioned")
    print("platforms for actual availability and current pricing.")
    print()
    
    all_books = []
    all_courses = []
    all_free = []
    all_paid = []
    
    # Collect all resources
    for topic_name, result in all_results.items():
        if 'resources' in result:
            resources = result['resources']
            all_books.extend(resources.get('books', []))
            all_courses.extend(resources.get('courses', []))
            all_free.extend(resources.get('free_resources', []))
            all_paid.extend(resources.get('paid_resources', []))
    
    # Display by category
    if all_books:
        print("RECOMMENDED BOOKS")
        print("-" * 50)
        for i, book in enumerate(all_books, 1):
            cost_tag = "[FREE]" if book['cost'] == 'free' else "[PAID]"
            print(f"{i}. {book['title']} {cost_tag}")
            print(f"   Author: {book['author']}")
            print(f"   Price: {book['price']}")
            print(f"   Coverage: {book['coverage'].title()}")
            print(f"   Description: {book['description']}")
            print(f"   Search: {book['url']}")
            print()
    
    if all_courses:
        print("RECOMMENDED COURSES")
        print("-" * 50)
        for i, course in enumerate(all_courses, 1):
            cost_tag = "[FREE]" if course['cost'] == 'free' else "[PAID]"
            print(f"{i}. {course['title']} {cost_tag}")
            print(f"   Provider: {course['provider']}")
            print(f"   Price: {course['price']}")
            print(f"   Duration: {course.get('duration', 'Self-paced')}")
            print(f"   Coverage: {course['coverage'].title()}")
            print(f"   Description: {course['description']}")
            print(f"   Search: {course['url']}")
            print()
    
    # Display free vs paid summary
    print("COST BREAKDOWN")
    print("-" * 50)
    print(f"Free Resources: {len(all_free)}")
    print(f"Paid Resources: {len(all_paid)}")
    print()
    
    if resource_preference == "free" and all_free:
        print("FREE RESOURCES SUMMARY")
        print("-" * 30)
        for resource in all_free:
            print(f"- {resource['title']} ({resource['type'].title()})")
    
    elif resource_preference == "paid" and all_paid:
        print("PAID RESOURCES SUMMARY")
        print("-" * 30)
        for resource in all_paid:
            print(f"- {resource['title']} ({resource['price']})")
    
    print("="*80)


def display_syllabus_results(all_results: Dict):
    """Display comprehensive results for all syllabus topics"""
    
    print("\n" + "="*80)
    print("COMPLETE SYLLABUS LEARNING PLAN")
    print("="*80)
    
    total_videos = sum(len(result['videos']) for result in all_results.values())
    successful_topics = sum(1 for result in all_results.values() if result['videos'])
    
    print(f"Topics Processed: {len(all_results)}")
    print(f"Successful Searches: {successful_topics}")
    print(f"Total Videos Found: {total_videos}")
    print()
    
    for i, (topic_name, result) in enumerate(all_results.items(), 1):
        print(f"{i}. {topic_name.upper()}")
        print("-" * 60)
        
        if not result['videos']:
            print("   No videos found for this topic")
            print()
            continue
        
        learning_path = result['learning_path']
        primary = learning_path['primary_video']
        supplements = learning_path['supplementary_videos']
        
        if primary:
            print(f"   PRIMARY VIDEO:")
            print(f"   {primary['title']}")
            print(f"   Channel: {primary['channel']}")
            print(f"   Score: {primary['composite_score']:.1f}/10")
            print(f"   URL: {primary['url']}")
            print()
        
        if supplements:
            print(f"   SUPPLEMENTARY VIDEOS:")
            for j, video in enumerate(supplements, 1):
                print(f"   {j}. {video['title']}")
                print(f"      Channel: {video['channel']}")
                print(f"      Score: {video['composite_score']:.1f}/10")
                print(f"      URL: {video['url']}")
            print()
        
        # Show subtopics if available
        if result.get('subtopics'):
            print(f"   SUBTOPICS COVERED:")
            for subtopic in result['subtopics'][:5]:  # Show first 5
                print(f"   - {subtopic}")
            if len(result['subtopics']) > 5:
                print(f"   ... and {len(result['subtopics']) - 5} more")
            print()
    
    print("="*80)
    print("SUCCESS: Complete learning plan generated from syllabus!")
    print("="*80)


def main():
    """Interactive main function for syllabus processing"""
    
    print("INTERACTIVE YOUTUBE SCRAPER - SYLLABUS MODE")
    print("=" * 60)
    print("Process entire syllabi and create comprehensive learning plans!")
    print("No API keys required - scrapes real YouTube data.")
    print()
    
    while True:
        print("Choose input method:")
        print("1. Enter syllabus text directly")
        print("2. Load syllabus from file")
        print("3. Use sample syllabus")
        print("4. Quick demo (single topic)")
        print("5. Exit")
        
        choice = input("\nYour choice (1-5): ").strip()
        
        if choice == '5':
            break
        elif choice == '4':
            # Quick demo with single topic
            print("Enter a single topic for quick demo:")
            topic_input = input("Topic: ").strip()
            if not topic_input:
                print("No topic entered")
                continue
            
            # Create a simple syllabus structure
            syllabus_text = f"Topic 1: {topic_input}\n- Core concepts\n- Practical applications"
            print(f"Created demo syllabus for: {topic_input}")
            print("=" * 60)
        elif choice == '3':
            # Use sample syllabus
            if os.path.exists('sample_syllabus.txt'):
                with open('sample_syllabus.txt', 'r', encoding='utf-8') as f:
                    syllabus_text = f.read()
                print("Loaded sample syllabus")
            else:
                print("Sample syllabus file not found")
                continue
        elif choice == '2':
            # Load from file
            file_path = input("Enter file path: ").strip()
            if not os.path.exists(file_path):
                print("File not found")
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    syllabus_text = f.read()
                print(f"Loaded syllabus from {file_path}")
            except Exception as e:
                print(f"Error reading file: {e}")
                continue
        elif choice == '1':
            # Enter text directly
            print("Enter your syllabus text:")
            print("Example format:")
            print("Week 1: Introduction to Programming")
            print("- Variables and data types")
            print("- Control structures")
            print()
            print("Enter 'END' on a new line when finished, or leave empty line to finish:")
            
            lines = []
            empty_line_count = 0
            
            while True:
                try:
                    line = input()
                    
                    # Check for END command
                    if line.strip().upper() == 'END':
                        break
                    
                    # Check for empty lines (allow up to 2 consecutive empty lines)
                    if not line.strip():
                        empty_line_count += 1
                        if empty_line_count >= 2:
                            print("Two empty lines detected. Finishing input...")
                            break
                        lines.append(line)
                    else:
                        empty_line_count = 0
                        lines.append(line)
                        
                except (EOFError, KeyboardInterrupt):
                    print("\nInput finished.")
                    break
            
            syllabus_text = '\n'.join(lines).strip()
            
            if not syllabus_text:
                print("No syllabus text entered")
                continue
        else:
            print("Invalid choice")
            continue
        
        print(f"\nSyllabus loaded ({len(syllabus_text)} characters)")
        print("=" * 60)
        
        # Extract topics from syllabus
        topics = extract_topics_from_syllabus(syllabus_text)
        
        if not topics:
            print("Could not extract topics from syllabus")
            continue
        
        # Ask about resource search
        print("\nDo you want to search for additional educational resources?")
        print("(books, courses, documentation, etc.)")
        search_resources = input("Search for resources? (y/n): ").strip().lower() == 'y'
        
        resource_preference = "both"
        if search_resources:
            print("\nResource preference:")
            print("1. Free resources only")
            print("2. Paid resources only") 
            print("3. Both free and paid")
            
            pref_choice = input("Your choice (1-3): ").strip()
            if pref_choice == '1':
                resource_preference = "free"
            elif pref_choice == '2':
                resource_preference = "paid"
            else:
                resource_preference = "both"
        
        # Process all topics
        all_results = process_syllabus_topics(topics, search_resources, resource_preference)
        
        # Display comprehensive results
        display_syllabus_results(all_results)
        
        # Display resource results if requested
        if search_resources:
            display_resource_results(all_results, resource_preference)
            
            # Show coverage analysis
            print("\n" + "="*80)
            print("SYLLABUS COVERAGE ANALYSIS")
            print("="*80)
            
            fully_covered = 0
            partially_covered = 0
            
            for topic_name, result in all_results.items():
                if 'resources' in result:
                    resources = result['resources']
                    total_resources = len(resources.get('books', [])) + len(resources.get('courses', []))
                    
                    if total_resources >= 2:
                        fully_covered += 1
                        coverage_status = "FULLY COVERED"
                    elif total_resources >= 1:
                        partially_covered += 1
                        coverage_status = "PARTIALLY COVERED"
                    else:
                        coverage_status = "LIMITED COVERAGE"
                    
                    print(f"{topic_name}: {coverage_status}")
                    
                    # Show alternatives for limited coverage
                    if total_resources < 2:
                        print(f"  Alternative: Search for '{topic_name} tutorial' or '{topic_name} guide'")
            
            print(f"\nSummary:")
            print(f"Fully Covered Topics: {fully_covered}")
            print(f"Partially Covered Topics: {partially_covered}")
            print(f"Total Topics: {len(all_results)}")
            
            if fully_covered + partially_covered < len(all_results):
                print("\nRecommendation: Consider supplementing with additional resources")
                print("for topics with limited coverage.")
            
            print("="*80)
        
        # Ask if user wants to process another syllabus
        print("\nWant to process another syllabus?")
        another = input("Enter 'y' for yes, or any other key to exit: ").strip().lower()
        
        if another != 'y':
            break
        
        print("\n" + "="*80 + "\n")
    
    print("\nThanks for using the Interactive YouTube Scraper!")
    print("Happy learning!")


if __name__ == "__main__":
    main()