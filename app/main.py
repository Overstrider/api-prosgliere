"""Blog API application entry point.

This module configures and creates the FastAPI application instance,
including router registration and app metadata.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Blog API",
    description="A RESTful API for managing blog posts and comments",
    version="1.0.0"
)

from .routers import posts
app.include_router(posts.router) 