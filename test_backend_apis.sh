#!/bin/bash

# Backend API Testing Script
echo "=== DRIVING SCHOOL PLATFORM - BACKEND API TESTING ==="
echo ""

BASE_URL="http://localhost:8001/api"
TOKEN=""

# Test 1: Health Check
echo "1. Testing Health Check..."
RESPONSE=$(curl -s -X GET "$BASE_URL/health")
echo "Response: $RESPONSE"
echo ""

# Test 2: Get States
echo "2. Testing Get States..."
RESPONSE=$(curl -s -X GET "$BASE_URL/states")
echo "Response: $RESPONSE" | head -c 200
echo "..."
echo ""

# Test 3: User Registration
echo "3. Testing User Registration..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=testuser@example.com&password=testpass123&first_name=Test&last_name=User&phone=0555123456&address=123 Test St&date_of_birth=1990-01-01&gender=male&state=Alger")
echo "Response: $RESPONSE"

# Extract token from response
TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "Extracted Token: $TOKEN"
echo ""

# Test 4: User Login
echo "4. Testing User Login..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"testpass123"}')
echo "Response: $RESPONSE"
echo ""

# Test 5: Get Driving Schools
echo "5. Testing Get Driving Schools..."
RESPONSE=$(curl -s -X GET "$BASE_URL/driving-schools")
echo "Response: $RESPONSE" | head -c 300
echo "..."
echo ""

# Test 6: Get User Dashboard
echo "6. Testing Get User Dashboard..."
RESPONSE=$(curl -s -X GET "$BASE_URL/dashboard" \
  -H "Authorization: Bearer $TOKEN")
echo "Response: $RESPONSE"
echo ""

# Test 7: Get User Documents
echo "7. Testing Get User Documents..."
RESPONSE=$(curl -s -X GET "$BASE_URL/documents" \
  -H "Authorization: Bearer $TOKEN")
echo "Response: $RESPONSE"
echo ""

# Test 8: Get User Enrollments
echo "8. Testing Get User Enrollments..."
RESPONSE=$(curl -s -X GET "$BASE_URL/enrollments/my" \
  -H "Authorization: Bearer $TOKEN")
echo "Response: $RESPONSE"
echo ""

# Test 9: Get User Notifications
echo "9. Testing Get User Notifications..."
RESPONSE=$(curl -s -X GET "$BASE_URL/notifications/my" \
  -H "Authorization: Bearer $TOKEN")
echo "Response: $RESPONSE"
echo ""

# Test 10: Get Quizzes
echo "10. Testing Get Available Quizzes..."
RESPONSE=$(curl -s -X GET "$BASE_URL/quizzes" \
  -H "Authorization: Bearer $TOKEN")
echo "Response: $RESPONSE"
echo ""

echo "=== BASIC API TESTING COMPLETED ==="