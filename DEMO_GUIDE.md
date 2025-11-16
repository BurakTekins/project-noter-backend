# 🎬 DEMO MODE - Automatic Calculations

## Overview

All calculations happen **automatically** based on grades and percentages. No student_id or extra parameters needed!

---

## 📊 How It Works

### 1. **Enrollments** → Shows LO Scores Automatically
```bash
GET /api/enrollments/
```

**Returns:**
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
    }
  ]
}
```

---

### 2. **Learning Outcomes** → Shows All Student Scores
```bash
GET /api/learning-outcomes/
GET /api/learning-outcomes/{id}/
```

**Returns:**
```json
{
  "id": 1,
  "code": "CLO-1",
  "description": "Understand data structures",
  "course_code": "CS201",
  "calculated_scores": [
    {
      "student_id": 1,
      "student_name": "Alice Johnson",
      "score": 88.0,
      "achievement_level": "EXCEEDED"
    },
    {
      "student_id": 2,
      "student_name": "Bob Smith",
      "score": 75.5,
      "achievement_level": "ACHIEVED"
    }
  ]
}
```

---

### 3. **Program Outcomes** → Shows All Student Scores
```bash
GET /api/program-outcomes/
GET /api/program-outcomes/{id}/
```

**Returns:**
```json
{
  "id": 1,
  "code": "PO-A",
  "title": "Technical Excellence",
  "calculated_scores": [
    {
      "student_id": 1,
      "student_name": "Alice Johnson",
      "score": 89.45,
      "achievement_level": "EXCEEDED"
    },
    {
      "student_id": 2,
      "student_name": "Bob Smith",
      "score": 78.20,
      "achievement_level": "ACHIEVED"
    }
  ]
}
```

---

## 🎯 Demo Flow

### Step 1: View Current Data
```bash
# See all students
curl http://127.0.0.1:8000/api/students/

# See all courses
curl http://127.0.0.1:8000/api/courses/

# See all assessments
curl http://127.0.0.1:8000/api/assessments/
```

---

### Step 2: See Automatic Calculations
```bash
# View enrollments with calculated LO scores
curl http://127.0.0.1:8000/api/enrollments/

# View learning outcomes with all student scores
curl http://127.0.0.1:8000/api/learning-outcomes/

# View program outcomes with all student scores
curl http://127.0.0.1:8000/api/program-outcomes/
```

---

### Step 3: Add New Data (Optional)
```bash
# Add a student assessment score
curl -X POST http://127.0.0.1:8000/api/student-scores/ \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "assessment": 1,
    "enrollment": 1,
    "score": 85.0
  }'

# Create Assessment-LO mapping
curl -X POST http://127.0.0.1:8000/api/assessment-lo-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "assessment": 1,
    "learning_outcome": 1,
    "contribution_percentage": 30.0
  }'

# Create LO-PO mapping
curl -X POST http://127.0.0.1:8000/api/lo-po-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "learning_outcome": 1,
    "program_outcome": 1,
    "weight": 5
  }'
```

---

## 🧮 Calculation Logic

### Assessment → LO Score
```
LO_Score = Σ(Assessment_Score * Contribution_Percentage)

Example:
Quiz (20%): 85/100
Midterm (30%): 90/100
Final (50%): 88/100

CLO-1 Score = (85 * 0.20) + (90 * 0.30) + (88 * 0.50)
            = 17.0 + 27.0 + 44.0
            = 88.0%
```

### LO → PO Score
```
PO_Score = Σ(LO_Score * Weight) / Σ(Weight)

Example:
CLO-1 (weight 5): 88.0%
CLO-2 (weight 3): 92.0%

PO-A Score = (88 * 5 + 92 * 3) / (5 + 3)
           = (440 + 276) / 8
           = 89.5%
```

---

## 🎬 Demo Presentation Tips

### Show Learning Outcomes
```bash
curl http://127.0.0.1:8000/api/learning-outcomes/ | python3 -m json.tool
```
**Highlight:** "Each learning outcome shows calculated scores for all students automatically!"

### Show Program Outcomes
```bash
curl http://127.0.0.1:8000/api/program-outcomes/ | python3 -m json.tool
```
**Highlight:** "Program outcomes aggregate from multiple learning outcomes with weighted calculations!"

### Show Enrollments
```bash
curl http://127.0.0.1:8000/api/enrollments/ | python3 -m json.tool
```
**Highlight:** "Each enrollment shows all learning outcome scores for that student in that course!"

---

## 📈 Achievement Levels

| Score | Level | Color |
|-------|-------|-------|
| ≥ 85% | EXCEEDED | 🟢 Green |
| 70-84% | ACHIEVED | 🔵 Blue |
| 50-69% | PARTIALLY | 🟡 Yellow |
| < 50% | NOT_ACHIEVED | 🔴 Red |

---

## ✨ Demo Highlights

### ✅ Automatic
- No manual calculation needed
- Scores update when data changes
- Works across all endpoints

### ✅ Comprehensive
- Shows all students
- All learning outcomes
- All program outcomes
- Complete achievement tracking

### ✅ Real-time
- Calculations happen on request
- Always up-to-date
- Based on actual data

---

## 🚀 Quick Test

Start server:
```bash
python manage.py runserver
```

Test endpoints:
```bash
# Terminal 1: Watch enrollments with LO scores
curl http://127.0.0.1:8000/api/enrollments/ | python3 -m json.tool

# Terminal 2: Watch learning outcomes with all student scores
curl http://127.0.0.1:8000/api/learning-outcomes/ | python3 -m json.tool

# Terminal 3: Watch program outcomes with all student scores
curl http://127.0.0.1:8000/api/program-outcomes/ | python3 -m json.tool
```

---

## 📝 Key Endpoints for Demo

| Endpoint | Shows |
|----------|-------|
| `/api/enrollments/` | Student enrollments with LO scores |
| `/api/learning-outcomes/` | LOs with all student scores |
| `/api/program-outcomes/` | POs with all student scores |
| `/api/students/` | All students |
| `/api/courses/` | All courses |
| `/api/assessments/` | All assessments |

---

## 🎉 Demo Ready!

Everything calculates automatically based on:
- ✅ Assessment scores
- ✅ Assessment-LO mappings (contribution percentages)
- ✅ LO-PO mappings (weights)
- ✅ Course credits (for PO calculations)

**No configuration needed - just GET the data and see the calculations!**
