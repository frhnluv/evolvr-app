from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    surname: str = Field(..., max_length=30) # [cite: 7, 8]
    otherNames: str = Field(..., max_length=70) # [cite: 9, 10]
    email: EmailStr = Field(..., max_length=30) # [cite: 11, 12]

class UserCreate(UserBase):
    userID: str = Field(..., max_length=255) # [cite: 5, 6]
    password: str = Field(..., max_length=255) # [cite: 13, 14]

class UserResponse(UserBase):
    userID: str
    createdAt: datetime # [cite: 16, 17]
    updatedAt: datetime # [cite: 18, 19]

    class Config:
        from_attributes = True

# --- SCHOOL SCHEMAS ---
class SchoolBase(BaseModel):
    schoolName: str = Field(..., max_length=50) # [cite: 41, 42]

class SchoolResponse(SchoolBase):
    schoolID: str # [cite: 39, 40]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

# --- STUDENT SCHEMAS ---
class StudentBase(BaseModel):
    studentID: str = Field(..., max_length=255) # [cite: 21, 22]
    userID: str # [cite: 27, 28]
    teacherID: str # [cite: 29, 30]

class StudentCreate(StudentBase):
    performance: float = Field(0.0, ge=0, le=100) # [cite: 23, 24]
    status: str = Field(..., max_length=100) # [cite: 25, 26]

class StudentResponse(StudentBase):
    performance: float
    status: str
    # Note: We typically include the nested User details in the frontend
    
    class Config:
        from_attributes = True

# --- QUESTION SCHEMAS ---
class QuestionBase(BaseModel):
    strand: str = Field(..., max_length=30) # [cite: 51, 52]
    subStrand: str = Field(..., max_length=30) # [cite: 53, 54]
    difficulty: str = Field(..., max_length=30) # [cite: 55, 56]
    question: str = Field(..., max_length=150) # [cite: 57, 58]
    optionA: str = Field(..., max_length=50) # [cite: 59, 60]
    optionB: str = Field(..., max_length=50) # [cite: 61, 62]
    optionC: str = Field(..., max_length=50) # [cite: 63, 64]
    optionD: str = Field(..., max_length=50) # [cite: 65, 66]
    answer: str = Field(..., max_length=50) # [cite: 67, 68]
    feedback: str = Field(..., max_length=150) # [cite: 69, 70]

class QuestionResponse(QuestionBase):
    questionID: str # [cite: 49, 50]
    
    class Config:
        from_attributes = True