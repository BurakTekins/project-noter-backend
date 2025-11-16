# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ASSESSMENT CALCULATION SYSTEM                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: ASSESSMENTS (Individual Tests/Projects)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┏━━━━━━━━━━━━━━┓  ┏━━━━━━━━━━━━━━┓  ┏━━━━━━━━━━━━━━┓                      │
│  ┃   Quiz 1     ┃  ┃   Midterm    ┃  ┃    Final     ┃                      │
│  ┃  Max: 100    ┃  ┃  Max: 100    ┃  ┃  Max: 100    ┃                      │
│  ┃  Weight: 20% ┃  ┃  Weight: 30% ┃  ┃  Weight: 50% ┃                      │
│  ┗━━━━━━━━━━━━━━┛  ┗━━━━━━━━━━━━━━┛  ┗━━━━━━━━━━━━━━┛                      │
│        │                  │                  │                                │
│    Alice: 85         Alice: 90         Alice: 88                             │
│        │                  │                  │                                │
│        └──────────────────┴──────────────────┘                               │
│                           │                                                   │
│                    AssessmentLOMapping                                        │
│                   (contribution_percentage)                                   │
│                           │                                                   │
│                           ▼                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: LEARNING OUTCOMES (Course-Level Goals)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓                 │
│  ┃  CLO-1: Data Structures Knowledge                      ┃                 │
│  ┃  Score: 88.0% (calculated from assessments)            ┃                 │
│  ┃  Formula: (85*0.20) + (90*0.30) + (88*0.50)            ┃                 │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛                 │
│                                                                               │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓                 │
│  ┃  CLO-2: Algorithm Design                               ┃                 │
│  ┃  Score: 92.0%                                           ┃                 │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛                 │
│                           │                                                   │
│                      LOPOMapping                                              │
│                    (weight: 1-5 scale)                                        │
│                           │                                                   │
│                           ▼                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: PROGRAM OUTCOMES (Program-Wide Competencies)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓   │
│  ┃  PO-A: Technical Excellence                                           ┃   │
│  ┃  Score: 89.5% (from CS201)                                            ┃   │
│  ┃  Formula: (88*5 + 92*3) / (5+3)                                       ┃   │
│  ┃  CLO-1 contributes with weight 5                                      ┃   │
│  ┃  CLO-2 contributes with weight 3                                      ┃   │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛   │
│                                                                               │
│                                   │                                           │
│                      Credit Weighting Across Courses                          │
│                                   │                                           │
│                                   ▼                                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FINAL: PROGRAM OUTCOME ACROSS ALL COURSES                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓   │
│  ┃  PO-A: Technical Excellence - FINAL SCORE                             ┃   │
│  ┃  Score: 89.45%                                                         ┃   │
│  ┃  Formula: (89.5*3 + 92.0*4 + 86.0*3) / (3+4+3)                        ┃   │
│  ┃                                                                        ┃   │
│  ┃  Contributing Courses:                                                 ┃   │
│  ┃    - CS201 (3 credits): 89.5%                                         ┃   │
│  ┃    - CS301 (4 credits): 92.0%                                         ┃   │
│  ┃    - CS302 (3 credits): 86.0%                                         ┃   │
│  ┃                                                                        ┃   │
│  ┃  Achievement Level: EXCEEDED (≥85%)                                   ┃   │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

```
Student: Alice Johnson
Course: CS201 - Data Structures (3 credits)

┌──────────────────┐
│ Step 1: Record   │
│ Assessment       │
│ Scores           │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Quiz 1: 85/100                  │
│ Midterm: 90/100                 │
│ Final: 88/100                   │
└────────┬────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Step 2: Map      │
│ Assessments      │
│ to LOs           │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Quiz → CLO-1: 20%               │
│ Midterm → CLO-1: 30%            │
│ Final → CLO-1: 50%              │
└────────┬────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Step 3: Calculate│
│ LO Score         │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────┐
│ CLO-1 Score: 88.0%              │
│ (85*0.20 + 90*0.30 + 88*0.50)   │
└────────┬────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Step 4: Map      │
│ LOs to POs       │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────┐
│ CLO-1 → PO-A: weight 5          │
│ CLO-2 → PO-A: weight 3          │
└────────┬────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Step 5: Calculate│
│ PO Score         │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────┐
│ PO-A (CS201): 89.5%             │
│ (88*5 + 92*3) / (5+3)           │
└────────┬────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Step 6: Combine  │
│ Across Courses   │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────┐
│ PO-A Final: 89.45%              │
│ Credit-weighted across          │
│ CS201, CS301, CS302             │
└─────────────────────────────────┘
```

## Database Schema

```
┌─────────────────────────┐
│   Assessment            │
├─────────────────────────┤
│ id                      │
│ name                    │
│ max_score               │
│ weight_percentage       │
└───────┬─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────────────┐      ┌─────────────────────────┐
│ StudentAssessmentScore  │  N:1 │   Enrollment            │
├─────────────────────────┤◄─────┤─────────────────────────┤
│ id                      │      │ id                      │
│ student_id              │      │ student_id              │
│ assessment_id           │      │ course_id               │
│ enrollment_id           │      │ semester, year          │
│ score                   │      │ status                  │
└─────────────────────────┘      └─────────────────────────┘

┌─────────────────────────┐      ┌─────────────────────────┐
│ AssessmentLOMapping     │  N:1 │   LearningOutcome       │
├─────────────────────────┤◄─────┤─────────────────────────┤
│ id                      │      │ id                      │
│ assessment_id           │      │ course_id               │
│ learning_outcome_id     │      │ code                    │
│ contribution_percentage │      │ description             │
└─────────────────────────┘      └───────┬─────────────────┘
                                         │
                                         │ 1:N
                                         ▼
┌─────────────────────────┐      ┌─────────────────────────┐
│ LOPOMapping             │  N:1 │   ProgramOutcome        │
├─────────────────────────┤◄─────┤─────────────────────────┤
│ id                      │      │ id                      │
│ learning_outcome_id     │      │ code                    │
│ program_outcome_id      │      │ title                   │
│ weight (1-5)            │      │ description             │
└─────────────────────────┘      └─────────────────────────┘
```

## API Call Flow

```
Frontend/Client
      │
      │ POST /api/student-scores/calculate_po_scores/
      │ Body: {"student_id": 1, "use_credits": true}
      ▼
StudentAssessmentScoreViewSet
      │
      │ calls
      ▼
calculate_all_po_scores(student, use_credits=True)
      │
      │ for each ProgramOutcome
      ▼
calculate_po_score(po, student, course)
      │
      │ for each LearningOutcome
      ▼
calculate_lo_score(lo, student, enrollment)
      │
      │ queries
      ▼
StudentAssessmentScore records
      │
      │ applies formulas
      ▼
Returns JSON Response:
{
  "student": "Alice Johnson",
  "use_credits": true,
  "po_scores": [
    {
      "po_code": "PO-A",
      "title": "Technical Excellence",
      "score": 89.45
    },
    ...
  ]
}
```
