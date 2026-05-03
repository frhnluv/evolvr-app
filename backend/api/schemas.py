# api/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# ==========================================
# 1. USER & AUTHENTICATION SCHEMAS
# ==========================================
class UserBase(BaseModel):
    name: str
    email: str
    role: str # 'student', 'teacher', 'admin', 'parent' [cite: 34-39]

class StudentProfile(UserBase):
    id: UUID
    grade_level: int
    current_path_id: Optional[str] = None
    total_minutes: int = 0

class TeacherProfile(UserBase):
    id: UUID
    school_id: UUID

# ==========================================
# 2. CONTENT & CURRICULUM SCHEMAS
# ==========================================
class StandardModel(BaseModel):
    id: UUID
    code: str  # e.g., CCSS ID [cite: 11]
    description: str

class QuestionModel(BaseModel):
    id: UUID
    skill_id: UUID
    content_payload: Dict[str, Any]  # The UI rendering data
    difficulty_parameter: float  # For IRT evaluation [cite: 628-629]
    discrimination_parameter: float = 1.0

class HintPayload(BaseModel):
    hint_level: int
    content_payload: Dict[str, Any] # Scaffolded hint data [cite: 263]

# ==========================================
# 3. SYNC & ADAPTIVE ENGINE SCHEMAS
# ==========================================
class SyncRecordModel(BaseModel):
    id: UUID  # Generated offline by Flutter
    student_id: UUID
    question_id: UUID
    skill_id: UUID
    student_answer: str
    attempt_number: int
    ability_level: float
    recorded_at: datetime

class SyncBatchPayload(BaseModel):
    session_id: UUID # Ties to LESSON_SESSIONS [cite: 205]
    records: List[SyncRecordModel]

class EngineFeedbackResponse(BaseModel):
    """What the LangGraph Engine returns to the mobile app"""
    is_correct: bool
    updated_ability: float # Updated via BKT/IRT [cite: 625-630]
    next_action: str # "hint", "new_question", "lesson_complete"
    hint: Optional[HintPayload] = None
    next_question_id: Optional[UUID] = None

class AdaptiveModelUpdate(BaseModel):
    student_id: UUID
    skill_vector: Dict[str, float] # The updated probabilistic state [cite: 209]

# ==========================================
# 4. REPORTING & MASTERY SCHEMAS
# ==========================================
class MasteryRecord(BaseModel):
    standard_id: UUID
    standard_code: str
    mastery_level: float # Confidence score [cite: 47, 86]
    last_updated: datetime

class StudentMasteryDashboard(BaseModel):
    """Powers the Real-Time Mastery Dashboard [cite: 110-115]"""
    student_id: UUID
    student_name: str
    mastery_records: List[MasteryRecord]
    at_risk: bool = False # Triggers Struggling Student Alerts [cite: 126-129]

class ClassReportResponse(BaseModel):
    class_id: UUID
    teacher_id: UUID
    students: List[StudentMasteryDashboard]

# ==========================================
# 5. ROSTERING (WEBHOOK) SCHEMAS
# ==========================================
class RosterDeltaPayload(BaseModel):
    """Payload format expected from Clever/ClassLink webhooks [cite: 135-139]"""
    sync_id: str
    timestamp: datetime
    created_users: List[UserBase]
    deactivated_users: List[str] # Triggers 90-day retention countdown [cite: 142-146]
    class_enrollments: List[Dict[str, str]]