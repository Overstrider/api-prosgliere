from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.schemas import BlogPostCreate, BlogPostResponse, BlogPostList, CommentCreate, CommentResponse
from app.crud import get_posts_cached, create_post, get_post, create_comment
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Main router
router = APIRouter(prefix="/api/posts")

@router.get("/", response_model=List[BlogPostList])
async def list_posts(db: AsyncSession = Depends(get_db)):
    """List all blog posts with comment counts.
    
    Args:
        db: Database session dependency.
        
    Returns:
        List[BlogPostList]: List of posts with ID, title, and comment count.
    """
    posts = await get_posts_cached(db)
    return [{"id": p[0], "title": p[1], "num_comments": p[2]} for p in posts]

@router.post("/", response_model=BlogPostResponse)
async def create_blog_post(post: BlogPostCreate, db: AsyncSession = Depends(get_db)):
    """Create a new blog post.
    
    Args:
        post: Blog post data to create.
        db: Database session dependency.
        
    Returns:
        BlogPostResponse: Created post with ID, title, content, and empty comments.
    """
    new_post = await create_post(db, post)
    return {"id": new_post.id, "title": new_post.title, "content": new_post.content, "comments": []}

@router.get("/{id}", response_model=BlogPostResponse)
async def get_blog_post(id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific blog post by ID.
    
    Args:
        id: UUID of the blog post to retrieve.
        db: Database session dependency.
        
    Returns:
        BlogPostResponse: Complete post data with all comments.
        
    Raises:
        HTTPException: 404 if post not found.
    """
    post = await get_post(db, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "comments": [{"id": c.id, "content": c.content} for c in post.comments]
    }

@router.post("/{id}/comments", response_model=CommentResponse)
async def add_comment(id: UUID, comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    """Add a comment to an existing blog post.
    
    Args:
        id: UUID of the blog post to comment on.
        comment: Comment data to create.
        db: Database session dependency.
        
    Returns:
        CommentResponse: Created comment with ID and content.
        
    Raises:
        HTTPException: 404 if post not found.
    """
    post = await get_post(db, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = await create_comment(db, id, comment)
    return {"id": new_comment.id, "content": new_comment.content} 