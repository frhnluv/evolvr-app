from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    surname: str = Field(..., max_length=30) # [cite: 7, 8]
    other_names: str = Field(..., max_length=70) # [cite: 9, 10]
    email: EmailStr = Field(..., max_length=30) # [cite: 11, 12]

class UserCreate(UserBase):
    user_id: str = Field(..., max_length=255) # [cite: 5, 6]
    password: str = Field(..., max_length=255) # [cite: 13, 14]

class UserRes(UserBase):
    user_id: str
    created_at: datetime # [cite: 16, 17]
    updated_at: datetime # [cite: 18, 19]

    class Config:
        from_attributes = True

# --- SCHOOL SCHEMAS ---
class SchoolBase(BaseModel):
    school_name: str = Field(..., max_length=50) # [cite: 41, 42]

class SchoolRes(SchoolBase):
    school_id: str # [cite: 39, 40]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- STUDENT SCHEMAS ---
class StudentBase(BaseModel):
    student_id: str = Field(..., max_length=255) # [cite: 21, 22]
    user_id: str # [cite: 27, 28]
    teacher_id: str # [cite: 29, 30]

class StudentCreate(StudentBase):
    status: str = Field(..., max_length=100) # [cite: 25, 26]

class StudentRes(StudentBase):
    status: str
    # Note: We typically include the nested User details in the frontend
    
    class Config:
        from_attributes = True

# --- QUESTION SCHEMAS ---
class QuestionBase(BaseModel):
    strand: str = Field(..., max_length=30) # [cite: 51, 52]
    sub_strand: str = Field(..., max_length=30) # [cite: 53, 54]
    difficulty: str = Field(..., max_length=30) # [cite: 55, 56]
    question: str = Field(..., max_length=150) # [cite: 57, 58]
    option_a: str = Field(..., max_length=50) # [cite: 59, 60]
    option_b: str = Field(..., max_length=50) # [cite: 61, 62]
    option_c: str = Field(..., max_length=50) # [cite: 63, 64]
    option_d: str = Field(..., max_length=50) # [cite: 65, 66]
    answer: str = Field(..., max_length=50) # [cite: 67, 68]
    feedback: str = Field(..., max_length=150) # [cite: 69, 70]

class QuestionRes(QuestionBase):
    question_id: str # [cite: 49, 50]
    
    class Config:
        from_attributes = True

# --- LEARNING SESSION SCHEMAS ---
class LearningSessionBase(BaseModel):
    student_id: str = Field(..., max_length=255)

class LearningSessionCreate(LearningSessionBase):
    pass

class LearningSessionRes(LearningSessionBase):
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    device_offline_flag: bool

    class Config:
        from_attributes = True

# --- STUDENT RESPONSE (ADAPTIVE) SCHEMAS ---
class StudentResponseBase(BaseModel):
    student_id: str = Field(..., max_length=255)
    question_id: str = Field(..., max_length=255)
    session_id: str = Field(..., max_length=255)

    selected_answer: str = Field(..., max_length=50)
    is_correct: bool

class StudentResponseCreate(StudentResponseBase):
    response_time: Optional[int] = None
    attempt_number: Optional[int] = 1

class StudentResponseRes(StudentResponseBase):
    response_id: str
    response_time: Optional[int]
    attempt_number: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- HINT SCHEMAS ---
class HintBase(BaseModel):
    question_id: str = Field(..., max_length=255)
    hint_level: int = Field(..., ge=1, le=5)
    hint_text: str = Field(..., max_length=255)

class HintCreate(HintBase):
    pass

class HintResponse(HintBase):
    hint_id: str

    class Config:
        from_attributes = True

# --- HINT USAGE SCHEMAS ---
class HintUsageBase(BaseModel):
    response_id: str = Field(..., max_length=255)
    hint_id: str = Field(..., max_length=255)

class HintUsageCreate(HintUsageBase):
    pass

class HintUsageResponse(HintUsageBase):
    usage_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- LEARNING PROGRESS SCHEMAS ---
class LearningProgressBase(BaseModel):
    student_id: str = Field(..., max_length=255)
    strand: str = Field(..., max_length=30)
    sub_strand: str = Field(..., max_length=30)

class LearningProgressCreate(LearningProgressBase):
    mastery_level: float = Field(0.0, ge=0, le=100)

class LearningProgressResponse(LearningProgressBase):
    progress_id: str
    mastery_level: float
    last_updated: datetime

    class Config:
        from_attributes = True

# --- ADAPTIVE DECISION SCHEMAS ---
class AdaptiveDecisionBase(BaseModel):
    previous_difficulty: str = Field(..., max_length=50)
    new_difficulty: str = Field(..., max_length=50)
    reason: str = Field(..., max_length=50)
    student_id: str = Field(..., max_length=255)
    session_id: str = Field(max_length=255)

class AdaptiveDecisionCreate(AdaptiveDecisionBase):
    pass

class AdaptiveDecisionRes(AdaptiveDecisionBase):
    decision_id: str = Field(..., max_length=255)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True