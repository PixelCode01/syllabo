from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import feedparser
from .logger import SyllaboLogger

class PodcastIntegrator:
    """Integrate educational podcasts and reading resources"""
    
    def __init__(self):
        self.logger = SyllaboLogger("podcast_integrator")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_podcasts(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Search for educational podcasts on a topic"""
        podcasts = []
        
        # Educational podcast feeds (curated list)
        educational_feeds = [
            {
                'name': 'TED Talks Education',
                'feed_url': 'https://feeds.feedburner.com/tedtalks_education',
                'description': 'Educational TED Talks'
            },
            {
                'name': 'Coursera Podcast',
                'feed_url': 'https://anchor.fm/s/coursera-podcast/podcast/rss',
                'description': 'Learning and career insights'
            },
            {
                'name': 'The Learning Scientists Podcast',
                'feed_url': 'https://feeds.buzzsprout.com/1750370.rss',
                'description': 'Science of learning'
            }
        ]
        
        for feed_info in educational_feeds:
            try:
                feed = feedparser.parse(feed_info['feed_url'])
                
                for entry in feed.entries[:max_results]:
                    if topic.lower() in entry.title.lower() or topic.lower() in entry.summary.lower():
                        podcast = {
                            'type': 'podcast',
                            'title': entry.title,
                            'description': entry.summary[:200] + '...' if len(entry.summary) > 200 else entry.summary,
                            'podcast_name': feed_info['name'],
                            'url': entry.link,
                            'published': entry.published if hasattr(entry, 'published') else 'Unknown',
                            'duration': getattr(entry, 'itunes_duration', 'Unknown')
                        }
                        podcasts.append(podcast)
                        
            except Exception as e:
                self.logger.error(f"Failed to parse feed {feed_info['name']}: {e}")
        
        return podcasts[:max_results]
    
    def search_reading_resources(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Search for reading resources (articles, papers, books)"""
        resources = []
        
        # Search academic papers
        arxiv_papers = self._search_arxiv(topic, max_results // 2)
        resources.extend(arxiv_papers)
        
        # Search educational articles
        articles = self._search_educational_articles(topic, max_results // 2)
        resources.extend(articles)
        
        return resources[:max_results]
    
    def _search_arxiv(self, topic: str, max_results: int) -> List[Dict]:
        """Search arXiv for academic papers"""
        try:
            search_url = f"http://export.arxiv.org/api/query?search_query=all:{topic}&start=0&max_results={max_results}"
            response = requests.get(search_url)
            
            papers = []
            soup = BeautifulSoup(response.content, 'xml')
            
            for entry in soup.find_all('entry'):
                title = entry.find('title').text.strip()
                summary = entry.find('summary').text.strip()
                authors = [author.find('name').text for author in entry.find_all('author')]
                link = entry.find('id').text
                
                paper = {
                    'type': 'academic_paper',
                    'title': title,
                    'description': summary[:300] + '...' if len(summary) > 300 else summary,
                    'authors': ', '.join(authors),
                    'url': link,
                    'source': 'arXiv',
                    'difficulty': 'advanced'
                }
                papers.append(paper)
            
            return papers
            
        except Exception as e:
            self.logger.error(f"Failed to search arXiv: {e}")
            return []
    
    def _search_educational_articles(self, topic: str, max_results: int) -> List[Dict]:
        """Search for educational articles and tutorials"""
        articles = []
        
        # Educational websites to search
        educational_sites = [
            'medium.com',
            'towardsdatascience.com',
            'freecodecamp.org',
            'khanacademy.org'
        ]
        
        for site in educational_sites:
            try:
                # This is a simplified search - real implementation would use proper APIs
                search_query = f"site:{site} {topic}"
                
                # Placeholder articles (in real implementation, would scrape search results)
                article = {
                    'type': 'article',
                    'title': f"{topic} Tutorial - {site.split('.')[0].title()}",
                    'description': f"Comprehensive guide to {topic} from {site}",
                    'url': f"https://{site}/search?q={topic.replace(' ', '+')}",
                    'source': site,
                    'difficulty': 'intermediate',
                    'estimated_read_time': '10-15 minutes'
                }
                articles.append(article)
                
            except Exception as e:
                self.logger.error(f"Failed to search {site}: {e}")
        
        return articles[:max_results]
    
    def ask_user_preference(self) -> Dict:
        """Ask user about their content preferences"""
        print("\nContent Preferences:")
        print("1. Include podcasts? (y/n)")
        include_podcasts = input().lower().startswith('y')
        
        print("2. Include reading materials? (y/n)")
        include_reading = input().lower().startswith('y')
        
        if include_reading:
            print("3. Preferred difficulty level:")
            print("   a) Beginner")
            print("   b) Intermediate") 
            print("   c) Advanced")
            print("   d) All levels")
            
            difficulty_choice = input().lower()
            difficulty_map = {
                'a': 'beginner',
                'b': 'intermediate', 
                'c': 'advanced',
                'd': 'all'
            }
            difficulty = difficulty_map.get(difficulty_choice, 'all')
        else:
            difficulty = 'all'
        
        return {
            'include_podcasts': include_podcasts,
            'include_reading': include_reading,
            'difficulty_preference': difficulty
        }
    
    def get_comprehensive_resources(self, topic: str, preferences: Dict) -> Dict:
        """Get comprehensive resources based on user preferences"""
        resources = {
            'podcasts': [],
            'articles': [],
            'academic_papers': [],
            'books': []
        }
        
        if preferences.get('include_podcasts', True):
            resources['podcasts'] = self.search_podcasts(topic)
        
        if preferences.get('include_reading', True):
            reading_resources = self.search_reading_resources(topic)
            
            # Filter by difficulty if specified
            difficulty = preferences.get('difficulty_preference', 'all')
            if difficulty != 'all':
                reading_resources = [
                    r for r in reading_resources 
                    if r.get('difficulty', 'intermediate') == difficulty
                ]
            
            # Separate by type
            for resource in reading_resources:
                if resource['type'] == 'academic_paper':
                    resources['academic_papers'].append(resource)
                else:
                    resources['articles'].append(resource)
        
        return resources
    
    def display_resources(self, resources: Dict):
        """Display resources in a formatted way"""
        for resource_type, items in resources.items():
            if items:
                print(f"\n{resource_type.upper().replace('_', ' ')}")
                print("-" * 40)
                
                for i, item in enumerate(items, 1):
                    print(f"{i}. {item['title']}")
                    print(f"   Source: {item.get('source', 'Unknown')}")
                    if 'duration' in item:
                        print(f"   Duration: {item['duration']}")
                    if 'estimated_read_time' in item:
                        print(f"   Read Time: {item['estimated_read_time']}")
                    print(f"   URL: {item['url']}")
                    print()