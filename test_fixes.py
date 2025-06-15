#!/usr/bin/env python3
"""Test all the fixed functionalities"""

import requests
import json
import time

BASE_URL = "http://localhost:8001/api"

def test_driving_schools_loading():
    """Test that driving schools load properly"""
    print("🔍 Testing driving schools loading...")
    
    response = requests.get(f"{BASE_URL}/driving-schools")
    data = response.json()
    
    if response.status_code == 200 and len(data.get('schools', [])) > 0:
        print(f"✅ Driving schools loading: SUCCESS - Found {len(data['schools'])} schools")
        return True
    else:
        print(f"❌ Driving schools loading: FAILED - {response.status_code}")
        return False

def test_manager_teacher_addition():
    """Test that managers can add teachers"""
    print("\n🔍 Testing manager teacher addition...")
    
    # Login as manager
    login_data = {'email': 'manager@test.com', 'password': 'password123'}
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Manager login failed: {login_response.status_code}")
        return False
    
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Add a new teacher
    teacher_data = {
        'email': f'newteacher{int(time.time())}@test.com',
        'first_name': 'New',
        'last_name': 'Teacher',
        'phone': '0213-21-999999',
        'address': '789 New Teacher Street',
        'date_of_birth': '1992-08-20',
        'gender': 'female',
        'can_teach_male': False,
        'can_teach_female': True
    }
    
    teacher_response = requests.post(f"{BASE_URL}/teachers/add", json=teacher_data, headers=headers)
    
    if teacher_response.status_code == 200:
        response_data = teacher_response.json()
        if 'teacher' in response_data and 'message' in response_data:
            print("✅ Manager teacher addition: SUCCESS")
            print(f"   - Added teacher: {response_data['teacher']['user_name']}")
            return True
        else:
            print(f"❌ Manager teacher addition: FAILED - Invalid response format")
            return False
    else:
        print(f"❌ Manager teacher addition: FAILED - {teacher_response.status_code}")
        print(f"   Error: {teacher_response.text}")
        return False

def test_manager_quiz_management():
    """Test that managers can see and edit quizzes"""
    print("\n🔍 Testing manager quiz management...")
    
    # Login as manager
    login_data = {'email': 'manager@test.com', 'password': 'password123'}
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Manager login failed: {login_response.status_code}")
        return False
    
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Test creating a quiz
    quiz_data = {
        'title': f'Test Quiz {int(time.time())}',
        'description': 'Test quiz for verification',
        'course_type': 'theory',
        'difficulty': 'easy',
        'passing_score': 75,
        'time_limit_minutes': 25,
        'questions': [{
            'question': 'What color is a stop sign?',
            'options': ['Red', 'Blue', 'Green', 'Yellow'],
            'correct_answer': 0,
            'explanation': 'Stop signs are always red.'
        }]
    }
    
    create_response = requests.post(f"{BASE_URL}/quizzes", json=quiz_data, headers=headers)
    
    if create_response.status_code != 200:
        print(f"❌ Quiz creation failed: {create_response.status_code}")
        print(f"   Error: {create_response.text}")
        return False
    
    # Test getting manager's quizzes
    get_response = requests.get(f"{BASE_URL}/quizzes/my", headers=headers)
    
    if get_response.status_code == 200:
        quizzes_data = get_response.json()
        if 'quizzes' in quizzes_data and len(quizzes_data['quizzes']) > 0:
            print("✅ Manager quiz management: SUCCESS")
            print(f"   - Created quiz: {quiz_data['title']}")
            print(f"   - Manager can see {len(quizzes_data['quizzes'])} quizzes")
            return True
        else:
            print(f"❌ Manager quiz management: FAILED - No quizzes found")
            return False
    else:
        print(f"❌ Manager quiz management: FAILED - {get_response.status_code}")
        return False

def main():
    print("🚗 Testing Driving School Platform Fixes\n")
    print("=" * 50)
    
    results = []
    
    # Test all fixed issues
    results.append(test_driving_schools_loading())
    results.append(test_manager_teacher_addition())
    results.append(test_manager_quiz_management())
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("\n🎉 All reported issues have been FIXED!")
        print("\nFixed Issues:")
        print("1. ✅ Driving schools now load properly")
        print("2. ✅ Managers can now add teachers (with user creation)")
        print("3. ✅ Managers can now see and manage their quizzes")
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total})")
        print("\nPlease check the individual test results above.")

if __name__ == "__main__":
    main()