#!/usr/bin/env python3
"""
Enhanced Video Search System
Provides comprehensive, non-repetitive video results with proper topic coverage
"""

import asyncio
from typing import List, Dict, Set, Optional
from collections import defaultdict
import re
from .youtube_client import YouTubeClient
from .logger import SyllaboLogger

class EnhancedVideoSearch:
    """Enhanced video search with topic coverage and deduplication"""
    
    def __init__(self):
        self.youtube_client = YouTubeClient()
        self.logger = SyllaboLogger("enhanced_video_search")
        
    async def comprehensive_topic_search(self, syllabus_text: str, max_videos_per_topic: int = 5) -> Dict:
        """
        Perform comprehensive search covering all syllabus topics
        Returns organized, non-repetitive results
        """
        # Extract individual topics from syllabus
        topics = self._extract_individual_topics(syllabus_text)
        
        self.logger.info(f"Extracted {len(topics)} topics from syllabus")
        
        # Search for videos for each topic
        all_results = {}
        seen_videos = set()  # Track video IDs to avoid duplicates
        
        for topic in topics:
            topic_videos = await self._search_topic_with_variations(topic, max_videos_per_topic)
            
            # Filter out duplicates
            unique_videos = []
            for video in topic_videos:
                video_id = video.get('id', '')
                if video_id and video_id not in seen_videos:
                    seen_videos.add(video_id)
                    unique_videos.append(video)
            
            if unique_videos:
                all_results[topic] = unique_videos
        
        # Organize and rank results
        organized_results = self._organize_and_rank_results(all_results, syllabus_text)
        
        return organized_results
    
    def _extract_individual_topics(self, syllabus_text: str) -> List[str]:
        """Extract individual mathematical topics from syllabus text"""
        # Common mathematical topic patterns
        topics = []
        
        # Split by common delimiters
        parts = re.split(r'[,;.]', syllabus_text)
        
        for part in parts:
            part = part.strip()
            if len(part) > 5:  # Ignore very short parts
                # Clean up the topic
                topic = self._clean_topic_name(part)
                if topic:
                    topics.append(topic)
        
        # Add some specific searches for comprehensive coverage
        additional_topics = self._generate_additional_searches(syllabus_text)
        topics.extend(additional_topics)
        
        return list(set(topics))  # Remove duplicates
    
    def _clean_topic_name(self, topic: str) -> str:
        """Clean and normalize topic names for better search"""
        # Remove common prefixes/suffixes
        topic = re.sub(r'^(and|or|the|a|an)\s+', '', topic, flags=re.IGNORECASE)
        topic = re.sub(r'\s+(and|or|the|a|an)$', '', topic, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        topic = ' '.join(topic.split())
        
        return topic if len(topic) > 3 else ''
    
    def _generate_additional_searches(self, syllabus_text: str) -> List[str]:
        """Generate additional specific searches based on syllabus content"""
        additional = []
        
        # Check for specific mathematical concepts
        concept_map = {
            'leibnitz': ['Leibnitz theorem', 'Leibniz rule differentiation'],
            'taylor': ['Taylor series', 'Taylor expansion', 'Taylor theorem'],
            'maclaurin': ['Maclaurin series', 'Maclaurin expansion'],
            'mean value': ['Mean value theorem', 'Rolle theorem', 'Lagrange mean value'],
            'successive differentiation': ['nth derivative', 'higher order derivatives'],
            'extrema': ['maxima minima', 'critical points', 'optimization'],
            'concavity': ['concave convex functions', 'second derivative test'],
            'inflection': ['inflection points', 'point of inflection']
        }
        
        syllabus_lower = syllabus_text.lower()
        
        for key, searches in concept_map.items():
            if key in syllabus_lower:
                additional.extend(searches)
        
        return additional
    
    async def _search_topic_with_variations(self, topic: str, max_results: int) -> List[Dict]:
        """Search for a topic with multiple query variations"""
        search_variations = self._generate_search_variations(topic)
        
        all_videos = []
        
        for variation in search_variations[:3]:  # Limit to 3 variations per topic
            try:
                videos = await self.youtube_client.search_videos(variation, max_results=max_results)
                
                # Add topic context to each video
                for video in videos:
                    video['search_topic'] = topic
                    video['search_query'] = variation
                
                all_videos.extend(videos)
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                self.logger.error(f"Error searching for '{variation}': {e}")
        
        return all_videos
    
    def _generate_search_variations(self, topic: str) -> List[str]:
        """Generate different search query variations for better coverage"""
        variations = [topic]
        
        # Add educational context
        educational_contexts = [
            f"{topic} tutorial",
            f"{topic} explained",
            f"{topic} calculus",
            f"{topic} mathematics",
            f"{topic} engineering math"
        ]
        
        variations.extend(educational_contexts)
        
        # Add specific mathematical contexts
        if any(word in topic.lower() for word in ['theorem', 'rule', 'law']):
            variations.append(f"{topic} proof")
            variations.append(f"{topic} examples")
        
        if any(word in topic.lower() for word in ['differentiation', 'derivative']):
            variations.append(f"{topic} problems")
            variations.append(f"{topic} solved examples")
        
        return variations
    
    def _organize_and_rank_results(self, topic_results: Dict, syllabus_text: str) -> Dict:
        """Organize and rank results by relevance and quality"""
        
        # Group videos by channel to identify repetitive content
        channel_groups = defaultdict(list)
        all_videos = []
        
        for topic, videos in topic_results.items():
            for video in videos:
                channel = video.get('channel', 'Unknown')
                channel_groups[channel].append({**video, 'topic': topic})
                all_videos.append({**video, 'topic': topic})
        
        # Rank and select best videos from each channel
        selected_videos = self._select_best_from_channels(channel_groups)
        
        # Organize by topic coverage
        topic_coverage = self._analyze_topic_coverage(selected_videos, syllabus_text)
        
        # Create final organized structure
        organized = {
            'comprehensive_videos': selected_videos[:15],  # Top 15 overall
            'topic_coverage': topic_coverage,
            'channel_diversity': self._calculate_channel_diversity(selected_videos),
            'missing_topics': self._identify_missing_topics(topic_coverage, syllabus_text),
            'recommended_study_order': self._create_study_order(selected_videos, syllabus_text)
        }
        
        return organized
    
    def _select_best_from_channels(self, channel_groups: Dict) -> List[Dict]:
        """Select best videos from each channel to avoid repetition"""
        selected = []
        
        for channel, videos in channel_groups.items():
            # Sort videos by quality indicators
            sorted_videos = sorted(videos, key=lambda v: (
                v.get('view_count', 0),
                -len(v.get('title', '')),  # Prefer shorter, more focused titles
                v.get('like_count', 0)
            ), reverse=True)
            
            # Take top 2 videos per channel to maintain diversity
            channel_limit = 3 if len(videos) > 5 else 2
            selected.extend(sorted_videos[:channel_limit])
        
        # Sort all selected videos by overall quality
        return sorted(selected, key=lambda v: (
            v.get('view_count', 0) * 0.4 +
            v.get('like_count', 0) * 0.3 +
            len(v.get('description', '')) * 0.1 +
            (1000000 if 'tutorial' in v.get('title', '').lower() else 0) * 0.2
        ), reverse=True)
    
    def _analyze_topic_coverage(self, videos: List[Dict], syllabus_text: str) -> Dict:
        """Analyze how well the videos cover the syllabus topics"""
        syllabus_keywords = self._extract_keywords(syllabus_text)
        
        coverage = {}
        for keyword in syllabus_keywords:
            matching_videos = []
            for video in videos:
                title_desc = f"{video.get('title', '')} {video.get('description', '')}".lower()
                if keyword.lower() in title_desc:
                    matching_videos.append(video)
            
            coverage[keyword] = {
                'video_count': len(matching_videos),
                'videos': matching_videos[:3],  # Top 3 videos for this topic
                'coverage_quality': self._assess_coverage_quality(matching_videos, keyword)
            }
        
        return coverage
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract key mathematical terms from syllabus"""
        # Mathematical terms to look for
        math_terms = [
            'differentiation', 'derivative', 'leibnitz', 'leibniz',
            'mean value theorem', 'taylor', 'maclaurin', 'expansion',
            'increasing', 'decreasing', 'concavity', 'convexity',
            'inflection', 'extrema', 'maxima', 'minima', 'critical points'
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in math_terms:
            if term in text_lower:
                found_terms.append(term)
        
        # Also extract terms from the original text
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
        mathematical_words = [w for w in words if w.lower() in [
            'theorem', 'expansion', 'function', 'derivative', 'calculus',
            'mathematics', 'analysis', 'optimization'
        ]]
        
        found_terms.extend(mathematical_words)
        
        return list(set(found_terms))
    
    def _assess_coverage_quality(self, videos: List[Dict], topic: str) -> str:
        """Assess the quality of coverage for a topic"""
        if not videos:
            return 'No coverage'
        
        total_views = sum(v.get('view_count', 0) for v in videos)
        avg_views = total_views / len(videos)
        
        if len(videos) >= 3 and avg_views > 100000:
            return 'Excellent'
        elif len(videos) >= 2 and avg_views > 50000:
            return 'Good'
        elif len(videos) >= 1 and avg_views > 10000:
            return 'Fair'
        else:
            return 'Limited'
    
    def _calculate_channel_diversity(self, videos: List[Dict]) -> Dict:
        """Calculate diversity of channels in results"""
        channels = [v.get('channel', 'Unknown') for v in videos]
        channel_counts = defaultdict(int)
        
        for channel in channels:
            channel_counts[channel] += 1
        
        return {
            'total_channels': len(channel_counts),
            'channel_distribution': dict(channel_counts),
            'diversity_score': len(channel_counts) / len(videos) if videos else 0
        }
    
    def _identify_missing_topics(self, coverage: Dict, syllabus_text: str) -> List[str]:
        """Identify topics that are poorly covered"""
        missing = []
        
        for topic, info in coverage.items():
            if info['coverage_quality'] in ['No coverage', 'Limited']:
                missing.append(topic)
        
        return missing
    
    def _create_study_order(self, videos: List[Dict], syllabus_text: str) -> List[Dict]:
        """Create recommended study order based on topic dependencies"""
        
        # Define topic dependencies (what should be learned first)
        dependencies = {
            'differentiation': 0,  # Foundation
            'successive differentiation': 1,
            'leibnitz': 2,
            'mean value theorem': 3,
            'taylor': 4,
            'maclaurin': 4,
            'extrema': 5,
            'concavity': 6,
            'inflection': 6
        }
        
        # Assign priority to videos based on their topics
        for video in videos:
            title_lower = video.get('title', '').lower()
            priority = 10  # Default priority
            
            for topic, dep_level in dependencies.items():
                if topic in title_lower:
                    priority = min(priority, dep_level)
            
            video['study_priority'] = priority
        
        # Sort by priority, then by quality
        ordered = sorted(videos, key=lambda v: (
            v.get('study_priority', 10),
            -v.get('view_count', 0)
        ))
        
        return ordered[:10]  # Top 10 in recommended order