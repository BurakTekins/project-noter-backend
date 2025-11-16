# 📚 Assessment Calculation System - Documentation Index

## 🎯 Quick Navigation

### For First-Time Users
1. **Start here**: [QUICKSTART_CALCULATIONS.md](QUICKSTART_CALCULATIONS.md)
2. **Understand the math**: [FORMULAS.md](FORMULAS.md)
3. **See the architecture**: [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)

### For Developers
1. **Implementation details**: [CALCULATION_IMPLEMENTATION.md](CALCULATION_IMPLEMENTATION.md)
2. **Usage guide**: [CALCULATION_USAGE.md](CALCULATION_USAGE.md)
3. **Complete summary**: [README_CALCULATIONS.md](README_CALCULATIONS.md)

---

## 📖 Documentation Files

### 🚀 [QUICKSTART_CALCULATIONS.md](QUICKSTART_CALCULATIONS.md)
**Best for**: Getting started quickly  
**Contents**:
- 5-minute setup instructions
- Common API calls with examples
- Quick Python code snippets
- Verification checklist

### 🔢 [FORMULAS.md](FORMULAS.md)
**Best for**: Understanding the mathematics  
**Contents**:
- All three calculation formulas explained
- Step-by-step examples with numbers
- Complete scenario walkthrough
- Achievement level thresholds

### 🏗️ [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)
**Best for**: Visual learners  
**Contents**:
- System architecture diagram
- Data flow visualization
- Database schema
- API call flow

### 📋 [CALCULATION_USAGE.md](CALCULATION_USAGE.md)
**Best for**: Detailed usage instructions  
**Contents**:
- Complete Python function reference
- API endpoint documentation
- Setup requirements
- Code examples for all operations

### 🛠️ [CALCULATION_IMPLEMENTATION.md](CALCULATION_IMPLEMENTATION.md)
**Best for**: Understanding what was built  
**Contents**:
- Complete list of changes
- Files modified/created
- Technical architecture
- Testing instructions

### ✅ [README_CALCULATIONS.md](README_CALCULATIONS.md)
**Best for**: Comprehensive overview  
**Contents**:
- Complete feature summary
- All endpoints listed
- Usage examples
- Verification steps

---

## 🎓 Learning Path

### Level 1: Beginner
```
1. Read: QUICKSTART_CALCULATIONS.md
2. Try: Run test calculations
3. Explore: Django admin interface
```

### Level 2: Intermediate
```
1. Read: FORMULAS.md
2. Study: ARCHITECTURE_DIAGRAM.md
3. Practice: Create mappings via API
```

### Level 3: Advanced
```
1. Read: CALCULATION_USAGE.md
2. Review: CALCULATION_IMPLEMENTATION.md
3. Customize: Extend calculation functions
```

---

## 🔍 Find What You Need

### "How do I...?"

#### ...calculate LO scores?
→ **FORMULAS.md** - Section: Formula 1  
→ **CALCULATION_USAGE.md** - Section: Calculate LO Score  
→ **QUICKSTART_CALCULATIONS.md** - Section: Calculate LO Scores

#### ...calculate PO scores?
→ **FORMULAS.md** - Section: Formula 2 & 3  
→ **CALCULATION_USAGE.md** - Section: Calculate PO Score  
→ **QUICKSTART_CALCULATIONS.md** - Section: Calculate PO Scores

#### ...use the API?
→ **QUICKSTART_CALCULATIONS.md** - Section: Common Tasks  
→ **CALCULATION_USAGE.md** - Section: API Endpoints  
→ **README_CALCULATIONS.md** - Section: Complete Endpoint List

#### ...understand the system design?
→ **ARCHITECTURE_DIAGRAM.md** - All sections  
→ **CALCULATION_IMPLEMENTATION.md** - Section: System Architecture

#### ...set up the mappings?
→ **CALCULATION_USAGE.md** - Section: Setup Requirements  
→ **QUICKSTART_CALCULATIONS.md** - Section: Common Tasks

#### ...test the system?
→ **QUICKSTART_CALCULATIONS.md** - Section: Test the System  
→ **CALCULATION_IMPLEMENTATION.md** - Section: Testing

---

## 📊 What's Implemented

### ✅ Models (3 new)
- **AssessmentLOMapping** - Links assessments to learning outcomes
- **LOPOMapping** - Links learning outcomes to program outcomes  
- **StudentAssessmentScore** - Stores student scores

