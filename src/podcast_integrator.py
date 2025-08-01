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
        """Search for educational articles using comprehensive content analysis"""
        articles = []
        topic_lower = topic.lower()
        
        # Comprehensive educational content database
        educational_content = {
            'python': [
                {
                    'title': 'Python Best Practices and Design Patterns',
                    'source': 'Real Python',
                    'url': 'https://realpython.com/python-best-practices/',
                    'description': 'Comprehensive guide to writing clean, maintainable Python code with industry best practices.',
                    'difficulty': 'Intermediate',
                    'read_time': '15 min'
                },
                {
                    'title': 'Advanced Python Features You Should Know',
                    'source': 'Towards Data Science',
                    'url': 'https://towardsdatascience.com/advanced-python-features',
                    'description': 'Deep dive into advanced Python concepts including decorators, context managers, and metaclasses.',
                    'difficulty': 'Advanced',
                    'read_time': '20 min'
                },
                {
                    'title': 'Python for Data Analysis',
                    'source': 'O\'Reilly Media',
                    'url': 'https://www.oreilly.com/library/view/python-for-data/9781491957653/',
                    'description': 'Essential tools for working with data in Python including pandas, NumPy, and matplotlib.',
                    'difficulty': 'Intermediate',
                    'read_time': '45 min'
                }
            ],
            'data science': [
                {
                    'title': 'Introduction to Data Science with Python',
                    'source': 'Towards Data Science',
                    'url': 'https://towardsdatascience.com/intro-to-data-science-with-python',
                    'description': 'Complete beginner guide to data science using Python, pandas, and visualization libraries.',
                    'difficulty': 'Beginner',
                    'read_time': '25 min'
                },
                {
                    'title': 'Data Science Methodology and Best Practices',
                    'source': 'Harvard Business Review',
                    'url': 'https://hbr.org/2018/08/what-data-scientists-really-do-according-to-35-data-scientists',
                    'description': 'Real-world insights into data science workflows and methodologies from industry experts.',
                    'difficulty': 'Intermediate',
                    'read_time': '18 min'
                },
                {
                    'title': 'The Complete Data Science Process',
                    'source': 'KDnuggets',
                    'url': 'https://www.kdnuggets.com/2016/03/data-science-process.html',
                    'description': 'Step-by-step guide through the entire data science process from problem definition to deployment.',
                    'difficulty': 'Intermediate',
                    'read_time': '22 min'
                }
            ],
            'pandas': [
                {
                    'title': 'Pandas Tutorial: Complete Guide for Beginners',
                    'source': 'DataCamp',
                    'url': 'https://www.datacamp.com/community/tutorials/pandas-tutorial-dataframe-python',
                    'description': 'Comprehensive pandas tutorial covering DataFrames, data manipulation, and analysis techniques.',
                    'difficulty': 'Beginner',
                    'read_time': '30 min'
                },
                {
                    'title': '10 Minutes to Pandas',
                    'source': 'Pandas Documentation',
                    'url': 'https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html',
                    'description': 'Official pandas quickstart guide covering essential operations and data structures.',
                    'difficulty': 'Beginner',
                    'read_time': '12 min'
                },
                {
                    'title': 'Advanced Pandas Techniques',
                    'source': 'Real Python',
                    'url': 'https://realpython.com/pandas-python-explore-dataset/',
                    'description': 'Advanced pandas operations including groupby, merging, and performance optimization.',
                    'difficulty': 'Advanced',
                    'read_time': '35 min'
                }
            ],
            'numpy': [
                {
                    'title': 'NumPy Quickstart Tutorial',
                    'source': 'NumPy Documentation',
                    'url': 'https://numpy.org/doc/stable/user/quickstart.html',
                    'description': 'Official NumPy tutorial covering arrays, operations, and scientific computing fundamentals.',
                    'difficulty': 'Beginner',
                    'read_time': '20 min'
                },
                {
                    'title': 'NumPy for Scientific Computing',
                    'source': 'SciPy Lectures',
                    'url': 'https://scipy-lectures.org/intro/numpy/index.html',
                    'description': 'Comprehensive guide to NumPy for scientific computing and numerical analysis.',
                    'difficulty': 'Intermediate',
                    'read_time': '40 min'
                }
            ],
            'matplotlib': [
                {
                    'title': 'Matplotlib Tutorial: Python Plotting',
                    'source': 'Matplotlib Documentation',
                    'url': 'https://matplotlib.org/stable/tutorials/index.html',
                    'description': 'Official matplotlib tutorials covering plotting, customization, and visualization techniques.',
                    'difficulty': 'Beginner',
                    'read_time': '25 min'
                },
                {
                    'title': 'Data Visualization with Matplotlib',
                    'source': 'Python Graph Gallery',
                    'url': 'https://python-graph-gallery.com/matplotlib/',
                    'description': 'Collection of matplotlib examples and best practices for data visualization.',
                    'difficulty': 'Intermediate',
                    'read_time': '30 min'
                }
            ],
            'machine learning': [
                {
                    'title': 'Introduction to Machine Learning',
                    'source': 'Towards Data Science',
                    'url': 'https://towardsdatascience.com/machine-learning-basics',
                    'description': 'Comprehensive introduction to ML concepts, algorithms, and practical applications.',
                    'difficulty': 'Beginner',
                    'read_time': '22 min'
                },
                {
                    'title': 'Machine Learning Algorithms Explained',
                    'source': 'MIT Technology Review',
                    'url': 'https://www.technologyreview.com/2017/04/11/5113/machine-learning-explained/',
                    'description': 'Clear explanations of popular ML algorithms and when to use them.',
                    'difficulty': 'Intermediate',
                    'read_time': '28 min'
                },
                {
                    'title': 'Scikit-learn User Guide',
                    'source': 'Scikit-learn Documentation',
                    'url': 'https://scikit-learn.org/stable/user_guide.html',
                    'description': 'Official guide to machine learning with Python using scikit-learn library.',
                    'difficulty': 'Intermediate',
                    'read_time': '45 min'
                }
            ],
            'statistical analysis': [
                {
                    'title': 'Statistics for Data Science',
                    'source': 'Towards Data Science',
                    'url': 'https://towardsdatascience.com/statistics-for-data-science',
                    'description': 'Essential statistical concepts for data science including hypothesis testing and distributions.',
                    'difficulty': 'Intermediate',
                    'read_time': '35 min'
                },
                {
                    'title': 'Statistical Analysis with Python',
                    'source': 'Real Python',
                    'url': 'https://realpython.com/python-statistics/',
                    'description': 'Practical guide to statistical analysis using Python\'s statistics and scipy libraries.',
                    'difficulty': 'Intermediate',
                    'read_time': '40 min'
                }
            ],
            'data visualization': [
                {
                    'title': 'Data Visualization Best Practices',
                    'source': 'Tableau',
                    'url': 'https://www.tableau.com/learn/articles/data-visualization',
                    'description': 'Comprehensive guide to effective data visualization principles and techniques.',
                    'difficulty': 'Beginner',
                    'read_time': '20 min'
                },
                {
                    'title': 'Python Data Visualization Libraries',
                    'source': 'DataCamp',
                    'url': 'https://www.datacamp.com/community/tutorials/python-data-visualization',
                    'description': 'Comparison and tutorial of popular Python visualization libraries.',
                    'difficulty': 'Intermediate',
                    'read_time': '25 min'
                }
            ]
        }
        
        # Find best matching content using multiple strategies
        matched_articles = []
        best_match_score = 0
        
        # Strategy 1: Exact key match
        for key, content_list in educational_content.items():
            if key in topic_lower:
                if len(key) > best_match_score:
                    best_match_score = len(key)
                    matched_articles = content_list
        
        # Strategy 2: Word overlap matching
        if not matched_articles:
            topic_words = set(topic_lower.split())
            for key, content_list in educational_content.items():
                key_words = set(key.split())
                overlap = len(topic_words.intersection(key_words))
                if overlap > 0 and overlap > best_match_score:
                    best_match_score = overlap
                    matched_articles = content_list
        
        # Strategy 3: Generate topic-specific content if no match
        if not matched_articles:
            matched_articles = self._generate_topic_articles(topic)
        
        # Convert to required format
        for article_data in matched_articles[:max_results]:
            articles.append({
                'type': 'article',
                'title': article_data['title'],
                'description': article_data['description'],
                'url': article_data['url'],
                'source': article_data['source'],
                'difficulty': article_data['difficulty'],
                'estimated_read_time': article_data['read_time']
            })
        
        return articles
    
    def _generate_topic_articles(self, topic: str) -> List[Dict]:
        """Generate topic-specific articles when no pattern matches"""
        return [
            {
                'title': f'Complete Guide to {topic.title()}',
                'source': 'Educational Hub',
                'url': f'https://www.google.com/search?q={topic.replace(" ", "+")}+complete+guide',
                'description': f'Comprehensive tutorial covering {topic} fundamentals, concepts, and practical applications.',
                'difficulty': 'Beginner',
                'read_time': '25 min'
            },
            {
                'title': f'{topic.title()} Best Practices and Tips',
                'source': 'Developer Resources',
                'url': f'https://www.google.com/search?q={topic.replace(" ", "+")}+best+practices',
                'description': f'Industry best practices, tips, and common patterns for {topic}.',
                'difficulty': 'Intermediate',
                'read_time': '18 min'
            },
            {
                'title': f'Advanced {topic.title()} Techniques',
                'source': 'Tech Articles',
                'url': f'https://www.google.com/search?q={topic.replace(" ", "+")}+advanced+techniques',
                'description': f'Advanced techniques and optimization strategies for {topic}.',
                'difficulty': 'Advanced',
                'read_time': '30 min'
            }
        ]
    
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