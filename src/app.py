from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, TextArea, Static, DataTable
from textual.screen import Screen
from rich.text import Text

from .syllabus_parser import SyllabusParser
from .youtube_client import YouTubeClient
from .ai_client import AIClient
from .video_analyzer import VideoAnalyzer
from .utils import truncate_text
import csv
import os
from datetime import datetime

class MainScreen(Screen):
    def __init__(self):
        super().__init__()
        self.auto_load_input = None
        self.is_file_input = False
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Vertical(
                Static("Syllabo - YouTube Video Finder", classes="title"),
                TextArea(id="syllabus_input"),
                Horizontal(
                    Button("Parse Syllabus", id="parse_btn", variant="primary"),
                    Button("Load from File", id="load_btn"),
                    classes="buttons"
                ),
                DataTable(id="topics_table"),
                Horizontal(
                    Button("Search Videos", id="search_btn", variant="success"),
                    Button("Export Results", id="export_btn"),
                    classes="buttons"
                ),
                DataTable(id="results_table"),
                classes="main_container"
            )
        )
        yield Footer()

    def on_mount(self):
        topics_table = self.query_one("#topics_table", DataTable)
        topics_table.add_columns("Topic", "Subtopics")
        
        results_table = self.query_one("#results_table", DataTable)
        results_table.add_columns("Topic", "Video Title", "Channel", "Relevance", "Duration")
        
        if self.auto_load_input:
            if self.is_file_input:
                parser = SyllabusParser()
                text = parser.load_from_file(self.auto_load_input)
            else:
                text = self.auto_load_input
            
            syllabus_input = self.query_one("#syllabus_input", TextArea)
            syllabus_input.text = text

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "parse_btn":
            await self.parse_syllabus()
        elif event.button.id == "search_btn":
            await self.search_videos()
        elif event.button.id == "export_btn":
            await self.export_results()

    async def parse_syllabus(self):
        syllabus_text = self.query_one("#syllabus_input", TextArea).text
        if not syllabus_text.strip():
            return
        
        parser = SyllabusParser()
        ai_client = AIClient()
        
        topics = await parser.extract_topics(syllabus_text, ai_client)
        
        topics_table = self.query_one("#topics_table", DataTable)
        topics_table.clear()
        
        for topic in topics:
            subtopics_str = ", ".join(topic.get("subtopics", []))
            topics_table.add_row(topic["name"], subtopics_str)

    async def search_videos(self):
        youtube_client = YouTubeClient()
        ai_client = AIClient()
        analyzer = VideoAnalyzer(ai_client)
        
        topics_table = self.query_one("#topics_table", DataTable)
        results_table = self.query_one("#results_table", DataTable)
        results_table.clear()
        
        for row_key in topics_table.rows:
            row = topics_table.get_row(row_key)
            topic_name = str(row[0])
            
            videos = await youtube_client.search_videos(topic_name)
            analyzed_videos = await analyzer.analyze_videos(videos, topic_name)
            
            for video in analyzed_videos[:3]:
                results_table.add_row(
                    topic_name,
                    truncate_text(video["title"]),
                    truncate_text(video["channel"], 20),
                    f"{video['relevance_score']:.1f}/10",
                    video["duration"]
                )

    async def export_results(self):
        results_table = self.query_one("#results_table", DataTable)
        if not results_table.rows:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"syllabo_results_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topic", "Video Title", "Channel", "Relevance", "Duration"])
            
            for row_key in results_table.rows:
                row = results_table.get_row(row_key)
                writer.writerow([str(cell) for cell in row])

class SyllaboApp(App):
    CSS_PATH = "styles.css"
    
    def __init__(self):
        super().__init__()
        self.cli_mode = False
        self.cli_input = None
        self.is_file = False
    
    def on_mount(self):
        screen = MainScreen()
        if self.cli_mode:
            screen.auto_load_input = self.cli_input
            screen.is_file_input = self.is_file
        self.push_screen(screen)