import asyncio
from typing import List, Dict, Optional
from .ai_client import AIClient
from .logger import SyllaboLogger

class ResourceFinder:
    """Find books, courses, and other learning resources for syllabus topics"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.logger = SyllaboLogger("resource_finder")
        
        # Comprehensive resource database
        self.resource_database = {
            'python': {
                'books': [
                    {'title': 'Python Crash Course', 'author': 'Eric Matthes', 'type': 'paid', 'price': '$39.99', 'topics': ['basics', 'projects', 'web_development']},
                    {'title': 'Automate the Boring Stuff', 'author': 'Al Sweigart', 'type': 'free', 'price': 'Free online', 'topics': ['automation', 'basics', 'practical']},
                    {'title': 'Effective Python', 'author': 'Brett Slatkin', 'type': 'paid', 'price': '$44.99', 'topics': ['advanced', 'best_practices']},
                    {'title': 'Python Tricks', 'author': 'Dan Bader', 'type': 'paid', 'price': '$29.99', 'topics': ['intermediate', 'tricks', 'clean_code']}
                ],
                'courses': [
                    {'title': 'Complete Python Bootcamp', 'platform': 'Udemy', 'type': 'paid', 'price': '$84.99', 'topics': ['basics', 'advanced', 'projects']},
                    {'title': 'Python for Everybody', 'platform': 'Coursera', 'type': 'free', 'price': 'Free audit', 'topics': ['basics', 'data_structures']},
                    {'title': 'CS50 Python', 'platform': 'edX', 'type': 'free', 'price': 'Free', 'topics': ['computer_science', 'programming_fundamentals']},
                    {'title': 'Real Python Membership', 'platform': 'Real Python', 'type': 'paid', 'price': '$60/year', 'topics': ['all_levels', 'tutorials', 'projects']}
                ],
                'resources': [
                    {'title': 'Python.org Tutorial', 'type': 'free', 'url': 'python.org', 'topics': ['official_docs', 'basics']},
                    {'title': 'Python Package Index', 'type': 'free', 'url': 'pypi.org', 'topics': ['packages', 'libraries']},
                    {'title': 'Python Weekly Newsletter', 'type': 'free', 'url': 'pythonweekly.com', 'topics': ['news', 'updates']}
                ]
            },
            'data_science': {
                'books': [
                    {'title': 'Python for Data Analysis', 'author': 'Wes McKinney', 'type': 'paid', 'price': '$49.99', 'topics': ['pandas', 'numpy', 'data_manipulation']},
                    {'title': 'Hands-On Machine Learning', 'author': 'Aurélien Géron', 'type': 'paid', 'price': '$54.99', 'topics': ['machine_learning', 'scikit_learn', 'tensorflow']},
                    {'title': 'The Elements of Statistical Learning', 'author': 'Hastie, Tibshirani, Friedman', 'type': 'free', 'price': 'Free PDF', 'topics': ['statistics', 'machine_learning', 'theory']},
                    {'title': 'Python Data Science Handbook', 'author': 'Jake VanderPlas', 'type': 'free', 'price': 'Free online', 'topics': ['numpy', 'pandas', 'matplotlib', 'scikit_learn']}
                ],
                'courses': [
                    {'title': 'Data Science Specialization', 'platform': 'Coursera', 'type': 'paid', 'price': '$49/month', 'topics': ['r_programming', 'statistics', 'machine_learning']},
                    {'title': 'CS109 Data Science', 'platform': 'Harvard', 'type': 'free', 'price': 'Free materials', 'topics': ['statistics', 'python', 'visualization']},
                    {'title': 'Applied Data Science with Python', 'platform': 'Coursera', 'type': 'paid', 'price': '$49/month', 'topics': ['python', 'pandas', 'machine_learning', 'visualization']},
                    {'title': 'Fast.ai Practical Deep Learning', 'platform': 'fast.ai', 'type': 'free', 'price': 'Free', 'topics': ['deep_learning', 'practical', 'pytorch']}
                ]
            },
            'machine_learning': {
                'books': [
                    {'title': 'Pattern Recognition and Machine Learning', 'author': 'Christopher Bishop', 'type': 'paid', 'price': '$94.99', 'topics': ['theory', 'mathematics', 'algorithms']},
                    {'title': 'Machine Learning Yearning', 'author': 'Andrew Ng', 'type': 'free', 'price': 'Free PDF', 'topics': ['strategy', 'practical_advice']},
                    {'title': 'Introduction to Statistical Learning', 'author': 'James, Witten, Hastie, Tibshirani', 'type': 'free', 'price': 'Free PDF', 'topics': ['statistics', 'r_programming', 'theory']}
                ],
                'courses': [
                    {'title': 'Machine Learning Course', 'platform': 'Coursera', 'type': 'free', 'price': 'Free audit', 'topics': ['andrew_ng', 'fundamentals', 'octave']},
                    {'title': 'CS229 Machine Learning', 'platform': 'Stanford', 'type': 'free', 'price': 'Free materials', 'topics': ['theory', 'mathematics', 'algorithms']},
                    {'title': 'Machine Learning Specialization', 'platform': 'Coursera', 'type': 'paid', 'price': '$49/month', 'topics': ['supervised_learning', 'unsupervised_learning', 'neural_networks']}
                ]
            },
            'javascript': {
                'books': [
                    {'title': 'Eloquent JavaScript', 'author': 'Marijn Haverbeke', 'type': 'free', 'price': 'Free online', 'topics': ['fundamentals', 'functional_programming', 'dom']},
                    {'title': 'You Don\'t Know JS', 'author': 'Kyle Simpson', 'type': 'free', 'price': 'Free online', 'topics': ['deep_dive', 'advanced', 'concepts']},
                    {'title': 'JavaScript: The Good Parts', 'author': 'Douglas Crockford', 'type': 'paid', 'price': '$29.99', 'topics': ['best_practices', 'clean_code']},
                    {'title': 'Modern JavaScript for the Impatient', 'author': 'Cay Horstmann', 'type': 'paid', 'price': '$44.99', 'topics': ['es6', 'modern_features']}
                ],
                'courses': [
                    {'title': 'JavaScript Algorithms and Data Structures', 'platform': 'freeCodeCamp', 'type': 'free', 'price': 'Free', 'topics': ['algorithms', 'data_structures', 'certification']},
                    {'title': 'The Complete JavaScript Course', 'platform': 'Udemy', 'type': 'paid', 'price': '$84.99', 'topics': ['fundamentals', 'advanced', 'projects']},
                    {'title': 'JavaScript30', 'platform': 'Wes Bos', 'type': 'free', 'price': 'Free', 'topics': ['projects', 'vanilla_js', 'practical']}
                ]
            }
        }
    
    async def find_resources_for_syllabus(self, syllabus_topics: List[str], 
                                        preference: str = 'both') -> Dict:
        """Find best resources for all syllabus topics"""
        print(f"\nFinding learning resources for {len(syllabus_topics)} topics...")
        
        # Ask user preference if not specified
        if preference == 'ask':
            preference = self._ask_user_preference()
        
        all_resources = {
            'books': [],
            'courses': [],
            'free_resources': [],
            'paid_resources': [],
            'topic_coverage': {},
            'missing_topics': [],
            'alternatives': {}
        }
        
        for topic in syllabus_topics:
            topic_resources = await self._find_topic_resources(topic, preference)
            
            # Merge resources
            all_resources['books'].extend(topic_resources['books'])
            all_resources['courses'].extend(topic_resources['courses'])
            
            # Track coverage
            all_resources['topic_coverage'][topic] = topic_resources['coverage_analysis']
            
            if not topic_resources['books'] and not topic_resources['courses']:
                all_resources['missing_topics'].append(topic)
                all_resources['alternatives'][topic] = self._suggest_alternatives(topic)
        
        # Remove duplicates and organize
        all_resources = self._organize_resources(all_resources, preference)
        
        return all_resources
    
    def _ask_user_preference(self) -> str:
        """Ask user about resource preferences"""
        print("\nResource preference options:")
        print("1. Free resources only")
        print("2. Paid resources only") 
        print("3. Both free and paid resources")
        
        choice = input("Choose your preference (1-3, default: 3): ").strip()
        preference_map = {'1': 'free', '2': 'paid', '3': 'both'}
        return preference_map.get(choice, 'both')
    
    async def _find_topic_resources(self, topic: str, preference: str) -> Dict:
        """Find resources for a specific topic"""
        topic_lower = topic.lower().replace(' ', '_')
        
        # Find matching resources in database
        matched_resources = {'books': [], 'courses': [], 'resources': []}
        coverage_analysis = {'covered_subtopics': [], 'missing_subtopics': []}
        
        # Search for exact and partial matches
        for key, resource_data in self.resource_database.items():
            if key in topic_lower or any(word in key for word in topic_lower.split('_')):
                # Filter by preference
                for resource_type in ['books', 'courses', 'resources']:
                    if resource_type in resource_data:
                        for resource in resource_data[resource_type]:
                            if preference == 'both' or resource['type'] == preference:
                                resource['topic_match'] = topic
                                matched_resources[resource_type].append(resource)
        
        # If no direct matches, use AI to suggest similar resources
        if not any(matched_resources.values()):
            matched_resources = await self._ai_suggest_resources(topic, preference)
        
        # Analyze topic coverage
        coverage_analysis = self._analyze_topic_coverage(topic, matched_resources)
        
        return {
            'books': matched_resources['books'][:5],  # Top 5 books
            'courses': matched_resources['courses'][:5],  # Top 5 courses
            'resources': matched_resources.get('resources', [])[:3],  # Top 3 other resources
            'coverage_analysis': coverage_analysis
        }
    
    async def _ai_suggest_resources(self, topic: str, preference: str) -> Dict:
        """Use AI to suggest resources when no database matches found"""
        try:
            prompt = f"""Suggest learning resources for the topic "{topic}".
            
