"""CRUD operations for blog posts and comments.

This module provides database operations including creation, retrieval,
and caching functionality for blog posts and comments.
"""

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .models import BlogPost, Comment
from .schemas import BlogPostCreate, CommentCreate
from .cache import get_cache, set_cache, invalidate
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

async def get_posts(db: AsyncSession):
    """Retrieve all blog posts with their comment counts.
    
    Args:
        db: Database session.
        
    Returns:
        List[Row]: List of tuples containing (post_id, title, comment_count).
    """
    query = select(BlogPost.id, BlogPost.title, func.count(Comment.id).label("num_comments")) \
        .outerjoin(Comment, Comment.post_id == BlogPost.id) \
        .group_by(BlogPost.id)
    result = await db.execute(query)
    return result.all()

async def get_posts_cached(db: AsyncSession):
    """Retrieve all blog posts with caching.
    
    Args:
        db: Database session.
        
    Returns:
        List[Row]: Cached or fresh list of posts with comment counts.
    """
    key = 'posts_list'
    cached = get_cache(key)
    if cached:
        return cached
    posts = await get_posts(db)
    set_cache(key, posts)
    return posts

async def create_post(db: AsyncSession, post: BlogPostCreate):
    """Create a new blog post.
    
    Args:
        db: Database session.
        post: Blog post data to create.
        
    Returns:
        BlogPost: The created blog post instance.
        
    Raises:
        HTTPException: 400 for data integrity errors, 500 for other errors.
    """
    try:
        db_post = BlogPost(**post.model_dump())
        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        invalidate('posts_list')
        return db_post
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Data integrity error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_post(db: AsyncSession, post_id: UUID):
    """Retrieve a specific blog post with its comments.
    
    Args:
        db: Database session.
        post_id: UUID of the post to retrieve.
        
    Returns:
        BlogPost | None: The blog post with comments, or None if not found.
    """
    query = select(BlogPost).where(BlogPost.id == post_id)
    result = await db.execute(query)
    post = result.scalar_one_or_none()
    if post:
        comments_query = select(Comment).where(Comment.post_id == post_id)
        comments_result = await db.execute(comments_query)
        post.comments = comments_result.scalars().all()
    return post

async def create_comment(db: AsyncSession, post_id: UUID, comment: CommentCreate):
    """Create a new comment on a blog post.
    
    Args:
        db: Database session.
        post_id: UUID of the post to comment on.
        comment: Comment data to create.
        
    Returns:
        Comment: The created comment instance.
        
    Raises:
        HTTPException: 400 for data integrity errors, 500 for other errors.
    """
    try:
        db_comment = Comment(**comment.model_dump(), post_id=post_id)
        db.add(db_comment)
        await db.commit()
        await db.refresh(db_comment)
        invalidate('posts_list')
        return db_comment
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Data integrity error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 