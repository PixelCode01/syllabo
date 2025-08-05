from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import asyncio
from .logger import SyllaboLogger
class PlatformIntegrator:
    """Integrat with multiple learning platforms"""
    
    def __init__(self):
        self.logger = SyllaboLogger("platform_integrator")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    async def search_coursera(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Search for Coursera courses using course database"""
        try:
            # Try web scraping first, then fallback to database
            search_url = f"https://www.coursera.org/search?query={topic.replace(' ', '%20')}"
            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            courses = []
            course_cards = soup.find_all('div', class_='cds-CommonCard-container')[:max_results]
            
            for card in course_cards:
                title_elem = card.find('h3')
                provider_elem = card.find('p', class_='cds-ProductCard-partnerNames')
                rating_elem = card.find('span', class_='cds-CommonCard-ratings')
                
                if title_elem:
                    course = {
                        'platform': 'Coursera',
                        'title': title_elem.get_text(strip=True),
                        'provider': provider_elem.get_text(strip=True) if provider_elem else 'Unknown',
                        'rating': rating_elem.get_text(strip=True) if rating_elem else 'N/A',
                        'type': 'course',
                        'url': f"https://www.coursera.org{card.find('a')['href']}" if card.find('a') else '',
                        'free': 'audit' in card.get_text().lower()
                    }
                    courses.append(course)
            
            if courses:
                return courses
            else:
                raise Exception("No courses found via scraping")
            
        except Exception as e:
            self.logger.error(f"Failed to search Coursera via scraping: {e}")
            # Fallback to course database
            return self._get_coursera_courses_from_database(topic, max_results)
    
    def _get_coursera_courses_from_database(self, topic: str, max_results: int) -> List[Dict]:
        """Get Coursera courses from internal database"""
        topic_lower = topic.lower()
        
        # Comprehensive course database
        coursera_courses = {
            'python': [
                {
                    'platform': 'Coursera',
                    'title': 'Python for Everybody Specialization',
                    'provider': 'University of Michigan',
                    'rating': '4.8',
                    'type': 'specialization',
                    'url': 'https://www.coursera.org/specializations/python',
                    'free': True,
                    'duration': '8 months',
                    'level': 'Beginner'
                },
                {
                    'platform': 'Coursera',
                    'title': 'Python Programming Fundamentals',
                    'provider': 'Duke University',
                    'rating': '4.7',
                    'type': 'course',
                    'url': 'https://www.coursera.org/learn/python-programming',
                    'free': True,
                    'duration': '4 weeks',
                    'level': 'Beginner'
                }
            ],
            'machine learning': [
                {
                    'platform': 'Coursera',
                    'title': 'Machine Learning Course',
                    'provider': 'Stanford University',
                    'rating': '4.9',
                    'type': 'course',
                    'url': 'https://www.coursera.org/learn/machine-learning',
                    'free': True,
                    'duration': '11 weeks',
                    'level': 'Intermediate'
                },
                {
                    'platform': 'Coursera',
                    'title': 'Machine Learning Specialization',
                    'provider': 'DeepLearning.AI',
                    'rating': '4.8',
                    'type': 'specialization',
                    'url': 'https://www.coursera.org/specializations/machine-learning-introduction',
                    'free': False,
                    'duration': '3 months',
                    'level': 'Intermediate'
                }
            ],
            'data science': [
                {
                    'platform': 'Coursera',
                    'title': 'Data Science Specialization',
                    'provider': 'Johns Hopkins University',
                    'rating': '4.6',
                    'type': 'specialization',
                    'url': 'https://www.coursera.org/specializations/jhu-data-science',
                    'free': True,
                    'duration': '11 months',
                    'level': 'Intermediate'
                },
                {
                    'platform': 'Coursera',
                    'title': 'IBM Data Science Professional Certificate',
                    'provider': 'IBM',
                    'rating': '4.5',
                    'type': 'certificate',
                    'url': 'https://www.coursera.org/professional-certificates/ibm-data-science',
                    'free': False,
                    'duration': '12 months',
                    'level': 'Beginner'
                }
            ]
        }
        
        # Find matching courses
        matched_courses = []
        for key, courses in coursera_courses.items():
            if key in topic_lower or any(word in topic_lower for word in key.split()):
                matched_courses.extend(courses)
        
        # If no specific match, return general programming courses
        if not matched_courses:
            matched_courses = coursera_courses.get('python', [])
        
        return matched_courses[:max_results]

    async def search_khan_academy(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Search Khan Academy content"""
        try:
            # Khan Academy has a search API
            api_url = f"https://www.khanacademy.org/api/internal/graphql/searchContent"
            
            # This is a simplified version - actual implementation would need proper API calls
            courses = [
                {
                    'platform': 'Khan Academy',
                    'title': f"{topic} - Khan Academy Course",
                    'provider': 'Khan Academy',
                    'rating': '4.8/5',
                    'type': 'course',
                    'url': f"https://www.khanacademy.org/search?page_search_query={topic.replace(' ', '%20')}",
                    'free': True
                }
            ]
            
            return courses
            
        except Exception as e:
            self.logger.error(f"Failed to search Khan Academy: {e}")
            return []
    
    async def search_edx(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Search edX courses"""
        try:
            search_url = f"https://www.edx.org/search?q={topic.replace(' ', '+')}"
            response = self.session.get(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            courses = []
            course_cards = soup.find_all('div', class_='discovery-card')[:max_results]
            
            for card in course_cards:
                title_elem = card.find('h3')
                provider_elem = card.find('span', class_='partner-name')
                
                if title_elem:
                    course = {
                        'platform': 'edX',
                        'title': title_elem.get_text(strip=True),
                        'provider': provider_elem.get_text(strip=True) if provider_elem else 'Unknown',
                        'rating': 'N/A',
                        'type': 'course',
                        'url': card.find('a')['href'] if card.find('a') else '',
                        'free': 'free' in card.get_text().lower()
                    }
                    courses.append(course)
            
            return courses
            
        except Exception as e:
            self.logger.error(f"Failed to search edX: {e}")
            return []
    
    async def search_all_platforms(self, topic: str, max_per_platform: int = 3) -> Dict[str, List[Dict]]:
        """Search all platforms simultaneously"""
        tasks = [
            self.search_coursera(topic, max_per_platform),
            self.search_khan_academy(topic, max_per_platform),
            self.search_edx(topic, max_per_platform)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            'coursera': results[0] if not isinstance(results[0], Exception) else [],
            'khan_academy': results[1] if not isinstance(results[1], Exception) else [],
            'edx': results[2] if not isinstance(results[2], Exception) else []
        }
    
    async def search_platform(self, platform: str, topic: str, max_results: int = 5) -> List[Dict]:
        """Search a specific platform"""
        if platform == "coursera":
            return await self.search_coursera(topic, max_results)
        elif platform == "khan_academy":
            return await self.search_khan_academy(topic, max_results)
        elif platform == "edx":
            return await self.search_edx(topic, max_results)
        elif platform == "youtube":
            # For YouTube, we'd need to implement YouTube search
            return []
        elif platform == "udemy":
            # For Udemy, we'd need to implement Udemy search
            return []
        else:
            return []
    
    def filter_by_preference(self, courses: List[Dict], 
                           free_only: bool = False, 
                           min_rating: float = 0.0) -> List[Dict]:
        """Filter courses by user preferences"""
        filtered = courses
        
        if free_only:
            filtered = [c for c in filtered if c.get('free', False)]
        
        if min_rating > 0:
            filtered = [c for c in filtered 
                       if self._parse_rating(c.get('rating', '0')) >= min_rating]
        
        return filtered
    
    def _parse_rating(self, rating_str: str) -> float:
        """Parse rating string to float"""
        try:
            if '/' in rating_str:
                return float(rating_str.split('/')[0])
            return float(rating_str)
        except:
            return 0.0
    
    async def get_course_details(self, course_url: str, platform: str) -> Dict:
        """Get detailed information about a specific course"""
        try:
            response = self.session.get(course_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Platform-specific parsing would go here
            details = {
                'description': 'Course description not available',
                'duration': 'Unknown',
                'level': 'Unknown',
                'prerequisites': [],
                'syllabus': []
            }
            
            return details
            
        except Exception as e:
            self.logger.error(f"Failed to get course details: {e}")
            return {}