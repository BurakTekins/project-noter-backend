#!/bin/bash

echo "Testing Calculation Endpoints"
echo "=============================="
echo ""

BASE_URL="http://127.0.0.1:8000"

# Get first student ID
echo "1. Fetching first student..."
STUDENT_ID=$(curl -s "${BASE_URL}/api/students/" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['results'][0]['id'] if data.get('results') else 'N/A')")
echo "   Student ID: $STUDENT_ID"
echo ""

# Get first course ID
echo "2. Fetching first course..."
COURSE_ID=$(curl -s "${BASE_URL}/api/courses/" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['results'][0]['id'] if data.get('results') else 'N/A')")
echo "   Course ID: $COURSE_ID"
echo ""

echo "3. Testing Calculate LO Scores endpoint..."
echo "   POST ${BASE_URL}/api/student-scores/calculate_lo_scores/"
curl -X POST "${BASE_URL}/api/student-scores/calculate_lo_scores/" \
  -H "Content-Type: application/json" \
  -d "{\"student_id\": ${STUDENT_ID}, \"course_id\": ${COURSE_ID}}" \
  2>/dev/null | python3 -m json.tool
echo ""

echo "4. Testing Calculate PO Scores endpoint..."
echo "   POST ${BASE_URL}/api/student-scores/calculate_po_scores/"
curl -X POST "${BASE_URL}/api/student-scores/calculate_po_scores/" \
  -H "Content-Type: application/json" \
  -d "{\"student_id\": ${STUDENT_ID}, \"use_credits\": true}" \
  2>/dev/null | python3 -m json.tool
echo ""

echo "5. Testing Student PO Summary endpoint..."
echo "   POST ${BASE_URL}/api/student-scores/student_po_summary/"
curl -X POST "${BASE_URL}/api/student-scores/student_po_summary/" \
  -H "Content-Type: application/json" \
  -d "{\"student_id\": ${STUDENT_ID}}" \
  2>/dev/null | python3 -m json.tool
echo ""

echo "=============================="
echo "Testing Complete!"
