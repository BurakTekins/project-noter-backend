
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def verify_persistence():
    course_id = 1
    
    # 1. Setup: Get or Create Assessment and LO
    print("--- Setup ---")
    
    # Get LO
    resp = requests.get(f"{BASE_URL}/courses/{course_id}/learning-outcomes/")
    if resp.status_code != 200:
        print("Failed to list LOs")
        return False
    los = resp.json()
    if not los:
        # Create LO
        resp = requests.post(f"{BASE_URL}/courses/{course_id}/learning-outcomes/", json={
            "code": "TEST-LO-1",
            "description": "Test LO"
        })
        if resp.status_code != 201:
            print("Failed to create LO")
            return False
        lo_code = "TEST-LO-1"
    else:
        lo_code = los[0]['code']
    print(f"Using LO: {lo_code}")

    # Get Assessment
    resp = requests.get(f"{BASE_URL}/courses/{course_id}/assessments/")
    if resp.status_code != 200:
        print("Failed to list Assessments")
        return False
    assessments = resp.json()
    if not assessments:
        # Create Assessment
        resp = requests.post(f"{BASE_URL}/courses/{course_id}/assessments/", json={
            "title": "Persistence Test Exam",
            "type": "Exam",
            "weight": 20
        })
        if resp.status_code != 201:
            print("Failed to create Assessment")
            return False
        assessment_id = resp.json()['id']
    else:
        assessment_id = assessments[0]['id']
    print(f"Using Assessment ID: {assessment_id}")

    # Get a Student ID (nested from enrollment)
    resp = requests.get(f"{BASE_URL}/courses/{course_id}/enrollments/")
    if resp.status_code == 200 and resp.json():
        student_id = resp.json()[0]['student']['id']
    else:
        print("No student found. Cannot test grades.")
        return False
    print(f"Using Student ID: {student_id}")


    # 2. Test Assessment Update (PUT)
    print("\n--- Testing Assessment Persistence ---")
    update_payload = {
        "id": assessment_id,
        "name": "Updated Exam Name",
        "studentGrades": {
            str(student_id): 95.5
        },
        "connections": [
            { "type": "learning", "targetId": lo_code, "percentageIndex": 0 }
        ],
        "percentages": [45] # 45% contribution
    }
    
    url = f"{BASE_URL}/courses/{course_id}/assessments/{assessment_id}/"
    resp = requests.put(url, json=update_payload)
    
    if resp.status_code != 200:
        print(f"❌ PUT Assessment Failed: {resp.text}")
        return False
    else:
        print("✅ PUT Assessment Request Successful")
        data = resp.json()
        if data['name'] != "Updated Exam Name":
            print(f"❌ Name did not update. Got: {data.get('name')}")
            return False
            
    # Verify Grades
    print("   Verifying Grades stored...")
    resp = requests.get(f"{BASE_URL}/courses/{course_id}/grades/")
    grades = resp.json()
    found_grade = False
    for g in grades:
        if g['assessment_id'] == assessment_id and g['student_id'] == student_id:
            if g['score'] == 95.5:
                print("✅ Grade 95.5 found in DB")
                found_grade = True
            else:
                print(f"❌ Grade found but score mismatch: {g['score']}")
    if not found_grade:
        print("❌ Grade not found in DB")
        return False

    # Verify Connections
    print("   Verifying Connections stored...")
    resp = requests.get(f"{BASE_URL}/courses/{course_id}/assessments/{assessment_id}/lo-connections/")
    connections = resp.json()
    found_conn = False
    for c in connections:
        if c['learning_outcome_id'] == lo_code and c['weight'] == 45:
            print("✅ Connection to LO with weight 45 found")
            found_conn = True
    if not found_conn:
        print(f"❌ Connection not found. Data: {json.dumps(connections)}")
        return False
        
    print("\n--- Testing GET Response Format ---")
    
    # 1. Check Course Assessment List for studentGrades
    print("   Checking GET /courses/{id}/assessments/...")
    resp = requests.get(f"{BASE_URL}/courses/{course_id}/assessments/")
    if resp.status_code == 200:
        assessments_list = resp.json()
        target_ass = next((a for a in assessments_list if a['id'] == assessment_id), None)
        if target_ass:
            if 'studentGrades' in target_ass:
                grades_map = target_ass['studentGrades']
                if str(student_id) in grades_map and grades_map[str(student_id)] == 95.5:
                     print("✅ studentGrades field present and correct in Assessment List")
                else:
                     print(f"❌ studentGrades content mismatch: {grades_map}")
                     return False
            else:
                print("❌ studentGrades field MISSING in Assessment List")
                return False
        else:
             print("❌ Created assessment not found in list")
             return False
    else:
        print("❌ Failed to list assessments")
        return False

    # 2. Check Student Assessment Endpoint
    print(f"   Checking GET /students/{student_id}/assessments/...")
    resp = requests.get(f"{BASE_URL}/students/{student_id}/assessments/")
    if resp.status_code == 200:
        student_assessments = resp.json()
        target_s_ass = next((a for a in student_assessments if a['id'] == assessment_id), None)
        if target_s_ass:
            if 'score' in target_s_ass and target_s_ass['score'] == 95.5:
                print("✅ specific score present and correct in Student Assessment View")
            else:
                 print(f"❌ score mismatch or missing: {target_s_ass}")
                 return False
        else:
             print("❌ Assessment not found in Student View")
             return False
    else:
        print(f"❌ Failed to get student assessments. Status: {resp.status_code}. Response: {resp.text}")
        return False

    # 3. Test LO Update (PUT) - Optional context verification
    # Assuming Program Outcomes exist or I'd need to create one. Skipping specific PO test if no POs exist.
    
    return True

if __name__ == "__main__":
    success = verify_persistence()
    sys.exit(0 if success else 1)
