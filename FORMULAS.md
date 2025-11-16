# Quick Reference: Calculation Formulas

## Formula 1: Assessment → Learning Outcome (LO)

```
LO_Score = Σ(AssessmentGrade * AssessmentWeight)
```

### Example
If CLO-1 has three assessments:
- Quiz (20% weight): Student scored 85/100 = 85%
- Midterm (30% weight): Student scored 90/100 = 90%
- Final (50% weight): Student scored 88/100 = 88%

**Calculation:**
```
CLO-1 = (85 * 0.20) + (90 * 0.30) + (88 * 0.50)
      = 17.0 + 27.0 + 44.0
      = 88.0%
```

### Implementation
```python
from outcomes.models import calculate_lo_score

lo = LearningOutcome.objects.get(code='CLO-1')
student = Student.objects.get(id=1)
score = calculate_lo_score(lo, student)
# Returns: 88.0
```

---

## Formula 2: Learning Outcome (LO) → Program Outcome (PO)

```
PO_Score = Σ(LO_Score * LO_PO_Weight) / Σ(LO_PO_Weight)
```

This is a **weighted average** where weights range from 1-5.

### Example
If PO-A receives contributions from:
- CLO-1 (weight 5): Score = 88.0%
- CLO-2 (weight 3): Score = 92.0%
- CLO-3 (weight 4): Score = 85.0%

**Calculation:**
```
PO-A = (88 * 5) + (92 * 3) + (85 * 4)
       ─────────────────────────────────
              5 + 3 + 4

     = 440 + 276 + 340
       ───────────────
            12

     = 1056 / 12
     = 88.0%
```

### Implementation
```python
from outcomes.models import calculate_po_score

po = ProgramOutcome.objects.get(code='PO-A')
student = Student.objects.get(id=1)
score = calculate_po_score(po, student)
# Returns: 88.0
```

---

## Formula 3: Final PO Score Across Multiple Courses

### Option A: Credit-Weighted (Default)
```
PO_Final = Σ(PO_from_course * CourseCredit) / Σ(CourseCredit)
```

#### Example
If PO-A appears in three courses:
- CS201 (3 credits): PO-A = 88.0%
- CS301 (4 credits): PO-A = 92.0%
- CS302 (3 credits): PO-A = 85.0%

**Calculation:**
```
PO-A_Final = (88 * 3) + (92 * 4) + (85 * 3)
             ─────────────────────────────
                   3 + 4 + 3

           = 264 + 368 + 255
             ───────────────
                   10

           = 887 / 10
           = 88.7%
```

### Option B: Simple Average
```
PO_Final = Σ(PO_from_course) / Number_of_Courses
```

#### Example (same data)
```
PO-A_Final = (88.0 + 92.0 + 85.0) / 3
           = 265.0 / 3
           = 88.33%
```

### Implementation
```python
from outcomes.models import calculate_all_po_scores

student = Student.objects.get(id=1)

# With credit weighting
po_scores = calculate_all_po_scores(student, use_credits=True)

# Without credit weighting (simple average)
po_scores = calculate_all_po_scores(student, use_credits=False)

for po, score in po_scores.items():
    print(f"{po.code}: {score:.2f}%")
```

---

## Complete Example Scenario

### Setup
- **Student**: Alice Johnson
- **Course**: CS201 (3 credits)
- **Learning Outcomes**: CLO-1, CLO-2
- **Program Outcome**: PO-A

### Step 1: Record Assessment Scores
```python
# Alice's scores in CS201
Quiz1: 85/100 (contributes 20% to CLO-1)
Midterm: 90/100 (contributes 30% to CLO-1)
Final: 88/100 (contributes 50% to CLO-1)

Project: 95/100 (contributes 40% to CLO-2)
Presentation: 90/100 (contributes 60% to CLO-2)
```

### Step 2: Calculate LO Scores
```python
CLO-1 = (85 * 0.20) + (90 * 0.30) + (88 * 0.50) = 88.0%
CLO-2 = (95 * 0.40) + (90 * 0.60) = 92.0%
```

### Step 3: Calculate PO Score (for CS201)
```python
# CLO-1 → PO-A with weight 5
# CLO-2 → PO-A with weight 3

PO-A (CS201) = (88 * 5) + (92 * 3) / (5 + 3)
             = (440 + 276) / 8
             = 89.5%
```

### Step 4: Calculate Final PO Score (across all courses)
If Alice completed CS201, CS301, CS302:
```python
PO-A (CS201, 3 credits): 89.5%
PO-A (CS301, 4 credits): 92.0%
PO-A (CS302, 3 credits): 86.0%

PO-A_Final = (89.5 * 3) + (92.0 * 4) + (86.0 * 3) / (3 + 4 + 3)
           = (268.5 + 368.0 + 258.0) / 10
           = 894.5 / 10
           = 89.45%
```

---

## API Usage

### Calculate LO Scores
```bash
POST /api/student-scores/calculate_lo_scores/
Content-Type: application/json

{
  "student_id": 1,
  "course_id": 2
}
```

### Calculate PO Scores
```bash
POST /api/student-scores/calculate_po_scores/
Content-Type: application/json

{
  "student_id": 1,
  "use_credits": true
}
```

### Get Comprehensive Summary
```bash
POST /api/student-scores/student_po_summary/
Content-Type: application/json

{
  "student_id": 1
}
```

---

## Achievement Level Thresholds

| Score Range | Achievement Level |
|-------------|-------------------|
| ≥ 85%       | EXCEEDED          |
| 70-84%      | ACHIEVED          |
| 50-69%      | PARTIALLY         |
| < 50%       | NOT_ACHIEVED      |

---

## Notes

- All percentages are stored as 0-100 (not 0-1)
- Weights for LO→PO are on 1-5 scale
- Assessment contributions are percentages (0-100)
- Credits are used for course weighting in final PO calculation
- Completed enrollments (status='COMPLETED') are used in calculations