### ✅ Functions (5 new)
- `calculate_lo_score()` - Assessment → LO calculation
- `calculate_po_score()` - LO → PO calculation
- `calculate_all_po_scores()` - All POs for a student
- `calculate_student_lo_scores()` - All LOs for a student
- `get_student_po_summary()` - Comprehensive summary

### ✅ API Endpoints (6 new)
- `/api/assessment-lo-mappings/` - CRUD operations
- `/api/lo-po-mappings/` - CRUD operations
- `/api/student-scores/` - CRUD operations
- `/api/student-scores/calculate_lo_scores/` - Calculate LOs
- `/api/student-scores/calculate_po_scores/` - Calculate POs
- `/api/student-scores/student_po_summary/` - Get summary

---

## 🧪 Testing Resources

### Test Script
```bash
python manage.py shell < test_calculations.py
```
Located in project root, tests all calculation functions.

### Manual Testing
See **QUICKSTART_CALCULATIONS.md** for:
- Shell commands
- API curl examples
- Python code snippets

---

## 📞 Support

### Troubleshooting
1. Check **QUICKSTART_CALCULATIONS.md** - Verification Checklist
2. Run migrations: `python manage.py migrate`
3. Test imports: `python manage.py shell`
4. Check logs for errors

### Common Issues
- **Import errors**: Ensure migrations are applied
- **Zero scores**: Check that mappings exist
- **Missing data**: Verify test data is populated

---

## 📝 File Quick Reference

| File | Purpose | Size |
|------|---------|------|
| QUICKSTART_CALCULATIONS.md | Quick start guide | Short |
| FORMULAS.md | Mathematical formulas | Medium |
| ARCHITECTURE_DIAGRAM.md | Visual diagrams | Medium |
| CALCULATION_USAGE.md | Detailed usage | Long |
| CALCULATION_IMPLEMENTATION.md | Technical details | Long |
| README_CALCULATIONS.md | Complete overview | Long |
| test_calculations.py | Test script | Short |

---

## 🎯 Use Cases

### For Instructors
**Need**: Record student grades and calculate outcomes  
**Read**: QUICKSTART_CALCULATIONS.md → FORMULAS.md  
**Use**: Django admin interface + API endpoints

### For Developers
**Need**: Integrate calculations into frontend  
**Read**: CALCULATION_USAGE.md → ARCHITECTURE_DIAGRAM.md  
**Use**: REST API endpoints

### For Administrators
**Need**: Understand system and manage data  
**Read**: README_CALCULATIONS.md → ARCHITECTURE_DIAGRAM.md  
**Use**: Django admin interface

### For Quality Assurance
**Need**: Setup and test the system  
**Read**: CALCULATION_IMPLEMENTATION.md → QUICKSTART_CALCULATIONS.md  
**Use**: Test script + API testing

---

## 🔄 System Flow Summary

```
1. Create Assessments (Quizzes, Exams, Projects)
   └─→ Create Assessment-LO Mappings (contribution %)
       └─→ Record Student Scores
           └─→ Calculate LO Scores (Formula 1)
               └─→ Create LO-PO Mappings (weight 1-5)
                   └─→ Calculate PO Scores (Formula 2)
                       └─→ Combine Across Courses (Formula 3)
```

---

## ✨ Next Steps

1. **New to the system?**  
   → Start with **QUICKSTART_CALCULATIONS.md**

2. **Want to understand the math?**  
   → Read **FORMULAS.md**

3. **Ready to implement?**  
   → Follow **CALCULATION_USAGE.md**

4. **Need technical details?**  
   → Review **CALCULATION_IMPLEMENTATION.md**

5. **Want the big picture?**  
   → Check **README_CALCULATIONS.md**

---

## 📅 Version Information

- **Implementation Date**: November 2025
- **Django Version**: 5.2.7
- **DRF Version**: 3.15.2
- **Database**: PostgreSQL

---

## 🎉 Ready to Start!

Choose your path:
- 🚀 **Quick Start**: QUICKSTART_CALCULATIONS.md
- 📚 **Learn More**: FORMULAS.md
- 🔧 **Build**: CALCULATION_USAGE.md
- 📖 **Reference**: README_CALCULATIONS.md
