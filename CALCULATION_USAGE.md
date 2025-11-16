# Assessment → LO → PO Calculation System

## Overview

This system implements a three-tier academic assessment calculation:
1. **Assessments** → Student scores on quizzes, exams, projects, etc.
2. **Learning Outcomes (LO)** → Course-level learning objectives
3. **Program Outcomes (PO)** → Program-wide competency goals

## Data Models

### New Models Added

1. **AssessmentLOMapping**: Links assessments to learning outcomes with contribution percentage
2. **LOPOMapping**: Links learning outcomes to program outcomes with weight (1-5 scale)
3. **StudentAssessmentScore**: Stores individual student scores on assessments

## Calculation Formulas

### 1. Assessment → LO Calculation
```
LO_Score = Σ(AssessmentGrade * AssessmentWeight)
```

**Example:**
- Quiz contributes 20% to LO1
- Midterm contributes 30% to LO1
- Final contributes 50% to LO1

If a student scores:
- Quiz: 85/100
- Midterm: 90/100
- Final: 88/100

Then: `LO1_Score = (85 * 0.20) + (90 * 0.30) + (88 * 0.50) = 87.0`

### 2. LO → PO Calculation (Weighted Average)
```
PO_Score = Σ(LO_Score * LO_PO_Weight) / Σ(LO_PO_Weight)
```

**Example:**
- LO1 → PO-A with weight 5
- LO2 → PO-A with weight 3
- LO3 → PO-A with weight 4

If scores are:
- LO1: 87.0
- LO2: 92.0
- LO3: 85.0

Then: `PO-A_Score = (87*5 + 92*3 + 85*4) / (5+3+4) = 87.75`

### 3. Final PO Score Across Courses (Credit-Weighted)
```
PO_Final = Σ(PO_from_course * CourseCredit) / Σ(CourseCredit)
```

**Example:**
- CS201 (3 credits): PO-A = 87.0
- CS301 (4 credits): PO-A = 92.0
- CS302 (3 credits): PO-A = 85.0

Then: `PO-A_Final = (87*3 + 92*4 + 85*3) / (3+4+3) = 88.4`

## Python Functions

### Import Functions
```python
from outcomes.models import (
    calculate_lo_score,
    calculate_po_score,
    calculate_all_po_scores,
    calculate_student_lo_scores,
    get_student_po_summary
)
```

### Function Usage

#### 1. Calculate LO Score
```python
from students.models import Student
from outcomes.models import LearningOutcome, calculate_lo_score

student = Student.objects.get(id=1)
lo = LearningOutcome.objects.get(code='CLO-1')

score = calculate_lo_score(lo, student)
print(f"LO Score: {score:.2f}%")
```

#### 2. Calculate PO Score
```python
from students.models import Student
from outcomes.models import ProgramOutcome, calculate_po_score

student = Student.objects.get(id=1)
po = ProgramOutcome.objects.get(code='PO-A')

# For a specific course
score = calculate_po_score(po, student, course=my_course)

# Across all courses
score = calculate_po_score(po, student)
print(f"PO Score: {score:.2f}%")
```

#### 3. Calculate All PO Scores
```python
from students.models import Student
from outcomes.models import calculate_all_po_scores

student = Student.objects.get(id=1)

# With credit weighting
po_scores = calculate_all_po_scores(student, use_credits=True)

# Without credit weighting (simple average)
po_scores = calculate_all_po_scores(student, use_credits=False)

for po, score in po_scores.items():
    print(f"{po.code}: {score:.2f}%")
```

#### 4. Get Comprehensive PO Summary
```python
from students.models import Student
from outcomes.models import get_student_po_summary

student = Student.objects.get(id=1)
summary = get_student_po_summary(student)

print(f"Student: {summary['student'].name}")
print(f"Average PO Score: {summary['statistics']['average_po_score']}")
print(f"Completed Courses: {summary['statistics']['completed_courses']}")
print(f"Total Credits: {summary['statistics']['total_credits']}")

for po_code, data in summary['po_scores'].items():
    print(f"{po_code}: {data['score']}% - {data['achievement_level']}")
```

## API Endpoints

### Calculate LO Scores
```
POST /api/student-scores/calculate_lo_scores/
Body: {"student_id": 1, "course_id": 2}
```

### Calculate PO Scores
```
POST /api/student-scores/calculate_po_scores/
Body: {"student_id": 1, "use_credits": true}
```

### Get PO Summary
```
POST /api/student-scores/student_po_summary/
Body: {"student_id": 1}
```

## Setup Requirements

### 1. Create Assessment-LO Mappings
```python
from outcomes.models import Assessment, LearningOutcome, AssessmentLOMapping

assessment = Assessment.objects.get(name='Midterm Exam')
lo = LearningOutcome.objects.get(code='CLO-1')

AssessmentLOMapping.objects.create(
    assessment=assessment,
    learning_outcome=lo,
    contribution_percentage=30.0  # 30% contribution
)
```

### 2. Create LO-PO Mappings
```python
from outcomes.models import LearningOutcome, ProgramOutcome, LOPOMapping

lo = LearningOutcome.objects.get(code='CLO-1')
po = ProgramOutcome.objects.get(code='PO-A')

LOPOMapping.objects.create(
    learning_outcome=lo,
    program_outcome=po,
    weight=5  # Weight on 1-5 scale
)
```

### 3. Record Student Scores
```python
from outcomes.models import StudentAssessmentScore

StudentAssessmentScore.objects.create(
    student=student,
    assessment=assessment,
    enrollment=enrollment,
    score=85.0  # Student's actual score
)
```

## Achievement Levels

Scores are automatically categorized:
- **EXCEEDED**: ≥ 85%
- **ACHIEVED**: 70-84%
- **PARTIALLY**: 50-69%
- **NOT_ACHIEVED**: < 50%

## New API Endpoints

1. **Assessment-LO Mappings**: `/api/assessment-lo-mappings/`
2. **LO-PO Mappings**: `/api/lo-po-mappings/`
3. **Student Scores**: `/api/student-scores/`

All endpoints support full CRUD operations (GET, POST, PUT, PATCH, DELETE).
