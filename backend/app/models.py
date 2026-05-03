from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# --- User Entity ---
class User(SQLModel, table=True):
    user_id: str = Field(primary_key=True, unique=True, index=True) 
    surname: str = Field(max_length=30) 
    other_names: str = Field(max_length=70) 
    email: str = Field(unique=True, max_length=30) 
    password: str = Field(max_length=255) 
    created_at: datetime = Field(default_factory=datetime.timezone.utc.now) 
    updated_at: datetime = Field(default_factory=datetime.timezone.utc.now)    

# --- School Entity ---
class School(SQLModel, table=True):
    school_id: str = Field(primary_key=True, unique=True) 
    school_name: str = Field(max_length=50) 
    created_at: datetime = Field(default_factory=datetime.timezone.utc.now) 
    updated_at: datetime = Field(default_factory=datetime.timezone.utc.now) 

# --- Teacher Entity ---
class Teacher(SQLModel, table=True):
    teacherID: str = Field(primary_key=True, unique=True) 
    user_id: str = Field(foreign_key="User.user_id") 
    school_id: str = Field(foreign_key="School.school_id") 

# --- Student Entity ---
class Student(SQLModel, table=True):
    student_id: str = Field(primary_key=True, unique=True) 
    # performance: float = Field(default=0.0) 
    status: str = Field(max_length=100) 
    user_id: str = Field(foreign_key="User.user_id") 
    teacher_id: str = Field(foreign_key="Teacher.teacher_id") 

# --- Question Entity ---
class Question(SQLModel, table=True):
    question_id: str = Field(primary_key=True, unique=True) 
    strand: str = Field(max_length=30) 
    sub_strand: str = Field(max_length=30) 
    difficulty: str = Field(max_length=30) 
    question: str = Field(max_length=150) 
    option_a: str = Field(max_length=50) 
    option_b: str = Field(max_length=50) 
    option_c: str = Field(max_length=50) 
    option_d: str = Field(max_length=50) 
    answer: str = Field(max_length=50) 
    feedback: str = Field(max_length=150) 
    created_at: datetime = Field(default_factory=datetime.timezone.utc.now) 
    updated_at: datetime = Field(default_factory=datetime.timezone.utc.now) 

class LearningSession(SQLModel, table=True):
    session_id: str = Field(primary_key=True, unique=True)
    start_time: datetime = Field(default_factory=datetime.timezone.utc.now)
    end_time: datetime = Field(default_factory=datetime.timezone.utc.now)
    device_offline_flag: bool = Field()
    student_id: str = Field(foreign_key="Student.student_id")

class StudentResponse(SQLModel, table=True):
    response_id: str = Field(primary_key=True, unique=True)
    selected_answer: str = Field(max_length=50)
    is_correct: bool = Field()
    response_time: int = Field()
    attempt_number: int = Field()
    created_at: datetime = Field(default_factory=datetime.timezone.utc.now)
    updated_at: datetime = Field(default_factory=datetime.timezone.utc.now)
    student_id: str = Field(foreign_key="Student.student_id")
    question_id: str = Field(foreign_key="Question.question_id")
    sesion_id: str = Field(foreign_key="LearningSession.session_id")

class Hint(SQLModel, table=True):
    hint_id: str = Field(primary_key=True, unique=True)
    hint_level: int = Field()
    hint_text: str = Field(max_length=50)
    question_id: str = Field(foreign_key="Question.question_id")

class HintUsage(SQLModel, table=True):
    usage_id: str = Field(primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.timezone.utc.now)
    updated_at: datetime = Field(default_factory=datetime.timezone.utc.now)
    response_id: str = Field(foreign_key="StudentResponse.response_id")
    hint_id: str = Field(foreign_key="Hint.hint_id")

class LearningPorgress(SQLModel, table=True):
    progress_id: str = Field(primary_key=True, unique=True)
    strand: str = Field(max_length=30)
    sub_strand: str = Field(max_length=30)
    mastery_level: float = Field()
    last_updated: datetime = Field(default_factory=datetime.timezone.utc.now)
    student_id: str = Field(foreign_key="Student.student_id")

class AdaptiveDecision(SQLModel, table=True):
    decision_id: str = Field(primary_key=True, unique=True)
    previous_difficulty: str = Field(max_length=50)
    new_difficulty: str = Field(max_length=50)
    reason: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.timezone.utc.now)
    updated_at: datetime = Field(default_factory=datetime.timezone.utc.now)
    student_id: str = Field(foreign_key="Student.student_id")
    session_id: str = Field(foreign_key="LearningSession.session_id")