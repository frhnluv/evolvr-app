# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.security import get_current_user

from api.routers import sync, users, students, teachers, questions

# Initialize FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Adaptive Learning Platform",
    version="1.0.0"
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
app.include_router(sync.router, prefix="/api/sync", tags=["Sync"])

# Example of a protected route using our security dependency
@app.get("/api/me", tags=["Auth"])
def get_my_profile(current_user = Depends(get_current_user)):
    return {
        "message": "You are authenticated!",
        "user_id": current_user.id,
        "email": current_user.email
    }