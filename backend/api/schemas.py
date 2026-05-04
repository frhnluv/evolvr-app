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
    name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=100)
    role: str = Field(..., description="student, teacher, or admin")
    school_id: Optional[UUID] = None

class UserCreate(UserBase):
    password: str = Field(..., max_length=255)

class UserRes(UserBase):
    id: UUID
    created_at: datetime

class SchoolBase(BaseSchema):
    name: str = Field(..., max_length=100)
    district_id: Optional[UUID] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolRes(SchoolBase):
    id: UUID
    created_at: datetime

class TeacherCreate(BaseSchema):
    user_id: UUID

class TeacherRes(BaseSchema):
    id: UUID
    user_id: UUID

class StudentCreate(BaseSchema):
    user_id: UUID
    grade_level: Optional[int] = None
    current_path_id: Optional[str] = None
    total_minutes: int = 0

class StudentRes(StudentCreate):
    id: UUID

# ==========================================
# 2. CONTENT & CURRICULUM SCHEMAS
# ==========================================

class QuestionBase(BaseSchema):
    lesson_id: UUID
    skill_id: UUID
    difficulty_parameter: float = 0.0
    discrimination_parameter: float = 1.0
    content_payload: Dict[str, Any]

class QuestionCreate(QuestionBase):
    pass

class QuestionRes(QuestionBase):
    id: UUID
    created_at: datetime

class HintBase(BaseSchema):
    question_id: UUID
    hint_level: int = Field(..., ge=1, le=5)
    content_payload: Dict[str, Any]

class HintCreate(HintBase):
    pass

class HintRes(HintBase):
    id: UUID
    created_at: datetime

# ==========================================
# 3. SYNC & ADAPTIVE ENGINE SCHEMAS
# ==========================================

class SyncRecordModel(BaseSchema):
    id: UUID
    question_id: UUID
    skill_id: UUID
    student_answer: Any # Could be string, dict, etc based on content_payload
    attempt_number: int
    ability_level: float
    recorded_at: datetime
    time_spent_seconds: Optional[int] = None
    hint_used_id: Optional[UUID] = None

class SyncBatchPayload(BaseSchema):
    session_id: UUID
    student_id: UUID
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

class LessonSessionBase(BaseSchema):
    student_id: UUID
    lesson_id: Optional[UUID] = None
    state: str = "ACTIVE"
    score: Optional[int] = None

class LessonSessionCreate(LessonSessionBase):
    pass

class LessonSessionRes(LessonSessionBase):
    id: UUID
    start_timestamp: datetime
    synced_at: Optional[datetime] = None

class ResponseBase(BaseSchema):
    lesson_session_id: UUID
    question_id: UUID
    is_correct: bool
    interaction_data: Optional[Dict[str, Any]] = None
    attempt_number: int = 1
    time_spent_seconds: Optional[int] = None
    hint_used_id: Optional[UUID] = None

class ResponseCreate(ResponseBase):
    pass

class ResponseRes(ResponseBase):
    id: UUID
    recorded_time: datetime

# ==========================================
# 4. REPORTING & MASTERY SCHEMAS
# ==========================================

class StudentSkillMetricBase(BaseSchema):
    student_id: UUID
    skill_id: UUID
    ability_level: float = 0.0
    mastery_probability: float = 0.0
    struggle_flag: bool = False

class StudentSkillMetricRes(StudentSkillMetricBase):
    id: UUID
    last_assessed: datetime

class StudentMasteryBase(BaseSchema):
    student_id: UUID
    standard_id: UUID
    mastery_level: float = 0.0

class StudentMasteryRes(StudentMasteryBase):
    id: UUID
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