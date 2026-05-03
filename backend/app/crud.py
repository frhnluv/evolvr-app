from supabase import create_client, Client
from fastapi import HTTPException, Path
from dotenv import load_dotenv
import os

# 1. Setup Connection
# These should be stored in your .env file for security
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(URL, KEY)

# --- USER OPERATIONS ---

def create_user(user_data: dict):
    # Verification: Ensure email is lowercase and trimmed
    user_data["email"] = user_data.get("email", "").lower().strip() 
    if not user_data["email"]:
        raise HTTPException(status_code=400, detail="Email is required")
    
    return supabase.table("User").insert(user_data).execute() 

def get_user_by_email(email: str):
    """Fetches a user by their email address[cite: 11, 12]."""
    response = supabase.table("User").select("*").eq("email", email).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]

def update_user_password(user_id: str, new_password: str):
    """Updates a user's password[cite: 13, 14]."""
    if not new_password:
        raise HTTPException(status_code=400, detail="New password cannot be empty")
    
    update_data = {
        "password": new_password,
        "updated_at": "now()" # Database will handle timestamp [cite: 18, 19]
    }
    
    return supabase.table("User").update(update_data).eq("userID", user_id).execute()

def update_user_details(user_id: str, update_data: dict):
    """Updates user details like surname and other names[cite: 7, 8, 9, 10]."""
    # Verification: Ensure email is not being updated here
    if "email" in update_data:
        raise HTTPException(status_code=400, detail="Email cannot be updated through this endpoint")
    
    update_data["updated_at"] = "now()" # Database will handle timestamp [cite: 18, 19]
    
    return supabase.table("User").update(update_data).eq("user_id", user_id).execute()

def delete_user(user_id: str):
    """Deletes a user from the database[cite: 15, 16]."""
    return supabase.table("User").delete().eq("user_id", user_id).execute()

# --- STUDENT OPERATIONS (For Grade 4 Learners) ---

def create_student(student_data: dict):
    """Creates a new student profile[cite: 21, 22]."""
    return supabase.table("Student").insert(student_data).execute()

def get_student_by_id(student_id: str):
    """Fetches a student's profile and performance[cite: 20, 23]."""
    response = supabase.table("Student").select("*").eq("student_id", student_id).execute()
    if not response.data:

        raise HTTPException(status_code=404, detail="Student not found")
    return response.data[0]

def get_all_students():
    """Retrieves all student profiles[cite: 20, 23]."""
    return supabase.table("Student").select("*").execute()

def update_student_details(student_id: str, update_data: dict):
    """Updates student details like userID or teacherID[cite: 27, 28]."""
    # Verification: Ensure performance and status are not being updated here
    if "status" in update_data:
        raise HTTPException(status_code=400, detail="Performance and status cannot be updated through this endpoint")
    
    update_data["updated_at"] = "now()" # Database will handle timestamp [cite: 18, 19]
    
    return supabase.table("Student").update(update_data).eq("student_id", student_id).execute()

def delete_student(student_id: str):
    """Deletes a student profile from the database[cite: 29, 30]."""
    return supabase.table("Student").delete().eq("student_id", student_id).execute()

# --- TEACHER OPERATIONS ---

def create_teacher(teacher_data: dict):
    """Creates a new teacher profile[cite: 32, 33]."""
    return supabase.table("Teacher").insert(teacher_data).execute()

