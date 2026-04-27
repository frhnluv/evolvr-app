from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# --- User Entity ---
class User(SQLModel, table=True):
    userID: str = Field(primary_key=True, unique=True, index=True) 
    surname: str = Field(max_length=30) 
    otherNames: str = Field(max_length=70) 
    email: str = Field(unique=True, max_length=30) 
    password: str = Field(max_length=255) 
    createdAt: datetime = Field(default_factory=datetime.timezone.utc.now) 
    updatedAt: datetime = Field(default_factory=datetime.timezone.utc.now)    

# --- School Entity ---
class School(SQLModel, table=True):
    schoolID: str = Field(primary_key=True, unique=True) 
    schoolName: str = Field(max_length=50) 
    createdAt: datetime = Field(default_factory=datetime.timezone.utc.now) 
    updatedAt: datetime = Field(default_factory=datetime.timezone.utc.now) 

# --- Teacher Entity ---
class Teacher(SQLModel, table=True):
    teacherID: str = Field(primary_key=True, unique=True) 
    userID: str = Field(foreign_key="user.userID") 
    schoolID: str = Field(foreign_key="school.schoolID") 

# --- Student Entity ---
class Student(SQLModel, table=True):
    studentID: str = Field(primary_key=True, unique=True) 
    performance: float = Field(default=0.0) 
    status: str = Field(max_length=100) 
    userID: str = Field(foreign_key="user.userID") 
    teacherID: str = Field(foreign_key="teacher.teacherID") 

# --- Question Entity ---
class Question(SQLModel, table=True):
    questionID: str = Field(primary_key=True, unique=True) 
    strand: str = Field(max_length=30) 
    subStrand: str = Field(max_length=30) 
    difficulty: str = Field(max_length=30) 
    question: str = Field(max_length=150) 
    optionA: str = Field(max_length=50) 
    optionB: str = Field(max_length=50) 
    optionC: str = Field(max_length=50) 
    optionD: str = Field(max_length=50) 
    answer: str = Field(max_length=50) 
    feedback: str = Field(max_length=150) 
    createdAt: datetime = Field(default_factory=datetime.timezone.utc.now) 
    updatedAt: datetime = Field(default_factory=datetime.timezone.utc.now) 