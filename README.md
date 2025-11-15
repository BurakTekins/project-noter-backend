# Project Noter - Engineering Program Learning Outcomes Tracker

A comprehensive Django REST Framework backend system for tracking and managing **Program Learning Outcomes (PLOs)** in engineering education programs.

## 🎯 Project Overview

This system helps educational institutions track student achievement of the **11 Program Learning Outcomes** defined for engineering programs, including:

1. **Mathematics & Engineering Knowledge**
2. **Problem Analysis & Solution**
3. **Design & Development**
4. **Modern Tools & IT**
5. **Research & Experimentation**
6. **Teamwork & Individual Work**
7. **Communication Skills**
8. **Lifelong Learning**
9. **Ethics & Professional Responsibility**
10. **Project Management & Entrepreneurship**
11. **Social Impact & Legal Awareness**

## 📦 Features

### Core Entities
- **Students**: Track student information, enrollment, GPA, and graduation status
- **Courses**: Manage course catalog with prerequisites and PLO mappings
- **Professors**: Faculty information and course assignments
- **Program Learning Outcomes (PLOs)**: The 11 defined learning outcomes

### Advanced Tracking
- **Enrollments**: Student course enrollments with grades and PLO assessments
- **Course Offerings**: Semester-specific course sections with professor assignments
- **Course-PLO Mappings**: Define which PLOs each course addresses and at what level
- **Student PLO Achievements**: Track individual student progress on each PLO

### API Features
- RESTful API endpoints for all entities
- Filtering, searching, and pagination
- PLO achievement analytics and reporting
- Student progress tracking
- Course-level PLO statistics

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project-noter-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Populate the 11 Program Learning Outcomes**
   ```bash
   python manage.py populate_plos
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## 📚 API Endpoints

### Students
- `GET/POST /api/students/` - List/Create students
- `GET/PUT/DELETE /api/students/{id}/` - Retrieve/Update/Delete student

### Courses
- `GET/POST /api/courses/` - List/Create courses
- `GET/PUT/DELETE /api/courses/{id}/` - Retrieve/Update/Delete course

### Professors
- `GET/POST /api/professors/` - List/Create professors
- `GET/PUT/DELETE /api/professors/{id}/` - Retrieve/Update/Delete professor

### Program Learning Outcomes
- `GET/POST /api/plos/` - List/Create PLOs
- `GET /api/plos/active/` - Get active PLOs only
- `GET/PUT/DELETE /api/plos/{id}/` - Retrieve/Update/Delete PLO

### Enrollments
- `GET/POST /api/enrollments/` - List/Create enrollments
- `GET /api/enrollments/by_student/?student_id={id}` - Get student's enrollments
- `GET /api/enrollments/by_course/?course_id={id}` - Get course enrollments
- `GET/PUT/DELETE /api/enrollments/{id}/` - Retrieve/Update/Delete enrollment

### Course Offerings
- `GET/POST /api/offerings/` - List/Create course offerings
- `GET /api/offerings/current_semester/?semester=FALL&year=2025` - Current offerings
- `GET/PUT/DELETE /api/offerings/{id}/` - Retrieve/Update/Delete offering

### Course-PLO Mappings
- `GET/POST /api/course-plo-mappings/` - List/Create mappings
- `GET /api/course-plo-mappings/by_course/?course_id={id}` - PLOs for a course
- `GET /api/course-plo-mappings/by_plo/?plo_id={id}` - Courses for a PLO
- `GET/PUT/DELETE /api/course-plo-mappings/{id}/` - Retrieve/Update/Delete mapping

### Student PLO Achievements
- `GET/POST /api/achievements/` - List/Create achievements
- `GET /api/achievements/student_summary/?student_id={id}` - Student's PLO summary
- `GET /api/achievements/plo_statistics/?plo_id={id}` - PLO statistics across students
- `GET/PUT/DELETE /api/achievements/{id}/` - Retrieve/Update/Delete achievement

## 🗄️ Database Schema

### Key Relationships
```
Student ← Enrollment → Course → CoursePLOMapping → ProgramLearningOutcome
                ↓                      ↓
           StudentPLOAchievement   (tracks PLO progress)

Professor ← CourseOffering → Course
```

### Enrollment Grades
- AA (4.0), BA (3.5), BB (3.0), CB (2.5), CC (2.0), DC (1.5), DD (1.0), FD (0.5), FF (0.0)

### PLO Contribution Levels
- **Introductory (1)**: Course introduces the PLO
- **Reinforcing (2)**: Course reinforces the PLO
- **Mastery (3)**: Course expects mastery of the PLO

### Achievement Levels
- **Not Achieved**: Student did not meet PLO standards
- **Partially Achieved**: Partial demonstration of PLO
- **Achieved**: Student demonstrated the PLO
- **Exceeded**: Student exceeded PLO expectations

## 🔐 Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` to:
- Manage all entities through a user-friendly interface
- Bulk import/export data
- View relationships and statistics

## 📊 Example Usage

### 1. Create a Course-PLO Mapping
```json
POST /api/course-plo-mappings/
{
  "course": 1,
  "plo": 2,
  "contribution_level": "MASTERY",
  "assessment_method": "Project-based evaluation and final exam",
  "weight_percentage": 25
}
```

### 2. Track Student Achievement
```json
POST /api/achievements/
{
  "student": 1,
  "plo": 2,
  "enrollment": 5,
  "achievement_level": "ACHIEVED",
  "score": 85.5,
  "notes": "Strong problem-solving skills demonstrated in project"
}
```

### 3. Get Student PLO Summary
```
GET /api/achievements/student_summary/?student_id=1
```

Response:
```json
{
  "student_id": 1,
  "plo_achievements": [
    {
      "plo__number": 1,
      "plo__short_name": "Mathematics & Engineering Knowledge",
      "avg_score": 82.3,
      "assessment_count": 3
    },
    ...
  ],
  "total_assessments": 25
}
```

## 🛠️ Technology Stack

- **Framework**: Django 5.2.7
- **API**: Django REST Framework 3.15.2
- **Filtering**: django-filter 24.3
- **Database**: SQLite (development) / PostgreSQL (production recommended)

## 📝 Development Notes

### Next Steps for Production
1. Set up environment variables for sensitive data
2. Configure PostgreSQL database
3. Add JWT authentication
4. Implement role-based permissions (Admin, Professor, Student)
5. Add CORS for frontend integration
6. Set up Docker containerization
7. Add API documentation (drf-spectacular)
8. Implement file uploads for reports
9. Add email notifications
10. Create data visualization endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

[Add your license information]

## 👥 Contact

[Add contact information]