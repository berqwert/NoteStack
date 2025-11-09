from datetime import datetime
from typing import Optional


class Note:
    """Note model"""
    
    def __init__(self, content: str, title: str = "", note_id: Optional[int] = None, date: Optional[str] = None):
        """
        Create a Note
        
        Args:
            content: Note content
            title: Note title
            note_id: Note ID (auto-generated if not provided)
            date: Date (current time used if not provided)
        """
        self.id = note_id
        self.title = title
        self.content = content
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> dict:
        """Convert Note to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "date": self.date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Note':
        """Create Note from dictionary"""
        return cls(
            content=data.get("content", ""),
            title=data.get("title", ""),
            note_id=data.get("id"),
            date=data.get("date")
        )
    
    def __str__(self) -> str:
        title_str = f"title='{self.title}'" if self.title else "title=''"
        return f"Note(id={self.id}, {title_str}, content={self.content[:50]}...)"
    
    def __repr__(self) -> str:
        return self.__str__()

