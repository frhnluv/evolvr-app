from fastapi import FastAPI, Depends, HTTPException
from typing import List
from . import crud, schemas

# Initialize the FastAPI application
app = FastAPI(
    title="Evolvr API",
    description="Backend for tracking learner abilities and teacher feedback."
)

# --- USER ENDPOINTS ---

@app.post("/users/", response_model=schemas.UserResponse, tags=["Users"])
def register_user(user: schemas.UserCreate):
    """
    Registers a new User (Teacher or Student)[cite: 4, 14].
    """
    result = crud.create_user(user.model_dump())
    if not result.data:
        raise HTTPException(status_code=400, detail="Registration failed")
    return result.data[0]

@app.get("/users/{email}", response_model=schemas.UserResponse, tags=["Users"])
def get_user(email: str):
    """
    Retrieves user details via email[cite: 11, 12].
    """
    return crud.get_user_by_email(email)

# --- STUDENT & PROGRESS ENDPOINTS ---

@app.post("/students/", response_model=schemas.StudentResponse, tags=["Students"])
def add_student(student: schemas.StudentCreate):
    """
    Creates a new student profile linked to a user and teacher[cite: 20, 28, 30].
    """
    result = crud.create_student(student.model_dump())
    return result.data[0]

@app.get("/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"])
def read_student_progress(student_id: str):
    """
    Fetches the specific student's performance and status for teacher feedback[cite: 23, 25].
    """
    return crud.get_student_by_id(student_id)

@app.get("/students/{student_id}/progress", tags=["Adaptive"])
def get_student_progress(student_id: str):
    result = crud.get_learning_progress(student_id)
    return result.data

# --- TEACHER ENDPOINTS ---

@app.get("/teachers/{teacher_id}/class", tags=["Teachers"])
def get_teacher_class_list(teacher_id: str):
    """
    Returns all students assigned to a specific teacher for the dashboard[cite: 29, 30].
    """
    result = crud.get_teacher_dashboard(teacher_id)
    return result.data

# --- QUESTION & QUIZ ENDPOINTS ---

@app.get("/questions/strand/{strand_name}", response_model=List[schemas.QuestionResponse], tags=["Questions"])
def get_questions_by_topic(strand_name: str):
    """
    Retrieves quiz questions filtered by learning strand (e.g., Numbers)[cite: 51, 52].
    """
    return crud.get_questions_by_strand(strand_name)

@app.post("/questions/", response_model=schemas.QuestionResponse, tags=["Questions"])
def create_question(question: schemas.QuestionBase):
    """
    Allows adding new questions to the database[cite: 48, 57].
    """
    result = crud.add_new_question(question.model_dump())
    return result.data[0]

# --- LEARNING SESSION ENDPOINTS ---

@app.post("/sessions/", response_model=schemas.LearningSessionResponse, tags=["Adaptive"])
def start_session(session: schemas.LearningSessionCreate):
    result = crud.create_learning_session(session.model_dump())
    return result.data[0]

@app.put("/sessions/{session_id}/end", tags=["Adaptive"])
def end_session(session_id: str):
    return crud.end_learning_session(session_id)

# --- STUDENT RESPONSE ENDPOINTS ---

@app.post("/responses/", response_model=schemas.StudentResponseResponse, tags=["Adaptive"])
def submit_response(response: schemas.StudentResponseCreate):
    result = crud.create_student_response(response.model_dump())
    return result.data[0]

@app.get("/sessions/{session_id}/responses", tags=["Adaptive"])
def get_session_responses(session_id: str):
    result = crud.get_responses_by_session(session_id)
    return result.data

# --- LEARNING PROGRESS ENDPOINTS ---

@app.get("/students/{student_id}/progress", tags=["Adaptive"])
def get_progress(student_id: str):
    result = crud.get_learning_progress(student_id)
    return result.data

# --- HINT ENDPOINTS ---

@app.get("/questions/{question_id}/hints", tags=["Hints"])
def get_hints(question_id: str):
    result = crud.get_hints_by_question(question_id)
    return result.data

# --- HINT USAGE ENDPOINT ---

@app.post("/hint-usage/", response_model=schemas.HintUsageResponse, tags=["Hints"])
def use_hint(usage: schemas.HintUsageCreate):
    result = crud.create_hint_usage(usage.model_dump())
    return result.data[0]

# --- ADAPTIVE DECISION ENDPOINTS ---

@app.post("/decisions/", response_model=schemas.AdaptiveDecisionResponse, tags=["Adaptive"])
def log_decision(decision: schemas.AdaptiveDecisionCreate):
    result = crud.create_adaptive_decision(decision.model_dump())
    return result.data[0]

@app.get("/sessions/{session_id}/decisions", tags=["Adaptive"])
def get_session_decisions(session_id: str):
    result = crud.get_decisions_by_session(session_id)
    return result.data