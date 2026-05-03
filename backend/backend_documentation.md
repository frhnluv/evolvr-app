# Evolvr Backend API Documentation

This document serves as a comprehensive guide for frontend developers integrating with the Evolvr backend.

## Overview

The Evolvr backend is built with **FastAPI** and uses **Supabase** for database management. It includes an Adaptive Learning Engine powered by **LangGraph** to process student interactions and generate AI-driven hints.

> [!TIP]
> **Naming Conventions (Crucial for Frontend):** 
> The Python backend internally uses `snake_case` (e.g., `user_id`), but the API is configured to **automatically translate to and from `camelCase`**. 
> 
> You should send JSON payloads in standard `camelCase` (e.g., `userId`), and you will receive responses in `camelCase`. The examples below reflect the `camelCase` format you will interact with.

---

## 1. Authentication & Users

All user-related operations, regardless of whether the user is a teacher or a student.

### `POST /api/users/`
Registers a new user in the system.

**Request Body:**
```json
{
  "surname": "Doe",
  "otherNames": "John",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "surname": "Doe",
  "otherNames": "John",
  "email": "john.doe@example.com",
  "createdAt": "2026-05-03T17:00:00Z",
  "updatedAt": "2026-05-03T17:00:00Z"
}
```

### `GET /api/users/{email}`
Fetches user details via email address. Returns the same payload as the `POST` response above.

### `PUT /api/users/{user_id}/password`
Updates a user's password. Expects `new_password` as a query parameter (e.g., `?new_password=abc`).

### `DELETE /api/users/{user_id}`
Deletes a user. Returns `204 No Content`.

---

## 2. Students

Manages student-specific profiles and performance tracking.

### `POST /api/students/`
Creates a student profile linked to a base `User` and a `Teacher`.

**Request Body:**
```json
{
  "userId": "uuid-of-user",
  "teacherId": "uuid-of-teacher",
  "status": "Developing"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-of-student",
  "userId": "uuid-of-user",
  "teacherId": "uuid-of-teacher",
  "status": "Developing"
}
```

### `GET /api/students/{student_id}`
Fetches specific student details.

### `GET /api/students/`
Fetches a list of all students.

### `PUT /api/students/{student_id}/progress`
Updates a student's performance score (0-100) and automatically recalculates their `status` (e.g., "Exceeding Expectations" vs "Developing").
Expects `score` as a query parameter (e.g., `?score=85`).

### `DELETE /api/students/{student_id}`
Deletes a student. Returns `204 No Content`.

---

## 3. Teachers

Manages teacher profiles and their respective classrooms.

### `POST /api/teachers/`
**Request Body:**
```json
{
  "userId": "uuid-of-user",
  "schoolId": "uuid-of-school"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-of-teacher",
  "userId": "uuid-of-user",
  "schoolId": "uuid-of-school"
}
```

### `GET /api/teachers/{teacher_id}/dashboard`
Returns a list of all students assigned to this teacher.

**Response (200 OK):**
```json
[
  {
    "id": "uuid-of-student",
    "userId": "uuid-of-user",
    "teacherId": "uuid-of-teacher",
    "status": "Exceeding Expectations"
  }
]
```

---

## 4. Questions & Curriculum

Manages the learning materials and quizzes.

### `POST /api/questions/`
Adds a new question to the database.

**Request Body:**
```json
{
  "strand": "Algebra",
  "subStrand": "Equations",
  "difficulty": "Medium",
  "question": "What is x if 2x = 4?",
  "optionA": "1",
  "optionB": "2",
  "optionC": "3",
  "optionD": "4",
  "answer": "2",
  "feedback": "Divide both sides by 2.",
  "difficultyParameter": 0.5,
  "discriminationParameter": 1.0
}
```

### `GET /api/questions/strand/{strand_name}`
Retrieves all questions for a specific learning strand (e.g., `/api/questions/strand/Algebra`).

---

## 5. Offline Sync & Adaptive Engine

> [!IMPORTANT]
> The `/api/sync/outbox` endpoint is the core of the mobile integration. It is designed to receive batched, offline learning transactions from the frontend (Flutter app) and process them through the LangGraph Adaptive Engine.

### `POST /api/sync/outbox`
Processes batched interactions. The engine evaluates correctness, updates BKT (Bayesian Knowledge Tracing) ability levels, generates hints via AI, and selects the next most appropriate question using Item Response Theory (IRT).

**Request Body:**
```json
{
  "sessionId": "uuid-of-session",
  "records": [
    {
      "id": "uuid-of-offline-record",
      "studentId": "uuid-of-student",
      "questionId": "uuid-of-question",
      "skillId": "Algebra",
      "studentAnswer": "3",
      "attemptNumber": 1,
      "abilityLevel": 0.5,
      "recordedAt": "2026-05-03T17:00:00Z"
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "message": "Sync processed",
  "syncedCount": 1,
  "failedCount": 0,
  "syncedIds": ["uuid-of-offline-record"],
  "engineFeedback": {
    "uuid-of-offline-record": {
      "isCorrect": false,
      "updatedAbility": 0.45,
      "nextAction": "hint",
      "hint": {
        "hintLevel": 1,
        "contentPayload": {
          "content": "Remember to perform the same operation on both sides of the equal sign."
        }
      },
      "nextQuestionId": null
    }
  },
  "failedDetails": []
}
```

### How to use `engineFeedback` on the Frontend:
When the frontend syncs offline responses, the backend evaluates each one. The frontend should look at `engineFeedback[record_id]` to see what happens next:
1. **If `isCorrect` is true**, move the student forward (`nextQuestionId` will be provided).
2. **If `isCorrect` is false**, check `nextAction`. If it equals `"hint"`, display the text found in `hint.contentPayload.content` to the student and let them try the same question again (incrementing their `attemptNumber`).
