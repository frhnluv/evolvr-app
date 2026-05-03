# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.security import get_current_user

from api.routers import sync
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

app.include_router(sync.router, prefix="/api/sync", tags=["Sync"])

# Example of a protected route using our security dependency
@app.get("/api/me", tags=["Auth"])
def get_my_profile(current_user = Depends(get_current_user)):
    return {
        "message": "You are authenticated!",
        "user_id": current_user.id,
        "email": current_user.email
    }

# TODO: Include routers for sync, reports, and webhooks here in later phases
# app.include_router(sync.router, prefix="/api/sync", tags=["Sync"])







# from fastapi import FastAPI, Depends, HTTPException
# from typing import List
# from . import crud, schemas

# # Initialize the FastAPI application
# app = FastAPI(
#     title="Evolvr API",
#     description="Backend for tracking learner abilities and teacher feedback."
# )

# # --- USER ENDPOINTS ---

# @app.post("/users/", response_model=schemas.UserResponse, tags=["Users"])
# def register_user(user: schemas.UserCreate):
#     """
#     Registers a new User (Teacher or Student)[cite: 4, 14].
#     """
#     result = crud.create_user(user.model_dump())
#     if not result.data:
#         raise HTTPException(status_code=400, detail="Registration failed")
#     return result.data[0]

# @app.get("/users/{email}", response_model=schemas.UserResponse, tags=["Users"])
# def get_user(email: str):
#     """
#     Retrieves user details via email[cite: 11, 12].
#     """
#     return crud.get_user_by_email(email)

# # --- STUDENT & PROGRESS ENDPOINTS ---

# @app.post("/students/", response_model=schemas.StudentResponse, tags=["Students"])
# def add_student(student: schemas.StudentCreate):
#     """
#     Creates a new student profile linked to a user and teacher[cite: 20, 28, 30].
#     """
#     result = crud.create_student(student.model_dump())
#     return result.data[0]

# @app.get("/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"])
# def read_student_progress(student_id: str):
#     """
#     Fetches the specific student's performance and status for teacher feedback[cite: 23, 25].
#     """
#     return crud.get_student_by_id(student_id)

# @app.put("/students/{student_id}/performance", tags=["Students"])
# def update_student_score(student_id: str, score: float):
#     """
#     Updates a student's performance score (0-100) and status.
#     """
#     return crud.update_student_progress(student_id, score)

# # --- TEACHER ENDPOINTS ---

# @app.get("/teachers/{teacher_id}/class", tags=["Teachers"])
# def get_teacher_class_list(teacher_id: str):
#     """
#     Returns all students assigned to a specific teacher for the dashboard[cite: 29, 30].
#     """
#     result = crud.get_teacher_dashboard(teacher_id)
#     return result.data

# # --- QUESTION & QUIZ ENDPOINTS ---

# @app.get("/questions/strand/{strand_name}", response_model=List[schemas.QuestionResponse], tags=["Questions"])
# def get_questions_by_topic(strand_name: str):
#     """
#     Retrieves quiz questions filtered by learning strand (e.g., Numbers)[cite: 51, 52].
#     """
#     return crud.get_questions_by_strand(strand_name)

# @app.post("/questions/", response_model=schemas.QuestionResponse, tags=["Questions"])
# def create_question(question: schemas.QuestionBase):
#     """
#     Allows adding new questions to the database[cite: 48, 57].
#     """
#     result = crud.add_new_question(question.model_dump())
#     return result.data[0]