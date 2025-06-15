import requests
import sys
import json
import time
import os
from datetime import datetime, timedelta

class DrivingSchoolAPITester:
    def __init__(self, base_url="http://localhost:8001"):
        # Get the backend URL from the frontend .env file
        try:
            with open('/app/frontend/.env', 'r') as f:
                for line in f:
                    if line.startswith('REACT_APP_BACKEND_URL='):
                        base_url = line.strip().split('=')[1].strip('"\'')
                        break
        except Exception as e:
            print(f"Warning: Could not read REACT_APP_BACKEND_URL from frontend/.env: {e}")
            
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.user_role = None
        self.tests_run = 0
        self.tests_passed = 0
        self.school_id = None
        self.enrollment_id = None
        self.course_id = None
        self.quiz_id = None
        self.expert_id = None
        self.session_id = None
        self.exam_id = None
        self.certificate_id = None
        self.notification_id = None
        self.review_id = None
        self.teacher_id = None
        self.document_id = None
        
        print(f"Testing backend URL: {self.base_url}")
        print("Note: This URL should match REACT_APP_BACKEND_URL in frontend/.env")

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None, form_data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, headers=headers)
                elif form_data:
                    response = requests.post(url, data=form_data, headers=headers)
                else:
                    headers['Content-Type'] = 'application/json'
                    response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Response text: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test the health check endpoint"""
        return self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200
        )

    def test_get_states(self):
        """Test getting Algerian states"""
        return self.run_test(
            "Get Algerian States",
            "GET",
            "api/states",
            200
        )

    def test_register_user(self, email, password, first_name, last_name):
        """Test user registration"""
        form_data = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'phone': '0555123456',
            'address': 'Test Address',
            'date_of_birth': '1990-01-01',
            'gender': 'male',
            'state': 'Alger'
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "api/auth/register",
            200,
            form_data=form_data
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_id = response['user']['id']
            self.user_role = response['user']['role']
            print(f"User registered with role: {self.user_role}")
            return True
        return False

    def test_login(self, email, password):
        """Test login"""
        success, response = self.run_test(
            "Login",
            "POST",
            "api/auth/login",
            200,
            data={"email": email, "password": password}
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_id = response['user']['id']
            self.user_role = response['user']['role']
            print(f"Logged in as: {response['user']['first_name']} {response['user']['last_name']} (Role: {self.user_role})")
            return True
        return False

    def test_create_driving_school(self, name):
        """Test creating a driving school"""
        data = {
            "name": name,
            "address": "123 Test Street",
            "state": "Alger",
            "phone": "0555123456",
            "email": "school@test.com",
            "description": "Test driving school",
            "price": 15000
        }
        
        success, response = self.run_test(
            "Create Driving School",
            "POST",
            "api/driving-schools",
            200,
            data=data
        )
        
        if success and 'id' in response:
            self.school_id = response['id']
            print(f"School created with ID: {self.school_id}")
            return True
        return False

    def test_get_driving_schools(self, state=None, min_price=None, max_price=None, min_rating=None, sort_by="name", sort_order="asc", page=1, limit=20):
        """Test getting driving schools with optional filters"""
        params = {
            "page": page,
            "limit": limit
        }
        
        if state:
            params["state"] = state
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        if min_rating is not None:
            params["min_rating"] = min_rating
        if sort_by:
            params["sort_by"] = sort_by
        if sort_order:
            params["sort_order"] = sort_order
            
        endpoint = f"api/driving-schools?{self._build_query_params(params)}"
        return self.run_test(
            f"Get Driving Schools (Page {page}, Limit {limit})",
            "GET",
            endpoint,
            200
        )
    
    def _build_query_params(self, params):
        """Build query parameters string from dictionary"""
        return "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

    def test_get_driving_school(self, school_id):
        """Test getting a specific driving school"""
        return self.run_test(
            "Get Driving School Details",
            "GET",
            f"api/driving-schools/{school_id}",
            200
        )

    def test_enroll_in_school(self, school_id):
        """Test enrolling in a driving school"""
        success, response = self.run_test(
            "Enroll in Driving School",
            "POST",
            "api/enrollments",
            200,
            data={"school_id": school_id}
        )
        
        if success and 'enrollment_id' in response:
            self.enrollment_id = response['enrollment_id']
            print(f"Enrolled with ID: {self.enrollment_id}")
            return True
        return False

    def test_complete_payment(self, enrollment_id):
        """Test completing payment"""
        form_data = {
            'enrollment_id': enrollment_id
        }
        
        return self.run_test(
            "Complete Payment",
            "POST",
            "api/payments/complete",
            200,
            form_data=form_data
        )

    def test_get_my_enrollments(self):
        """Test getting user's enrollments"""
        success, response = self.run_test(
            "Get My Enrollments",
            "GET",
            "api/enrollments/my",
            200
        )
        
        if success and len(response) > 0:
            # Get the first course ID for later tests
            for enrollment in response:
                if 'courses' in enrollment and len(enrollment['courses']) > 0:
                    self.course_id = enrollment['courses'][0]['id']
                    print(f"Found course ID: {self.course_id}")
                    break
        
        return success, response

    def test_get_dashboard(self):
        """Test getting dashboard data"""
        return self.run_test(
            "Get Dashboard",
            "GET",
            f"api/dashboard/{self.user_role}",
            200
        )

    def test_create_quiz(self):
        """Test creating a quiz (manager only)"""
        if self.user_role != 'manager':
            print("Skipping quiz creation - requires manager role")
            return False, {}
            
        data = {
            "course_type": "theory",
            "title": "Basic Road Signs Quiz",
            "description": "Test your knowledge of basic road signs",
            "difficulty": "easy",
            "questions": [
                {
                    "question": "What does a red octagonal sign mean?",
                    "options": ["Stop", "Yield", "Caution", "No entry"],
                    "correct_answer": 0
                },
                {
                    "question": "What does a yellow triangle sign indicate?",
                    "options": ["Stop", "Yield", "Warning", "Speed limit"],
                    "correct_answer": 2
                }
            ],
            "passing_score": 70,
            "time_limit_minutes": 10
        }
        
        success, response = self.run_test(
            "Create Quiz",
            "POST",
            "api/quizzes",
            200,
            data=data
        )
        
        if success and 'quiz_id' in response:
            self.quiz_id = response['quiz_id']
            print(f"Quiz created with ID: {self.quiz_id}")
            return True
        return False

    def test_get_quizzes(self):
        """Test getting quizzes"""
        return self.run_test(
            "Get Quizzes",
            "GET",
            "api/quizzes",
            200
        )

    def test_complete_course_session(self, course_id):
        """Test completing a course session"""
        if not course_id:
            print("Skipping session completion - no course ID available")
            return False, {}
            
        return self.run_test(
            "Complete Course Session",
            "POST",
            f"api/courses/{course_id}/complete-session",
            200
        )

    def test_take_exam(self, course_id):
        """Test taking an exam"""
        if not course_id or self.user_role != 'student':
            print("Skipping exam - no course ID available or not a student")
            return False, {}
            
        form_data = {
            'score': 85
        }
        
        return self.run_test(
            "Take Exam",
            "POST",
            f"api/courses/{course_id}/take-exam",
            200,
            form_data=form_data
        )

    def test_add_teacher(self):
        """Test adding a teacher"""
        if self.user_role != 'manager':
            print("Skipping teacher addition - requires manager role")
            return False, {}
            
        data = {
            "email": f"teacher_{int(time.time())}@test.com",
            "can_teach_male": True,
            "can_teach_female": True
        }
        
        return self.run_test(
            "Add Teacher",
            "POST",
            "api/teachers/add",
            200,
            data=data
        )

    def test_video_room_creation(self):
        """Test video room creation"""
        if not self.course_id or self.user_role != 'teacher':
            print("Skipping video room creation - no course ID or not a teacher")
            return False, {}
            
        data = {
            "course_id": self.course_id,
            "student_id": "some-student-id",  # This would need a real student ID
            "scheduled_at": datetime.now().isoformat(),
            "duration_minutes": 60
        }
        
        return self.run_test(
            "Create Video Room",
            "POST",
            "api/video-rooms",
            200,
            data=data
        )
        
    # Phase 2 Feature Tests
    
    def test_register_external_expert(self):
        """Test registering as an external expert"""
        if self.user_role != 'guest':
            print("Skipping external expert registration - requires guest role")
            return False, {}
            
        data = {
            "email": f"expert_{int(time.time())}@test.com",
            "specialization": ["park", "road"],
            "available_states": ["Alger", "Blida"],
            "certification_number": f"CERT-{int(time.time())}",
            "years_of_experience": 5
        }
        
        success, response = self.run_test(
            "Register External Expert",
            "POST",
            "api/external-experts/register",
            200,
            data=data
        )
        
        if success and 'expert_id' in response:
            self.expert_id = response['expert_id']
            print(f"Expert registered with ID: {self.expert_id}")
            return True
        return False
        
    def test_get_external_experts(self):
        """Test getting external experts"""
        return self.run_test(
            "Get External Experts",
            "GET",
            "api/external-experts",
            200
        )
        
    def test_schedule_exam(self):
        """Test scheduling an exam with external expert"""
        if not self.course_id or self.user_role != 'student':
            print("Skipping exam scheduling - no course ID or not a student")
            return False, {}
            
        data = {
            "course_id": self.course_id,
            "exam_type": "park",
            "preferred_dates": [(datetime.now() + timedelta(days=1)).isoformat(), 
                               (datetime.now() + timedelta(days=2)).isoformat()],
            "location": "Alger"
        }
        
        success, response = self.run_test(
            "Schedule Exam",
            "POST",
            "api/exams/schedule",
            200,
            data=data
        )
        
        if success and 'exam_id' in response:
            self.exam_id = response['exam_id']
            print(f"Exam scheduled with ID: {self.exam_id}")
            return True
        return False
        
    def test_get_my_exams(self):
        """Test getting user's exams"""
        if self.user_role not in ['student', 'external_expert']:
            print("Skipping get exams - requires student or external_expert role")
            return False, {}
            
        return self.run_test(
            "Get My Exams",
            "GET",
            "api/exams/my",
            200
        )
        
    def test_schedule_session(self):
        """Test scheduling a practical session"""
        if not self.course_id or self.user_role != 'student':
            print("Skipping session scheduling - no course ID or not a student")
            return False, {}
            
        data = {
            "course_id": self.course_id,
            "teacher_id": "some-teacher-id",  # This would need a real teacher ID
            "scheduled_at": (datetime.now() + timedelta(days=1)).isoformat(),
            "duration_minutes": 60,
            "location": "Driving School Parking"
        }
        
        success, response = self.run_test(
            "Schedule Session",
            "POST",
            "api/sessions/schedule",
            200,
            data=data
        )
        
        if success and 'session_id' in response:
            self.session_id = response['session_id']
            print(f"Session scheduled with ID: {self.session_id}")
            return True
        return False
        
    def test_get_my_sessions(self):
        """Test getting user's sessions"""
        return self.run_test(
            "Get My Sessions",
            "GET",
            "api/sessions/my",
            200
        )
        
    def test_complete_session(self):
        """Test completing a session"""
        if not self.session_id or self.user_role not in ['teacher', 'manager']:
            print("Skipping session completion - no session ID or not a teacher/manager")
            return False, {}
            
        return self.run_test(
            "Complete Session",
            "POST",
            f"api/sessions/{self.session_id}/complete",
            200
        )
        
    def test_get_my_certificates(self):
        """Test getting user's certificates"""
        if self.user_role != 'student':
            print("Skipping certificates - requires student role")
            return False, {}
            
        success, response = self.run_test(
            "Get My Certificates",
            "GET",
            "api/certificates/my",
            200
        )
        
        if success and len(response) > 0:
            self.certificate_id = response[0]['id']
            print(f"Found certificate ID: {self.certificate_id}")
        
        return success, response
        
    def test_verify_certificate(self):
        """Test verifying a certificate"""
        if not self.certificate_id:
            print("Skipping certificate verification - no certificate ID")
            return False, {}
            
        return self.run_test(
            "Verify Certificate",
            "GET",
            f"api/certificates/{self.certificate_id}/verify",
            200
        )
        
    def test_get_my_teachers(self):
        """Test getting teachers for a manager's school"""
        if self.user_role != 'manager':
            print("Skipping get teachers - requires manager role")
            return False, {}
            
        success, response = self.run_test(
            "Get My Teachers",
            "GET",
            "api/teachers/my",
            200
        )
        
        if success and len(response) > 0:
            self.teacher_id = response[0]['id']
            print(f"Found teacher ID: {self.teacher_id}")
        
        return success, response
        
    def test_get_my_quizzes(self):
        """Test getting manager's quizzes"""
        if self.user_role != 'manager':
            print("Skipping get my quizzes - requires manager role")
            return False, {}
            
        return self.run_test(
            "Get My Quizzes",
            "GET",
            "api/quizzes/my",
            200
        )
        
    def test_upload_document(self):
        """Test document upload"""
        if self.user_role not in ['student', 'teacher']:
            print("Skipping document upload - requires student or teacher role")
            return False, {}
        
        # Create a simple text file for testing
        test_file_content = b"This is a test document for the driving school platform."
        files = {
            'file': ('test_document.txt', test_file_content, 'text/plain')
        }
        
        form_data = {
            'document_type': 'profile_photo'
        }
        
        success, response = self.run_test(
            "Upload Document",
            "POST",
            "api/documents/upload",
            200,
            files=files,
            form_data=form_data
        )
        
        if success and 'document_id' in response:
            self.document_id = response['document_id']
            print(f"Document uploaded with ID: {self.document_id}")
            return True
        return False
        
    def test_get_documents(self):
        """Test getting user documents"""
        if not self.user_id:
            print("Skipping get documents - no user ID")
            return False, {}
            
        return self.run_test(
            "Get User Documents",
            "GET",
            "api/documents",
            200
        )
        
    def test_take_quiz(self):
        """Test taking a quiz"""
        if self.user_role != 'student':
            print("Skipping quiz taking - requires student role")
            return False, {}
            
        # First get available quizzes
        success, quizzes = self.run_test(
            "Get Available Quizzes",
            "GET",
            "api/quizzes",
            200
        )
        
        if not success or not quizzes or len(quizzes) == 0:
            print("No quizzes available to take")
            return False, {}
            
        quiz_id = quizzes[0]['id']
        
        # Create sample answers
        answers = {}
        for i, question in enumerate(quizzes[0]['questions']):
            # Just pick the first answer for testing
            answers[str(i)] = 0
        
        return self.run_test(
            "Take Quiz",
            "POST",
            f"api/quizzes/{quiz_id}/attempt",
            200,
            data=answers
        )
        
    def test_mark_notification_read(self):
        """Test marking a notification as read"""
        if not self.notification_id:
            print("Skipping notification marking - no notification ID")
            return False, {}
            
        return self.run_test(
            "Mark Notification Read",
            "POST",
            f"api/notifications/{self.notification_id}/read",
            200
        )
        
    def test_get_my_notifications(self):
        """Test getting user's notifications"""
        success, response = self.run_test(
            "Get My Notifications",
            "GET",
            "api/notifications/my",
            200
        )
        
        if success and len(response) > 0:
            self.notification_id = response[0]['id']
            print(f"Found notification ID: {self.notification_id}")
        
        return success, response
        
    def test_get_school_analytics(self):
        """Test getting school analytics"""
        if self.user_role != 'manager':
            print("Skipping school analytics - requires manager role")
            return False, {}
            
        return self.run_test(
            "Get School Analytics",
            "GET",
            "api/analytics/school-overview",
            200
        )
        
    def test_get_teacher_performance(self):
        """Test getting teacher performance analytics"""
        if self.user_role != 'manager':
            print("Skipping teacher performance - requires manager role")
            return False, {}
            
        # This would need a real teacher ID
        teacher_id = "some-teacher-id"
        
        return self.run_test(
            "Get Teacher Performance",
            "GET",
            f"api/analytics/teacher-performance/{teacher_id}",
            200
        )
        
    def test_create_review(self):
        """Test creating a review"""
        if not self.enrollment_id or self.user_role != 'student':
            print("Skipping review creation - no enrollment ID or not a student")
            return False, {}
            
        data = {
            "rating": 5,
            "comment": "Great driving school and instructors!",
            "enrollment_id": self.enrollment_id
        }
        
        success, response = self.run_test(
            "Create Review",
            "POST",
            "api/reviews",
            200,
            data=data
        )
        
        if success and 'review_id' in response:
            self.review_id = response['review_id']
            print(f"Review created with ID: {self.review_id}")
            return True
        return False
        
    def test_get_school_reviews(self):
        """Test getting school reviews"""
        if not self.school_id:
            print("Skipping school reviews - no school ID")
            return False, {}
            
        return self.run_test(
            "Get School Reviews",
            "GET",
            f"api/reviews/school/{self.school_id}",
            200
        )

