# Quick Start Guide - Calculation System

## ⚡ 5-Minute Setup

### 1. Database is Ready ✅
Migrations already applied. Three new tables created:
- `outcomes_assessmentlomapping`
- `outcomes_lopomapping`
- `outcomes_studentassessmentscore`

### 2. Test the System

```bash
# Start Django shell
python manage.py shell

# Run test calculations
>>> from students.models import Student
>>> from outcomes.models import get_student_po_summary
>>> 
>>> student = Student.objects.first()
>>> summary = get_student_po_summary(student)
>>> print(summary)
```

### 3. Use the API

Start the server:
```bash
python manage.py runserver
```

Test calculation endpoints:
```bash
# Get PO summary for student ID 1
curl -X POST http://127.0.0.1:8000/api/student-scores/student_po_summary/ \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1}'
```

---

## 🎯 Common Tasks

### Create Assessment-LO Mapping (via API)
```bash
curl -X POST http://127.0.0.1:8000/api/assessment-lo-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "assessment": 1,
    "learning_outcome": 1,
    "contribution_percentage": 30.0
  }'
```

### Create LO-PO Mapping (via API)
```bash
curl -X POST http://127.0.0.1:8000/api/lo-po-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "learning_outcome": 1,
    "program_outcome": 1,
    "weight": 5
  }'
```

### Record Student Score (via API)
```bash
curl -X POST http://127.0.0.1:8000/api/student-scores/ \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "assessment": 1,
    "enrollment": 1,
    "score": 85.0
  }'
```

### Calculate LO Scores (via API)
```bash
curl -X POST http://127.0.0.1:8000/api/student-scores/calculate_lo_scores/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "course_id": 1
  }'
```

### Calculate PO Scores (via API)
```bash
curl -X POST http://127.0.0.1:8000/api/student-scores/calculate_po_scores/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "use_credits": true
  }'
```

---

## 🐍 Python Usage

```python
from students.models import Student
from courses.models import Course
from outcomes.models import (
    LearningOutcome,
    ProgramOutcome,
    calculate_lo_score,
    calculate_po_score,
    calculate_all_po_scores,
    get_student_po_summary
)

# Get student
student = Student.objects.get(student_number="2024001")

# Calculate single LO score
lo = LearningOutcome.objects.get(code="CLO-1")
lo_score = calculate_lo_score(lo, student)
print(f"LO Score: {lo_score:.2f}%")

# Calculate single PO score
po = ProgramOutcome.objects.get(code="PO-A")
po_score = calculate_po_score(po, student)
print(f"PO Score: {po_score:.2f}%")

# Calculate all PO scores
all_scores = calculate_all_po_scores(student, use_credits=True)
for po, score in all_scores.items():
    print(f"{po.code}: {score:.2f}%")

# Get comprehensive summary
summary = get_student_po_summary(student)
print(f"Average PO: {summary['statistics']['average_po_score']}%")
print(f"Completed: {summary['statistics']['completed_courses']} courses")
```

---

## 🔗 New Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/assessment-lo-mappings/` | GET, POST | Assessment→LO mappings |
| `/api/lo-po-mappings/` | GET, POST | LO→PO mappings |
| `/api/student-scores/` | GET, POST | Student assessment scores |
| `/api/student-scores/calculate_lo_scores/` | POST | Calculate LO scores |
| `/api/student-scores/calculate_po_scores/` | POST | Calculate PO scores |
| `/api/student-scores/student_po_summary/` | POST | Get PO summary |

---

## 📚 Full Documentation

- **FORMULAS.md** - Mathematical formulas with examples
- **CALCULATION_USAGE.md** - Complete usage guide
- **CALCULATION_IMPLEMENTATION.md** - Technical details
- **README_CALCULATIONS.md** - Implementation summary

---

## ✅ Verification Checklist

- [x] Database migrations applied
- [x] Models imported successfully
- [x] Functions imported successfully
- [x] API endpoints registered
- [x] Admin interfaces available
- [x] No Python errors

---

## 🆘 Need Help?

1. Check **FORMULAS.md** for formula explanations
2. Check **CALCULATION_USAGE.md** for code examples
3. Run `python manage.py shell < test_calculations.py` for testing
4. Access Django admin at `/admin/` to manage data visually

---

## 🎉 You're All Set!

The calculation system is ready to use. Start by:
1. Creating assessment-LO mappings
2. Creating LO-PO mappings
3. Recording student scores
4. Running calculations via API or Python
