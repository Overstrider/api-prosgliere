"""SQLAlchemy database models.

This module defines the database schema for blog posts and comments
using SQLAlchemy ORM with PostgreSQL UUID support.
"""

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import uuid

class BlogPost(Base):
    """Blog post model.
    
    Attributes:
        id: Primary key UUID.
        title: Post title (required).
        content: Post content (required).
    """
    __tablename__ = "blog_posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

class Comment(Base):
    """Comment model.
    
    Attributes:
        id: Primary key UUID.
        content: Comment content (required).
        post_id: Foreign key reference to blog post.
    """
    __tablename__ = "comments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("blog_posts.id"), nullable=False) 