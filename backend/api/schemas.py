# api/schemas.py
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        from_attributes=True
    )

# ==========================================
# 1. USER & AUTHENTICATION SCHEMAS
# ==========================================

class UserBase(BaseSchema):
    surname: str = Field(..., max_length=30)
    other_names: str = Field(..., max_length=70)
    email: EmailStr = Field(..., max_length=30)

class UserCreate(UserBase):
    password: str = Field(..., max_length=255)

class UserRes(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

class TeacherCreate(BaseSchema):
    user_id: UUID
    school_id: UUID

class TeacherRes(BaseSchema):
    id: UUID
    user_id: UUID
    school_id: UUID

class StudentCreate(BaseSchema):
    user_id: UUID
    teacher_id: UUID
    status: str = Field(..., max_length=100)

class StudentRes(BaseSchema):
    id: UUID
    user_id: UUID
    teacher_id: UUID
    status: str

# ==========================================
# 2. CONTENT & CURRICULUM SCHEMAS
# ==========================================

class QuestionBase(BaseSchema):
    strand: str = Field(..., max_length=30)
    sub_strand: str = Field(..., max_length=30)
    difficulty: str = Field(..., max_length=30)
    question: str = Field(..., max_length=150)
    option_a: str = Field(..., max_length=50)
    option_b: str = Field(..., max_length=50)
    option_c: str = Field(..., max_length=50)
    option_d: str = Field(..., max_length=50)
    answer: str = Field(..., max_length=50)
    feedback: str = Field(..., max_length=150)
    
    # Adaptive properties (if used in Engine)
    difficulty_parameter: float = 0.5
    discrimination_parameter: float = 1.0

class QuestionCreate(QuestionBase):
    pass

class QuestionRes(QuestionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

class HintPayload(BaseSchema):
    hint_level: int
    content_payload: Dict[str, Any]

# ==========================================
# 3. SYNC & ADAPTIVE ENGINE SCHEMAS
# ==========================================

class SyncRecordModel(BaseSchema):
    id: UUID
    student_id: UUID
    question_id: UUID
    skill_id: UUID
    student_answer: str
    attempt_number: int
    ability_level: float
    recorded_at: datetime

class SyncBatchPayload(BaseSchema):
    session_id: UUID
    records: List[SyncRecordModel]

class EngineFeedbackResponse(BaseSchema):
    is_correct: bool
    updated_ability: float
    next_action: str
    hint: Optional[HintPayload] = None
    next_question_id: Optional[UUID] = None

# ==========================================
# 4. REPORTING & MASTERY SCHEMAS
# ==========================================

class MasteryRecord(BaseSchema):
    standard_id: UUID
    standard_code: str
    mastery_level: float
    last_updated: datetime

class StudentMasteryDashboard(BaseSchema):
    student_id: UUID
    student_name: str
    mastery_records: List[MasteryRecord]
    at_risk: bool = False

class ClassReportResponse(BaseSchema):
    class_id: UUID
    teacher_id: UUID
    students: List[StudentMasteryDashboard]