# main.py
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from core.config import settings
from core.security import get_current_user

from api.routers import (
    sync, users, students, teachers, questions,
    schools, lesson_sessions, responses,
    student_mastery, hints, reports, webhooks
)
# Initialize FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Adaptive Learning Platform",
    version="1.0.0"
)

# Setup basic structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("evolvr-backend")

# Global Exception Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Please try again later."},
    )

# Configure CORS for web portal access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific dashboard domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic Health Check
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "online",
        "system": settings.PROJECT_NAME
    }

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(teachers.router, prefix="/api/teachers", tags=["Teachers"])
app.include_router(questions.router, prefix="/api/questions", tags=["Questions"])
app.include_router(schools.router, prefix="/api/schools", tags=["Schools"])
app.include_router(lesson_sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(responses.router, prefix="/api/responses", tags=["Responses"])
app.include_router(student_mastery.router, prefix="/api/mastery", tags=["Mastery"])
app.include_router(hints.router, prefix="/api/hints", tags=["Hints"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(sync.router, prefix="/api/sync", tags=["Sync"])

# Example of a protected route using our security dependency
@app.get("/api/me", tags=["Auth"])
def get_my_profile(current_user = Depends(get_current_user)):
    return {
        "message": "You are authenticated!",
        "user_id": current_user.id,
        "email": current_user.email
    }