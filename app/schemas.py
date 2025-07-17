"""Pydantic schemas for request/response validation.

This module defines data validation schemas for API requests and responses
using Pydantic models with appropriate field constraints.
"""

from pydantic import BaseModel, Field
from uuid import UUID
from typing import List

class BlogPostCreate(BaseModel):
    """Schema for creating a new blog post.
    
    Attributes:
        title: Post title (minimum 1 character).
        content: Post content (minimum 1 character).
    """
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

class BlogPostList(BaseModel):
    """Schema for blog post list response.
    
    Attributes:
        id: Post UUID.
        title: Post title.
        num_comments: Number of comments on the post.
    """
    id: UUID
    title: str
    num_comments: int

class BlogPostResponse(BaseModel):
    """Schema for complete blog post response.
    
    Attributes:
        id: Post UUID.
        title: Post title.
        content: Post content.
        comments: List of associated comments.
    """
    id: UUID
    title: str
    content: str
    comments: List[dict]

class CommentCreate(BaseModel):
    """Schema for creating a new comment.
    
    Attributes:
        content: Comment content (minimum 1 character).
    """
    content: str = Field(..., min_length=1)

class CommentResponse(BaseModel):
    """Schema for comment response.
    
    Attributes:
        id: Comment UUID.
        content: Comment content.
    """
    id: UUID
    content: str 