Provide 3-5 resources in each category:
1. Books (include author, estimated price, key topics covered)
2. Online courses (include platform, price type, key topics)
3. Free resources (websites, documentation, tutorials)

Format as a structured list. Focus on {preference} resources when possible.
Be realistic about prices and availability."""

            response = await self.ai_client.get_completion(prompt)
            
            # Parse AI response into structured format
            return self._parse_ai_resource_response(response, topic, preference)
            
        except Exception as e:
            self.logger.error(f"AI resource suggestion failed: {e}")
            return self._generate_fallback_resources(topic, preference)
    
    def _parse_ai_resource_response(self, response: str, topic: str, preference: str) -> Dict:
        """Parse AI response into structured resource format"""
        resources = {'books': [], 'courses': [], 'resources': []}
        
        lines = response.split('\n')
        current_category = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect category headers
            if 'book' in line.lower() and ':' in line:
                current_category = 'books'
                continue
            elif 'course' in line.lower() and ':' in line:
                current_category = 'courses'
                continue
            elif 'resource' in line.lower() and ':' in line:
                current_category = 'resources'
                continue
            
            # Parse resource entries
            if current_category and (line.startswith('-') or line.startswith('•')):
                resource = self._parse_resource_line(line, current_category, topic, preference)
                if resource:
                    resources[current_category].append(resource)
        
        return resources
    
    def _parse_resource_line(self, line: str, category: str, topic: str, preference: str) -> Optional[Dict]:
        """Parse a single resource line from AI response"""
        line = line.lstrip('-•').strip()
        
        if category == 'books':
            # Try to extract title, author, price
            parts = line.split(' by ')
            if len(parts) >= 2:
                title = parts[0].strip()
                author_price = parts[1].strip()
                
                # Extract price if mentioned
                price = 'Check price'
                if '$' in author_price:
                    price_match = author_price.split('$')
                    if len(price_match) > 1:
                        price = f"${price_match[1].split()[0]}"
                
                return {
                    'title': title,
                    'author': author_price.split('$')[0].strip(),
                    'type': 'paid' if '$' in line else 'free',
                    'price': price,
                    'topics': [topic.lower()],
                    'topic_match': topic
                }
        
        elif category == 'courses':
            # Extract course info
            title = line.split('(')[0].strip()
            platform = 'Various platforms'
            
            if 'coursera' in line.lower():
                platform = 'Coursera'
            elif 'udemy' in line.lower():
                platform = 'Udemy'
            elif 'edx' in line.lower():
                platform = 'edX'
            
            return {
                'title': title,
                'platform': platform,
                'type': 'paid' if '$' in line or 'paid' in line.lower() else 'free',
                'price': 'Check platform',
                'topics': [topic.lower()],
                'topic_match': topic
            }
        
        elif category == 'resources':
            return {
                'title': line,
                'type': 'free',
                'url': 'Search online',
                'topics': [topic.lower()],
                'topic_match': topic
            }
        
        return None
    
    def _generate_fallback_resources(self, topic: str, preference: str) -> Dict:
        """Generate fallback resources when AI fails"""
        return {
            'books': [
                {
                    'title': f'Complete Guide to {topic.title()}',
                    'author': 'Various Authors',
                    'type': 'paid',
                    'price': '$30-50',
                    'topics': [topic.lower()],
                    'topic_match': topic
                }
            ],
            'courses': [
                {
                    'title': f'{topic.title()} Fundamentals',
                    'platform': 'Online Learning Platforms',
                    'type': 'both',
                    'price': 'Varies',
                    'topics': [topic.lower()],
                    'topic_match': topic
                }
            ],
            'resources': [
                {
                    'title': f'{topic.title()} Documentation',
                    'type': 'free',
                    'url': 'Official documentation',
                    'topics': [topic.lower()],
                    'topic_match': topic
                }
            ]
        }
    
    def _analyze_topic_coverage(self, topic: str, resources: Dict) -> Dict:
        """Analyze how well resources cover the topic"""
        all_resources = []
        for resource_type in resources.values():
            all_resources.extend(resource_type)
        
        if not all_resources:
            return {
                'coverage_percentage': 0,
                'covered_subtopics': [],
                'missing_subtopics': [topic],
                'recommended_combination': []
            }
        
        # Analyze subtopic coverage
        covered_subtopics = set()
        for resource in all_resources:
            covered_subtopics.update(resource.get('topics', []))
        
        # Estimate coverage
        coverage_percentage = min(100, len(covered_subtopics) * 25)  # Rough estimate
        
        return {
            'coverage_percentage': coverage_percentage,
            'covered_subtopics': list(covered_subtopics),
            'missing_subtopics': [],
            'recommended_combination': self._recommend_resource_combination(all_resources)
        }
    
    def _recommend_resource_combination(self, resources: List[Dict]) -> List[str]:
        """Recommend best combination of resources"""
        recommendations = []
        
        # Prefer free resources first, then paid
        free_resources = [r for r in resources if r['type'] == 'free']
        paid_resources = [r for r in resources if r['type'] == 'paid']
        
        if free_resources:
            recommendations.append(f"Start with: {free_resources[0]['title']}")
        
        if paid_resources:
            recommendations.append(f"For deeper learning: {paid_resources[0]['title']}")
        
        return recommendations[:3]
    
    def _suggest_alternatives(self, topic: str) -> List[str]:
        """Suggest alternative learning approaches for missing topics"""
        return [
            f"Search for '{topic}' tutorials on YouTube",
            f"Look for '{topic}' documentation and guides",
            f"Find '{topic}' practice exercises online",
            f"Join '{topic}' communities and forums"
        ]
    
    def _organize_resources(self, resources: Dict, preference: str) -> Dict:
        """Remove duplicates and organize resources"""
        # Remove duplicate books
        seen_books = set()
        unique_books = []
        for book in resources['books']:
            book_key = (book['title'], book.get('author', ''))
            if book_key not in seen_books:
                seen_books.add(book_key)
                unique_books.append(book)
        
        # Remove duplicate courses
        seen_courses = set()
        unique_courses = []
        for course in resources['courses']:
            course_key = (course['title'], course.get('platform', ''))
            if course_key not in seen_courses:
                seen_courses.add(course_key)
                unique_courses.append(course)
        
        # Separate by type
        free_resources = []
        paid_resources = []
        
        for resource in unique_books + unique_courses:
            if resource['type'] == 'free':
                free_resources.append(resource)
            else:
                paid_resources.append(resource)
        
        resources['books'] = unique_books
        resources['courses'] = unique_courses
        resources['free_resources'] = free_resources
        resources['paid_resources'] = paid_resources
        
        return resources
    
    def display_resources(self, resources: Dict):
        """Display resources in a user-friendly format"""
        print("\n" + "="*60)
        print("LEARNING RESOURCES FOUND")
        print("="*60)
        
        # Display books
        if resources['books']:
            print(f"\n📚 BOOKS ({len(resources['books'])} found):")
            print("-" * 40)
            for book in resources['books']:
                price_tag = "💰" if book['type'] == 'paid' else "🆓"
                print(f"{price_tag} {book['title']}")
                print(f"   Author: {book.get('author', 'Unknown')}")
                print(f"   Price: {book.get('price', 'Check price')}")
                print(f"   Topics: {', '.join(book.get('topics', []))}")
                print()
        
        # Display courses
        if resources['courses']:
            print(f"\n🎓 COURSES ({len(resources['courses'])} found):")
            print("-" * 40)
            for course in resources['courses']:
                price_tag = "💰" if course['type'] == 'paid' else "🆓"
                print(f"{price_tag} {course['title']}")
                print(f"   Platform: {course.get('platform', 'Unknown')}")
                print(f"   Price: {course.get('price', 'Check platform')}")
                print(f"   Topics: {', '.join(course.get('topics', []))}")
                print()
        
        # Display coverage analysis
        if resources['topic_coverage']:
            print(f"\n📊 TOPIC COVERAGE ANALYSIS:")
            print("-" * 40)
            for topic, analysis in resources['topic_coverage'].items():
                coverage = analysis.get('coverage_percentage', 0)
                print(f"• {topic}: {coverage}% covered")
                
                missing = analysis.get('missing_subtopics', [])
                if missing:
                    print(f"  Missing: {', '.join(missing)}")
        
        # Display missing topics and alternatives
        if resources['missing_topics']:
            print(f"\n⚠️  TOPICS WITH LIMITED RESOURCES:")
            print("-" * 40)
            for topic in resources['missing_topics']:
                print(f"• {topic}")
                alternatives = resources['alternatives'].get(topic, [])
                for alt in alternatives[:2]:
                    print(f"  - {alt}")
                print()
        
        # Summary
        total_free = len(resources['free_resources'])
        total_paid = len(resources['paid_resources'])
        print(f"\n📈 SUMMARY:")
        print(f"Free resources: {total_free}")
        print(f"Paid resources: {total_paid}")
        print(f"Total resources: {total_free + total_paid}")