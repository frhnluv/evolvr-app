from fastapi import HTTPException
from core.database import supabase
from typing import List, Dict

def get_student_mastery_dashboard(student_id: str):
    # Fetch student
    student_res = supabase.table("Student").select("*, User(surname, other_names)").eq("student_id", student_id).execute()
    if not student_res.data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student = student_res.data[0]
    user_data = student.get("User", {})
    student_name = f"{user_data.get('other_names', '')} {user_data.get('surname', '')}".strip() or "Unknown Student"

    # Fetch progress
    progress_res = supabase.table("LearningProgress").select("*").eq("student_id", student_id).execute()
    records = []
    at_risk = False
    
    for p in progress_res.data:
        mastery = p.get("mastery_level", 0.0)
        records.append({
            "standard_id": p["progress_id"], # using progress_id as standard_id placeholder
            "standard_code": f"{p.get('strand')}-{p.get('sub_strand')}",
            "mastery_level": mastery,
            "last_updated": p.get("updated_at", p.get("last_updated"))
        })
        if mastery < 30.0:
            at_risk = True

    return {
        "student_id": student_id,
        "student_name": student_name,
        "mastery_records": records,
        "at_risk": at_risk
    }

def get_class_report(teacher_id: str, class_id: str):
    # Fetch all students for teacher
    students_res = supabase.table("Student").select("student_id").eq("teacher_id", teacher_id).execute()
    
    student_dashboards = []
    for s in students_res.data:
        try:
            dashboard = get_student_mastery_dashboard(s["student_id"])
            student_dashboards.append(dashboard)
        except Exception:
            continue
            
    return {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "students": student_dashboards
    }

def get_session_analytics(session_id: str):
    # Calculate simple analytics for a session
    responses = supabase.table("StudentResponse").select("*").eq("session_id", session_id).execute()
    total_questions = len(responses.data)
    if total_questions == 0:
        return {"session_id": session_id, "accuracy": 0, "total_questions": 0}
        
    correct_answers = sum(1 for r in responses.data if r.get("is_correct"))
    accuracy = (correct_answers / total_questions) * 100
    
    return {
        "session_id": session_id,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "accuracy": round(accuracy, 2)
    }
