# Automatic Calculation Usage Guide

## Overview

Calculations now happen **automatically** when you fetch data from existing endpoints. No separate calculation endpoints needed!

---

## How It Works

### 1. **Enrollments** - Automatically shows LO scores

When you GET an enrollment, it automatically calculates all Learning Outcome scores for that student in that course.

```bash
GET /api/enrollments/
GET /api/enrollments/{id}/
```

**Response includes:**
```json
{
  "id": 1,
  "student_name": "Alice Johnson",
  "course_code": "CS201",
  "status": "COMPLETED",
  "lo_scores": [
    {
      "lo_code": "CLO-1",
      "lo_description": "Understand data structures",
      "score": 88.0,
      "achievement_level": "EXCEEDED"
    },
    {
      "lo_code": "CLO-2",
      "lo_description": "Implement algorithms",
      "score": 92.0,
      "achievement_level": "EXCEEDED"
    }
  ]
}
```

---

### 2. **Learning Outcomes** - Add `student_id` to calculate scores

When you GET learning outcomes and provide a `student_id`, it automatically calculates that student's score.

```bash
GET /api/learning-outcomes/?student_id=1
GET /api/learning-outcomes/{id}/?student_id=1
GET /api/learning-outcomes/by_course/?course_id=2&student_id=1
```

**Response includes:**
```json
{
  "id": 1,
  "code": "CLO-1",
  "description": "Understand data structures",
  "course_code": "CS201",
  "calculated_scores": {
    "student_id": 1,
    "student_name": "Alice Johnson",
    "score": 88.0,
    "achievement_level": "EXCEEDED"
  }
}
```

---

### 3. **Program Outcomes** - Add `student_id` to calculate scores

When you GET program outcomes and provide a `student_id`, it automatically calculates that student's PO score.

```bash
GET /api/program-outcomes/?student_id=1
GET /api/program-outcomes/{id}/?student_id=1
GET /api/program-outcomes/?student_id=1&use_credits=true
```

**Response includes:**
```json
{
  "id": 1,
  "code": "PO-A",
  "title": "Technical Excellence",
  "calculated_scores": {
    "student_id": 1,
    "student_name": "Alice Johnson",
    "score": 89.45,
    "achievement_level": "EXCEEDED"
  }
}
```

---

## Examples

### Example 1: Get all LO scores for a student in a specific course

```bash
curl "http://127.0.0.1:8000/api/learning-outcomes/by_course/?course_id=2&student_id=1"
```

Returns all learning outcomes for course 2, with calculated scores for student 1.

---

### Example 2: Get student's enrollment with LO scores

```bash
curl "http://127.0.0.1:8000/api/enrollments/?student=1"
```

Returns all enrollments for student 1, each with calculated LO scores.

---

### Example 3: Get all PO scores for a student

```bash
curl "http://127.0.0.1:8000/api/program-outcomes/?student_id=1"
```

Returns all program outcomes with calculated scores for student 1.

---

### Example 4: Get specific PO score for a student

```bash
curl "http://127.0.0.1:8000/api/program-outcomes/1/?student_id=1"
```

Returns PO #1 with calculated score for student 1.

---

## When Calculations Happen

### ✅ Automatic Calculation Happens When:

1. **Enrollments**: Always calculated for COMPLETED enrollments
2. **Learning Outcomes**: When `student_id` is in query params
3. **Program Outcomes**: When `student_id` is in query params

### ❌ No Calculation When:

1. **Enrollments**: Status is not COMPLETED
2. **Learning Outcomes**: No `student_id` provided
3. **Program Outcomes**: No `student_id` provided
4. **No data**: Student hasn't taken assessments or no mappings exist

---

## Data Flow

```
1. POST Assessment Score
   └─> Stored in StudentAssessmentScore

2. GET Enrollment
   └─> Automatically calculates LO scores
       └─> Uses AssessmentLOMapping + StudentAssessmentScore

3. GET Learning Outcome (with student_id)
   └─> Automatically calculates LO score for that student
       └─> Uses AssessmentLOMapping + StudentAssessmentScore

4. GET Program Outcome (with student_id)
   └─> Automatically calculates PO score for that student
       └─> Uses LOPOMapping + calculated LO scores
```

---

## Setup Requirements

Before calculations work, you need:

1. **Assessment-LO Mappings**: Link assessments to learning outcomes
   ```bash
   POST /api/assessment-lo-mappings/
   {
     "assessment": 1,
     "learning_outcome": 1,
     "contribution_percentage": 30.0
   }
   ```

2. **LO-PO Mappings**: Link learning outcomes to program outcomes
   ```bash
   POST /api/lo-po-mappings/
   {
     "learning_outcome": 1,
     "program_outcome": 1,
     "weight": 5
   }
   ```

3. **Student Scores**: Record student assessment scores
   ```bash
   POST /api/student-scores/
   {
     "student": 1,
     "assessment": 1,
     "enrollment": 1,
     "score": 85.0
   }
   ```

---

## Benefits

✅ **Simple**: Just add `?student_id=X` to your existing endpoints
✅ **Automatic**: Calculations happen transparently
✅ **Efficient**: Only calculates when needed
✅ **RESTful**: Uses existing endpoints, no special calculation routes
✅ **Flexible**: Works with single items or lists

---

## API Quick Reference

| Endpoint | Query Param | Returns |
|----------|-------------|---------|
| `/api/enrollments/` | (none) | Enrollments with LO scores |
| `/api/learning-outcomes/` | `?student_id=X` | LOs with calculated scores |
| `/api/learning-outcomes/by_course/` | `?course_id=Y&student_id=X` | Course LOs with scores |
| `/api/program-outcomes/` | `?student_id=X` | POs with calculated scores |
| `/api/program-outcomes/{id}/` | `?student_id=X` | Single PO with score |

---

## Testing

Start your server:
```bash
python manage.py runserver
```

Test automatic calculations:
```bash
# Get enrollments (auto-calculates LO scores)
curl "http://127.0.0.1:8000/api/enrollments/"

# Get learning outcomes with student scores
curl "http://127.0.0.1:8000/api/learning-outcomes/?student_id=1"

# Get program outcomes with student scores
curl "http://127.0.0.1:8000/api/program-outcomes/?student_id=1"
```
