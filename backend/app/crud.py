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
        "updatedAt": "now()" # Database will handle timestamp [cite: 18, 19]
    }
    
    return supabase.table("User").update(update_data).eq("userID", user_id).execute()

def update_user_details(user_id: str, update_data: dict):
    """Updates user details like surname and other names[cite: 7, 8, 9, 10]."""
    # Verification: Ensure email is not being updated here
    if "email" in update_data:
        raise HTTPException(status_code=400, detail="Email cannot be updated through this endpoint")
    
    update_data["updatedAt"] = "now()" # Database will handle timestamp [cite: 18, 19]
    
    return supabase.table("User").update(update_data).eq("userID", user_id).execute()

def delete_user(user_id: str):
    """Deletes a user from the database[cite: 15, 16]."""
    return supabase.table("User").delete().eq("userID", user_id).execute()

# --- STUDENT OPERATIONS (For Grade 4 Learners) ---

def create_student(student_data: dict):
    """Creates a new student profile[cite: 21, 22]."""
    return supabase.table("Student").insert(student_data).execute()

def get_student_by_id(student_id: str):
    """Fetches a student's profile and performance[cite: 20, 23]."""
    response = supabase.table("Student").select("*").eq("studentID", student_id).execute()
    if not response.data:

        raise HTTPException(status_code=404, detail="Student not found")
    return response.data[0]

def get_all_students():
    """Retrieves all student profiles[cite: 20, 23]."""
    return supabase.table("Student").select("*").execute()

def update_student_progress(student_id: str, score: float):
    """Updates performance and sets status based on grade[cite: 23, 24, 25]."""
    # Verification: Logic check for the score
    if not (0 <= score <= 100):
        raise HTTPException(status_code=400, detail="Performance score must be between 0 and 100")
    
    # Simple logic to determine status [cite: 25, 26]
    status = "Exceeding Expectations" if score >= 80 else "Developing"
    
    update_data = {
        "performance": score,
        "status": status,
        "updatedAt": "now()" # Database will handle timestamp [cite: 18, 19]
    }
    
    return supabase.table("Student").update(update_data).eq("studentID", student_id).execute()

def update_student_details(student_id: str, update_data: dict):
    """Updates student details like userID or teacherID[cite: 27, 28]."""
    # Verification: Ensure performance and status are not being updated here
    if "performance" in update_data or "status" in update_data:
        raise HTTPException(status_code=400, detail="Performance and status cannot be updated through this endpoint")
    
    update_data["updatedAt"] = "now()" # Database will handle timestamp [cite: 18, 19]
    
    return supabase.table("Student").update(update_data).eq("studentID", student_id).execute()

def delete_student(student_id: str):
    """Deletes a student profile from the database[cite: 29, 30]."""
    return supabase.table("Student").delete().eq("studentID", student_id).execute()

# --- TEACHER OPERATIONS ---

def create_teacher(teacher_data: dict):
    """Creates a new teacher profile[cite: 32, 33]."""
    return supabase.table("Teacher").insert(teacher_data).execute()

def get_teacher_by_id(teacher_id: str):
    """Fetches a teacher's profile[cite: 31, 32]."""
    response = supabase.table("Teacher").select("*").eq("teacherID", teacher_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return response.data[0]

def get_teacher_dashboard(teacher_id: str):
    """Fetches all students assigned to a specific teacher[cite: 29, 30]."""
    return supabase.table("Student").select("studentID, performance, status").eq("teacherID", teacher_id).execute()

def update_teacher_details(teacher_id: str, update_data: dict):
    """Updates teacher details like userID or schoolID[cite: 34, 35, 36, 37]."""
    update_data["updatedAt"] = "now()" # Database will handle timestamp [cite: 18, 19]
    
    return supabase.table("Teacher").update(update_data).eq("teacherID", teacher_id).execute()

def delete_teacher(teacher_id: str):
    """Deletes a teacher profile from the database[cite: 38, 39]."""
    return supabase.table("Teacher").delete().eq("teacherID", teacher_id).execute()

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
    required_fields = ["question", "optionA", "optionB", "optionC", "optionD", "answer"]
    for field in required_fields:
        if not question_data.get(field):
            raise HTTPException(status_code=400, detail=f"Field '{field}' cannot be empty")
            
    return supabase.table("Question").insert(question_data).execute()

def update_question(question_id: str, update_data: dict):
    """Updates an existing question's details[cite: 49, 50]."""
    update_data["updatedAt"] = "now()" # Database will handle timestamp [cite: 18, 19]
    
    return supabase.table("Question").update(update_data).eq("questionID", question_id).execute()

def delete_question(question_id: str):
    """Deletes a question from the database[cite: 53, 54]."""
    return supabase.table("Question").delete().eq("questionID", question_id).execute()