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

# --- SCHOOL SCHEMAS ---
class SchoolBase(BaseSchema):
    school_name: str = Field(..., max_length=50)

class SchoolCreate(SchoolBase):
    pass

class SchoolRes(SchoolBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

# --- TEACHER SCHEMAS ---
class TeacherCreate(BaseSchema):
    user_id: UUID
    school_id: UUID

class TeacherRes(BaseSchema):
    id: UUID
    user_id: UUID
    school_id: UUID

# --- STUDENT SCHEMAS ---
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

# --- HINT SCHEMAS ---
class HintBase(BaseSchema):
    question_id: UUID
    hint_level: int = Field(..., ge=1, le=5)
    hint_text: str = Field(..., max_length=255)

class HintCreate(HintBase):
    pass

class HintResponse(HintBase):
    id: UUID

# --- HINT USAGE SCHEMAS ---
class HintUsageBase(BaseSchema):
    response_id: UUID
    hint_id: UUID

class HintUsageCreate(HintUsageBase):
    pass

class HintUsageResponse(HintUsageBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

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

class HintPayload(BaseSchema):
    hint_level: int
    content_payload: Dict[str, Any]

class EngineFeedbackResponse(BaseSchema):
    is_correct: bool
    updated_ability: float
    next_action: str
    hint: Optional[HintPayload] = None
    next_question_id: Optional[UUID] = None

# --- LEARNING SESSION SCHEMAS ---
class LearningSessionBase(BaseSchema):
    student_id: UUID

class LearningSessionCreate(LearningSessionBase):
    pass

class LearningSessionRes(LearningSessionBase):
    id: UUID
    start_time: datetime
    end_time: Optional[datetime] = None
    device_offline_flag: bool

# --- STUDENT RESPONSE SCHEMAS ---
class StudentResponseBase(BaseSchema):
    student_id: UUID
    question_id: UUID
    session_id: UUID
    selected_answer: str = Field(..., max_length=50)
    is_correct: bool

class StudentResponseCreate(StudentResponseBase):
    response_time: Optional[int] = None
    attempt_number: Optional[int] = 1

class StudentResponseRes(StudentResponseBase):
    id: UUID
    response_time: Optional[int]
    attempt_number: int
    created_at: datetime

# --- ADAPTIVE DECISION SCHEMAS ---
class AdaptiveDecisionBase(BaseSchema):
    previous_difficulty: str = Field(..., max_length=50)
    new_difficulty: str = Field(..., max_length=50)
    reason: str = Field(..., max_length=50)
    student_id: UUID
    session_id: UUID

class AdaptiveDecisionCreate(AdaptiveDecisionBase):
    pass

class AdaptiveDecisionRes(AdaptiveDecisionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

# ==========================================
# 4. REPORTING & MASTERY SCHEMAS
# ==========================================

class LearningProgressBase(BaseSchema):
    student_id: UUID
    strand: str = Field(..., max_length=30)
    sub_strand: str = Field(..., max_length=30)

class LearningProgressCreate(LearningProgressBase):
    mastery_level: float = Field(0.0, ge=0, le=100)

class LearningProgressResponse(LearningProgressBase):
    id: UUID
    mastery_level: float
    last_updated: datetime

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