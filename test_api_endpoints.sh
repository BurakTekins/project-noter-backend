#!/bin/bash
# Backend endpoint'lerini curl ile test etmek için script
# Kullanım: bash test_api_endpoints.sh <student_id>

STUDENT_ID=${1:-1}
BASE_URL="http://localhost:8000/api"

echo "=========================================="
echo "Testing Backend Endpoints"
echo "Student ID: $STUDENT_ID"
echo "=========================================="
echo ""

# Test 1: Enrollments
echo "1. Testing /students/$STUDENT_ID/enrollments/"
echo "-------------------------------------------"
curl -s "$BASE_URL/students/$STUDENT_ID/enrollments/" | python -m json.tool
echo ""
echo ""

# Test 2: Courses
echo "2. Testing /students/$STUDENT_ID/courses/"
echo "-------------------------------------------"
curl -s "$BASE_URL/students/$STUDENT_ID/courses/" | python -m json.tool
echo ""
echo ""

# Test 3: Learning Outcomes
echo "3. Testing /students/$STUDENT_ID/learning-outcomes/"
echo "-------------------------------------------"
curl -s "$BASE_URL/students/$STUDENT_ID/learning-outcomes/" | python -m json.tool
echo ""
echo ""

echo "=========================================="
echo "Test Complete"
echo "=========================================="