def get_teacher_by_id(teacher_id: str):
    """Fetches a teacher's profile[cite: 31, 32]."""
    response = supabase.table("Teacher").select("*").eq("teacher_id", teacher_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return response.data[0]

def get_teacher_dashboard(teacher_id: str):
    """Fetches all students assigned to a specific teacher[cite: 29, 30]."""
    return supabase.table("Student").select("student_id, status").eq("teacher_id", teacher_id).execute()

def update_teacher_details(teacher_id: str, update_data: dict):
    """Updates teacher details like userID or schoolID[cite: 34, 35, 36, 37]."""
    update_data["updated_at"] = "now()" # Database will handle timestamp [cite: 18, 19]
    
    return supabase.table("Teacher").update(update_data).eq("teacher_id", teacher_id).execute()

def delete_teacher(teacher_id: str):
    """Deletes a teacher profile from the database[cite: 38, 39]."""
    return supabase.table("Teacher").delete().eq("teacher_id", teacher_id).execute()

# --- SCHOOL OPERATIONS ---
def create_school(school_data: dict):
    return supabase.table("School").insert(school_data).execute()

def get_school_by_id(school_id: str):
    response = supabase.table("School").select("*").eq("school_id", school_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="School not found")
    return response.data[0]

def update_school_name(school_id: str, school_name: str):
    update_data = {
        "school_name": school_name
    }
    return supabase.table("School").update(update_data).eq("student_id", school_id).execute()

def delete_school(school_id: str):
    return supabase.table("School").delete().eq("school_id", school_id).execute()

# --- QUESTION OPERATIONS ---

def get_questions_by_strand(strand_name: str):
    """Retrieves questions filtered by learning strand (e.g., Algebra)[cite: 51, 52]."""
    response = supabase.table("Question").select("*").eq("strand", strand_name).execute() 
    if not response.data:
        raise HTTPException(status_code=404, detail=f"No questions found for {strand_name}")
    return response.data

def add_new_question(question_data: dict):
    """Allows teachers to add new questions to the pool[cite: 48, 57]."""
    # Verification: Ensure all options and the answer are present [cite: 59, 60, 61, 62, 67]
    required_fields = ["question", "option_a", "option_b", "option_c", "option_d", "answer"]
    for field in required_fields:
        if not question_data.get(field):
            raise HTTPException(status_code=400, detail=f"Field '{field}' cannot be empty")
            
    return supabase.table("Question").insert(question_data).execute()

def update_question(question_id: str, update_data: dict):
    """Updates an existing question's details[cite: 49, 50]."""
    update_data["updated_at"] = "now()" # Database will handle timestamp [cite: 18, 19]
    
    return supabase.table("Question").update(update_data).eq("question_id", question_id).execute()

def delete_question(question_id: str):
    """Deletes a question from the database[cite: 53, 54]."""
    return supabase.table("Question").delete().eq("question_id", question_id).execute()

# --- LEARNING SESSION OPERATIONS ---

def create_learning_session(session_data: dict):
    return supabase.table("LearningSession").insert(session_data).execute()

def get_session_by_id(session_id: str):
    response = supabase.table("LearningSession").select("*").eq("session_id", session_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Session not found")
    return response.data[0]

def end_learning_session(session_id: str):
    return supabase.table("LearningSession").update({
        "end_time": "now()"
    }).eq("session_id", session_id).execute()

# --- STUDENT RESPONSE (ADAPTIVE) OPERATIONS ---

def create_student_response(response_data: dict):
    """Stores a student's answer to a question."""
    return supabase.table("StudentResponse").insert(response_data).execute()

def get_responses_by_session(session_id: str):
    return supabase.table("StudentResponse").select("*").eq("session_id", session_id).execute()

def get_student_history(student_id: str):
    return supabase.table("StudentResponse").select("*").eq("student_id", student_id).execute()

# --- LEARNING PROGRESS OPERATIONS ---

def upsert_learning_progress(progress_data: dict):
    """
    Inserts or updates mastery level.
    Supabase supports upsert.
    """
    return supabase.table("LearningProgress").upsert(progress_data).execute()

def get_learning_progress(student_id: str):
    return supabase.table("LearningProgress").select("*").eq("student_id", student_id).execute()

# --- HINT OPERATIONS ---

def get_hints_by_question(question_id: str):
    return supabase.table("Hint").select("*").eq("question_id", question_id).execute()

# --- HINT USAGE OPERATIONS ---
def create_hint_usage(usage_data: dict):
    return supabase.table("HintUsage").insert(usage_data).execute()

# --- ADAPTIVE DECISION OPERATIONS ---
def create_adaptive_decision(decision_data: dict):
    return supabase.table("AdaptiveDecision").insert(decision_data).execute()

def get_decisions_by_session(session_id: str):
    return supabase.table("AdaptiveDecision").select("*").eq("session_id", session_id).execute()