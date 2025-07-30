#!/usr/bin/env python3

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_client import AIClient
from src.notes_generator import NotesGenerator

async def demo_study_materials():
    print("=" * 60)
    print("           STUDY MATERIALS GENERATOR DEMO")
    print("=" * 60)
    
    # Initialize AI client and notes generator
    ai_client = AIClient()
    notes_generator = NotesGenerator(ai_client)
    
    # Sample video data
    sample_video = {
        'id': 'sample123',
        'title': 'Machine Learning Fundamentals - Complete Tutorial',
        'channel': 'AI Education',
        'description': 'Learn the basics of machine learning including supervised learning, unsupervised learning, and neural networks.'
    }
    
    sample_transcript = """
    Welcome to this machine learning tutorial. Today we'll cover the fundamentals of machine learning.
    Machine learning is a subset of artificial intelligence that enables computers to learn from data.
    There are three main types: supervised learning, unsupervised learning, and reinforcement learning.
    Supervised learning uses labeled data to train models. Common algorithms include linear regression and decision trees.
    Unsupervised learning finds patterns in data without labels. Examples include clustering and dimensionality reduction.
    """
    
    topic = "Machine Learning Fundamentals"
    
    print(f"Generating study materials for: {topic}")
    print(f"Based on video: {sample_video['title']}")
    print("-" * 60)
    
    try:
        # Generate study materials
        study_materials = await notes_generator.generate_study_notes(
            topic, sample_video, sample_transcript
        )
        
        # Display results
        print("\nSTUDY NOTES:")
        print("-" * 30)
        for i, note in enumerate(study_materials.get('notes', []), 1):
            print(f"{i}. {note}")
        
        print("\nPRACTICE QUESTIONS:")
        print("-" * 30)
        for i, question in enumerate(study_materials.get('questions', []), 1):
            print(f"{i}. {question}")
        
        print("\nKEY CONCEPTS:")
        print("-" * 30)
        for concept in study_materials.get('key_concepts', []):
            print(f"• {concept}")
        
        print("\nSTUDY TIPS:")
        print("-" * 30)
        for tip in study_materials.get('study_tips', []):
            print(f"→ {tip}")
        
        print("\n" + "=" * 60)
        print("Study materials generated successfully!")
        print("This demonstrates how AI creates personalized learning content.")
        
    except Exception as e:
        print(f"Error generating study materials: {e}")

if __name__ == "__main__":
    asyncio.run(demo_study_materials())