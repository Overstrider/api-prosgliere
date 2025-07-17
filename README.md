# BlogTest API

A production-ready RESTful API for a blogging platform built with Python 3.13, FastAPI (async), SQLAlchemy, PostgreSQL, Docker, and Nginx load balancing.

## 🚀 Features
- **Models**: BlogPost (title, content), Comment (content, linked to post)
- **Endpoints**: 
  - `GET /api/posts/` - List posts with comment counts
  - `POST /api/posts/` - Create new post
  - `GET /api/posts/{id}` - Get specific post with comments
  - `POST /api/posts/{id}/comments` - Add comment to post
- **Tech Stack**: Python 3.13, FastAPI async, SQLAlchemy with abstraction layer, Alembic migrations
- **Performance**: In-memory caching, load balancer with 2 API instances
- **Database**: PostgreSQL with automatic migrations
- **Architecture**: Docker containers with Nginx load balancer
- **Error Handling**: Comprehensive 404, 400, 500 error responses

## 📋 Prerequisites
- Docker and Docker Compose installed
- No local Python installation required - everything runs in containers

## 🏃 Running the API

### Start the API Services
```bash
# Start all services (database, 2 API instances, load balancer)
docker compose up -d

# Check if services are running
docker compose ps

# View logs
docker compose logs -f
```

### API Access
- **Main API**: http://localhost:8080/api/posts/
- **Health Check**: Access the API to verify it's working
- **Load Balancer**: Automatically distributes requests between 2 API instances

### Stop Services
```bash
# Stop all services
docker compose down

# Stop and remove volumes (reset database)
docker compose down -v
```

## API Usage Examples

### 1. List all posts
```bash
curl --location --request GET 'http://localhost:8080/api/posts/'
```

### 2. Create a new post
```bash
curl --location --request POST 'http://localhost:8080/api/posts/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "My Amazing Post",
    "content": "This is the content of my amazing blog post!"
}'
```

### 3. Get a specific post (replace with actual post ID)
```bash
curl --location --request GET 'http://localhost:8080/api/posts/2dca0ff1-b3ce-4908-bcd2-cce826873298'
```

### 4. Add a comment to a post (replace with actual post ID)
```bash
curl --location --request POST 'http://localhost:8080/api/posts/2dca0ff1-b3ce-4908-bcd2-cce826873298/comments' \
--header 'Content-Type: application/json' \
--data-raw '{
    "content": "Great post! Really enjoyed reading it."
}'
```

## 🔧 Technical Details

### Architecture
- **Load Balancer**: Nginx distributing requests between 2 FastAPI instances
- **Database**: PostgreSQL with automatic migrations via Alembic
- **Caching**: Simple in-memory cache per instance (not shared)
- **Network**: Docker bridge network for container communication
- **Resource Limits**: Optimized for 1.5 vCPU, 3GB RAM total

### Configuration
- **Database**: PostgreSQL max 30 connections
- **Nginx**: Max 256 connections
- **Environment**: Configurable via environment variables

## 📁 Project Structure
```
blogtest/
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── cache.py         # Simple caching
│   ├── database.py      # Database connection
│   └── routers/
│       └── posts.py     # API endpoints
├── alembic/             # Database migrations
├── nginx/
│   └── nginx.conf       # Load balancer config
├── docker-compose.yml   # Main services
└── README.md           # This file
``` 