def test_get_my_quizzes(self):
    """Test getting manager's quizzes"""
    if self.user_role != 'manager':
        print("Skipping get my quizzes - requires manager role")
        return False, {}
        
    return self.run_test(
        "Get My Quizzes",
        "GET",
        "api/quizzes/my",
        200
    )

def main():
    # Setup
    tester = DrivingSchoolAPITester()
    
    print("\n🔍 ALGERIA DRIVING SCHOOL PLATFORM API TEST\n")
    print("Testing critical functionality based on the fix request:\n")
    
    # 1. Test health check (both root and API prefixed)
    health_success, health_data = tester.test_health_check()
    if not health_success:
        print("❌ API health check failed, stopping tests")
        return 1
    else:
        print(f"✅ API health check passed: {health_data}")
    
    # 2. Test driving schools API
    schools_success, schools_data = tester.test_get_driving_schools()
    if schools_success:
        schools_count = len(schools_data.get('schools', []))
        print(f"✅ Retrieved {schools_count} driving schools")
        
        # Print school names to verify
        school_names = [school.get('name', 'Unknown') for school in schools_data.get('schools', [])]
        print(f"School names: {', '.join(school_names)}")
        
        # Test pagination
        if schools_data.get('pagination'):
            print(f"✅ Pagination info: {schools_data.get('pagination')}")
        else:
            print("❌ Pagination information missing")
    else:
        print("❌ Failed to retrieve driving schools")
    
    # 3. Test authentication with manager credentials
    print("\nTesting authentication with manager credentials:")
    manager_login_success = tester.test_login("manager@test.com", "password123")
    if manager_login_success:
        print("✅ Manager login successful")
        
        # 4. Test manager-specific endpoints
        
        # Test adding a teacher
        add_teacher_success, add_teacher_data = tester.test_add_teacher()
        if add_teacher_success:
            print("✅ Teacher addition successful")
            if 'teacher' in add_teacher_data:
                print(f"Teacher added: {add_teacher_data['teacher'].get('email', 'Unknown')}")
        else:
            print("❌ Teacher addition failed")
        
        # Test getting manager's quizzes
        quizzes_success, quizzes_data = tester.test_get_my_quizzes()
        if quizzes_success:
            quizzes_count = len(quizzes_data.get('quizzes', []))
            print(f"✅ Retrieved {quizzes_count} quizzes for manager")
            if quizzes_count > 0:
                quiz_titles = [quiz.get('title', 'Unknown') for quiz in quizzes_data.get('quizzes', [])]
                print(f"Quiz titles: {', '.join(quiz_titles)}")
        else:
            print("❌ Failed to retrieve manager's quizzes")
        
        # Test creating a quiz
        create_quiz_success, create_quiz_data = tester.test_create_quiz()
        if create_quiz_success:
            print("✅ Quiz creation successful")
            if 'quiz_id' in create_quiz_data:
                print(f"Quiz created with ID: {create_quiz_data['quiz_id']}")
        else:
            print("❌ Quiz creation failed")
    else:
        print("❌ Manager login failed")
    
    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    print(f"Pass rate: {(tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0:.2f}%")
    
    # Print summary of findings
    print("\n📋 SUMMARY OF FINDINGS:")
    print("✅ Working features:")
    if health_success:
        print("  - Backend health check")
    if schools_success:
        print(f"  - Driving schools listing (found {len(schools_data.get('schools', []))} schools)")
        if schools_data.get('pagination'):
            print("  - Pagination")
    if 'manager_login_success' in locals() and manager_login_success:
        print("  - Manager authentication")
    if 'add_teacher_success' in locals() and add_teacher_success:
        print("  - Teacher addition")
    if 'quizzes_success' in locals() and quizzes_success:
        print("  - Manager quizzes retrieval")
    if 'create_quiz_success' in locals() and create_quiz_success:
        print("  - Quiz creation")
    
    print("\n❌ Issues/Not working:")
    if not health_success:
        print("  - Backend health check not working")
    if not schools_success:
        print("  - Driving schools listing not working")
    elif schools_success and not schools_data.get('pagination'):
        print("  - Pagination information missing")
    if 'manager_login_success' in locals() and not manager_login_success:
        print("  - Manager authentication not working")
    if 'add_teacher_success' in locals() and not add_teacher_success:
        print("  - Teacher addition not working")
    if 'quizzes_success' in locals() and not quizzes_success:
        print("  - Manager quizzes retrieval not working")
    if 'create_quiz_success' in locals() and not create_quiz_success:
        print("  - Quiz creation not working")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
