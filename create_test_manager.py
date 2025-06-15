#!/usr/bin/env python3
"""Create a test manager user and driving school for testing"""

import asyncio
import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

# Database setup
MONGO_URL = 'mongodb://localhost:27017'
client = AsyncIOMotorClient(MONGO_URL)
db = client.driving_school_platform

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_test_manager():
    """Create a test manager user and school for testing"""
    print("Creating test manager...")
    
    # Check if test manager already exists
    existing_manager = await db.users.find_one({"email": "manager@test.com"})
    if existing_manager:
        print("Test manager already exists!")
        return existing_manager["id"]
    
    # Create manager user
    manager_id = str(uuid.uuid4())
    password_hash = pwd_context.hash("password123")
    
    manager_data = {
        "id": manager_id,
        "email": "manager@test.com",
        "password_hash": password_hash,
        "first_name": "Test",
        "last_name": "Manager",
        "phone": "0213-21-123456",
        "address": "123 Test Street",
        "date_of_birth": datetime(1985, 1, 1),
        "gender": "male",
        "role": "manager",
        "state": "Alger",
        "profile_photo_url": None,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    await db.users.insert_one(manager_data)
    print(f"Created manager: {manager_data['email']} with password: password123")
    
    # Create driving school
    school_id = str(uuid.uuid4())
    school_data = {
        "id": school_id,
        "name": "Test Driving School",
        "address": "123 Test Street, Alger",
        "state": "Alger",
        "phone": "0213-21-123456",
        "email": "test@school.com",
        "description": "Test driving school for platform testing",
        "logo_url": None,
        "photos": [],
        "price": 35000.0,
        "rating": 4.5,
        "total_reviews": 0,
        "manager_id": manager_id,
        "latitude": 36.7537,
        "longitude": 3.0588,
        "created_at": datetime.utcnow()
    }
    
    await db.driving_schools.insert_one(school_data)
    print(f"Created driving school: {school_data['name']}")
    
    return manager_id

async def main():
    try:
        manager_id = await create_test_manager()
        print(f"\nTest setup completed successfully!")
        print(f"Manager ID: {manager_id}")
        print("Login with: manager@test.com / password123")
    except Exception as e:
        print(f"Error creating test data: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())