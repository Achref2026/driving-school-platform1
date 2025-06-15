#!/bin/bash

echo "=== COMPREHENSIVE BACKEND WORKFLOW TESTING ==="
echo ""

BASE_URL="http://localhost:8001/api"

# 1. Create Manager and School
echo "1. Creating Manager and Driving School..."
MANAGER_REG=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=manager_test@example.com&password=testpass123&first_name=Manager&last_name=Test&phone=0555111111&address=Manager St&date_of_birth=1980-01-01&gender=male&state=Alger")

MANAGER_TOKEN=$(echo "$MANAGER_REG" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "Manager Token: ${MANAGER_TOKEN:0:50}..."

# Create driving school
SCHOOL_RESPONSE=$(curl -s -X POST "$BASE_URL/driving-schools" \
  -H "Authorization: Bearer $MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Comprehensive Test School",
    "address": "123 Test Street",
    "state": "Alger",
    "phone": "+213 21 111 111",
    "email": "test_school@example.com",
    "description": "A comprehensive test driving school",
    "price": 30000.0
  }')

SCHOOL_ID=$(echo "$SCHOOL_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "School ID: $SCHOOL_ID"

# 2. Create Student and Enroll
echo ""
echo "2. Creating Student and Enrolling..."
STUDENT_REG=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=student_test@example.com&password=testpass123&first_name=Student&last_name=Test&phone=0555222222&address=Student St&date_of_birth=1995-01-01&gender=female&state=Alger")

STUDENT_TOKEN=$(echo "$STUDENT_REG" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "Student Token: ${STUDENT_TOKEN:0:50}..."

# Enroll in school
ENROLLMENT_RESPONSE=$(curl -s -X POST "$BASE_URL/enrollments" \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"school_id\": \"$SCHOOL_ID\"}")

ENROLLMENT_ID=$(echo "$ENROLLMENT_RESPONSE" | grep -o '"enrollment_id":"[^"]*"' | cut -d'"' -f4)
echo "Enrollment ID: $ENROLLMENT_ID"

# 3. Manager views enrollments
echo ""
echo "3. Testing Manager Views Enrollments..."
MANAGER_ENROLLMENTS=$(curl -s -X GET "$BASE_URL/manager/enrollments" \
  -H "Authorization: Bearer $MANAGER_TOKEN")
echo "Manager can see enrollments: $(echo "$MANAGER_ENROLLMENTS" | grep -o 'student_test@example.com' || echo 'NO')"

# 4. Manager approves enrollment
echo ""
echo "4. Testing Manager Approval..."
APPROVAL_RESPONSE=$(curl -s -X POST "$BASE_URL/manager/enrollments/$ENROLLMENT_ID/approve" \
  -H "Authorization: Bearer $MANAGER_TOKEN")
echo "Approval Response: $APPROVAL_RESPONSE"

# 5. Test other endpoints
echo ""
echo "5. Testing Additional Endpoints..."

# Analytics
echo "Testing Analytics..."
ANALYTICS=$(curl -s -X GET "$BASE_URL/analytics/school-overview" \
  -H "Authorization: Bearer $MANAGER_TOKEN")
echo "Analytics Working: $(echo "$ANALYTICS" | grep -o 'total_students' | head -1 || echo 'NO')"

# Quizzes
echo "Testing Quizzes..."
QUIZZES=$(curl -s -X GET "$BASE_URL/quizzes" \
  -H "Authorization: Bearer $STUDENT_TOKEN")
echo "Quizzes Working: $(echo "$QUIZZES" | grep -o '\[\]' || echo 'ERROR')"

# Notifications
echo "Testing Notifications..."
NOTIFICATIONS=$(curl -s -X GET "$BASE_URL/notifications/my" \
  -H "Authorization: Bearer $STUDENT_TOKEN")
echo "Notifications Working: $(echo "$NOTIFICATIONS" | grep -o '\[\]' || echo 'ERROR')"

# Certificates
echo "Testing Certificates..."
CERTIFICATES=$(curl -s -X GET "$BASE_URL/certificates/my" \
  -H "Authorization: Bearer $STUDENT_TOKEN")
echo "Certificates Working: $(echo "$CERTIFICATES" | grep -o '\[\]' || echo 'ERROR')"

echo ""
echo "=== WORKFLOW TESTING COMPLETED ==="