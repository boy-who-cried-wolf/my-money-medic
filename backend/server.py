from fastapi import FastAPI, Depends, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.security import verify_token
from app.database import init_db
from app.database.connection import test_connection
from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Set specific loggers to DEBUG
logging.getLogger("app.api.v1.endpoints.captcha").setLevel(logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

# Global variable to track database status
db_initialized = False


# Initialize FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_initialized
    # Initialize database
    try:
        logger.info("Starting application initialization...")
        db_initialized = init_db()
        if db_initialized:
            logger.info("Application started successfully with database")
        else:
            logger.warning("Application started without database initialization")
    except Exception as e:
        logger.error(f"Error during application startup: {str(e)}")
        logger.info("Application will start without database initialization")
        db_initialized = False

    yield

    # Cleanup code can go here if needed
    logger.info("Application shutdown")


app = FastAPI(
    title="Broker Matching Platform API",
    description="Backend API for Broker Matching Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Static files configuration
static_dir = Path("static")
admin_static_dir = Path("static/admin")

if static_dir.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("✅ Static files mounted at /static")
else:
    logger.warning("⚠️ Static directory not found, frontend files not served")

if admin_static_dir.exists():
    app.mount("/admin", StaticFiles(directory="static/admin"), name="admin")
    logger.info("✅ Admin static files mounted at /admin")
else:
    logger.warning("⚠️ Admin static directory not found, admin files not served")

# CORS configuration - Updated for production
origins = [
    "http://localhost:3000",  # React's default port
    "http://localhost:3001",  # React's alternative port
    "http://localhost:5173",  # Vite's default port
    "https://*.railway.app",  # Railway deployment
    "https://*.vercel.app",  # Vercel deployment
    "https://*.ondigitalocean.app",  # DigitalOcean Apps
    "https://*.herokuapp.com",  # Heroku deployment
    "https://*.render.com",  # Render deployment
]

# Add custom domain if specified
if custom_domain := os.getenv("FRONTEND_URL"):
    origins.append(custom_domain)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
# @app.get("/")
# async def root():
#     return {
#         "message": "Welcome to Broker Matching Platform API",
#         "docs_url": "/api/docs",
#         "version": "1.0.0",
#     }


# Public test endpoint for quizzes - no auth required
@app.get("/api/public-quizzes")
async def public_quizzes():
    """Public endpoint for testing - no authentication required"""
    try:
        from app.database.connection import SessionLocal
        from app.database.models.quiz import Quiz, QuizQuestion

        db = SessionLocal()
        try:
            quizzes = db.query(Quiz).all()
            result = [
                {
                    "id": str(quiz.id),
                    "title": quiz.title,
                    "description": quiz.description,
                    "category": quiz.category,
                    "created_at": quiz.created_at,
                    "question_count": db.query(QuizQuestion)
                    .filter(QuizQuestion.quiz_id == quiz.id)
                    .count(),
                }
                for quiz in quizzes
            ]
            return result
        except Exception as e:
            return {"error": str(e)}
        finally:
            db.close()
    except Exception:
        return {"message": "Service starting up"}


# Public test endpoint for getting quiz details - no auth required
@app.get("/api/public-quizzes/{quiz_id}")
async def public_quiz_details(quiz_id: str):
    """Public endpoint for viewing quiz details - no authentication required"""
    try:
        from app.database.connection import SessionLocal
        from app.database.models.quiz import Quiz, QuizQuestion

        db = SessionLocal()
        try:
            quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
            if not quiz:
                return {"error": "Quiz not found"}

            questions = (
                db.query(QuizQuestion)
                .filter(QuizQuestion.quiz_id == quiz_id)
                .order_by(QuizQuestion.order)
                .all()
            )

            return {
                "id": str(quiz.id),
                "title": quiz.title,
                "description": quiz.description,
                "category": (
                    quiz.category.value
                    if hasattr(quiz.category, "value")
                    else quiz.category
                ),
                "created_at": quiz.created_at,
                "questions": [
                    {
                        "id": str(q.id),
                        "text": q.text,
                        "question_type": (
                            q.question_type.value
                            if hasattr(q.question_type, "value")
                            else q.question_type
                        ),
                        "options": q.options,
                        "order": q.order,
                        "weight": q.weight,
                    }
                    for q in questions
                ],
            }
        except Exception as e:
            return {"error": str(e)}
        finally:
            db.close()
    except Exception:
        return {"message": "Service starting up"}


# Health check endpoint
@app.get("/api/health")
async def health_check():
    global db_initialized

    # Check database connection
    db_status = "connected" if db_initialized and test_connection() else "disconnected"

    health_data = {
        "status": "healthy",
        "service": "Broker Matching Platform API",
        "version": "1.0.0",
        "database": db_status,
        "timestamp": f"{__import__('datetime').datetime.utcnow().isoformat()}Z",
    }

    # Return 200 even if database is disconnected - app is still functional
    return health_data


# Include API router
try:
    from app.api import api_router
    
    # Mount the main API router
    app.include_router(api_router, prefix="/api")
    logger.info("✅ API router loaded successfully")
    
    # Debug: Print all registered routes
    logger.info("Registered routes:")
    for route in app.routes:
        if hasattr(route, "methods"):
            logger.info(f"  {route.methods} {route.path}")
        else:
            logger.info(f"  MOUNT {route.path}")
        
except ImportError as e:
    logger.error(f"Failed to import API router: {str(e)}")
    logger.error("Please check that all required modules are installed and paths are correct")
    raise
except Exception as e:
    logger.error(f"Error including API router: {str(e)}")
    logger.error("Stack trace:", exc_info=True)
    raise


# Test endpoint
@app.get("/api/private")
async def private_route(user_id: str = Depends(verify_token)):
    return {"message": "This is a private endpoint", "user_id": user_id}


@app.exception_handler(Exception)
async def generic_exception_handler(_, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Request: {request.method} {request.url.path}")
    logger.debug(f"Headers: {dict(request.headers)}")
    
    # Log request body for POST requests
    if request.method == "POST":
        try:
            body = await request.body()
            if body:
                logger.debug(f"Request body: {body.decode()}")
        except Exception as e:
            logger.error(f"Error reading request body: {str(e)}")
    
    response = await call_next(request)
    
    logger.debug(f"Response status: {response.status_code}")
    return response


# Catch-all route for React SPA routing - must be last
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    # If the path starts with /api, let it pass through to the API routes
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Handle admin routes first
    # if full_path.startswith("admin/"):
    #     admin_path = full_path[6:]  # Remove 'admin/' prefix
    #     admin_file = admin_static_dir / admin_path
    #     if admin_file.exists() and admin_file.is_file():
    #         return FileResponse(admin_file)
    #     # If file not found, serve admin index.html for client-side routing
    #     admin_index = admin_static_dir / "index.html"
    #     if admin_index.exists():
    #         return FileResponse(admin_index)
    #     raise HTTPException(status_code=404, detail="Admin page not found")
    
    # Handle root admin path
    if full_path.startswith("admin"):
        admin_index = admin_static_dir / "index.html"
        if admin_index.exists():
            return FileResponse(admin_index)
        raise HTTPException(status_code=404, detail="Admin page not found")
    
    # Try to serve the requested file from static directory
    static_file = static_dir / full_path
    if static_file.exists() and static_file.is_file():
        return FileResponse(static_file)
    
    # If file not found, serve index.html for client-side routing
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    
    raise HTTPException(status_code=404, detail="Not found")


# Main entry point for running the server
if __name__ == "__main__":
    import uvicorn

    # Get port from environment variable, default to 8000 for local development
    port = int(os.getenv("PORT", "8000"))

    logger.info(f"Starting server on port {port}")

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Set to False for production
        timeout_keep_alive=30,
    )
