#!/usr/bin/env python3
"""
Add sample driving schools to the database for testing
"""
import asyncio
import uuid
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')

# Sample Algerian states
ALGERIAN_STATES = [
    "Adrar", "Chlef", "Laghouat", "Oum El Bouaghi", "Batna", "Béjaïa", "Biskra", 
    "Béchar", "Blida", "Bouira", "Tamanrasset", "Tébessa", "Tlemcen", "Tiaret", 
    "Tizi Ouzou", "Alger", "Djelfa", "Jijel", "Sétif", "Saïda", "Skikda", 
    "Sidi Bel Abbès", "Annaba", "Guelma", "Constantine", "Médéa", "Mostaganem", 
    "M'Sila", "Mascara", "Ouargla", "Oran"
]

# Sample driving schools data
SAMPLE_SCHOOLS = [
    {
        "name": "École de Conduite Atlas",
        "state": "Alger",
        "address": "123 Rue Didouche Mourad, Alger",
        "phone": "+213 21 123 456",
        "email": "contact@ecole-atlas.dz",
        "description": "École de conduite moderne avec instructeurs qualifiés et véhicules récents. Formation théorique et pratique de qualité.",
        "price": 25000.0,
        "rating": 4.5,
        "total_reviews": 127,
        "photos": [
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "Auto École El Djazair",
        "state": "Oran",
        "address": "45 Boulevard de la République, Oran",
        "phone": "+213 41 789 012",
        "email": "info@autoecole-djazair.dz",
        "description": "Plus de 20 ans d'expérience dans la formation à la conduite. Taux de réussite élevé aux examens.",
        "price": 22000.0,
        "rating": 4.2,
        "total_reviews": 89,
        "photos": [
            "https://images.unsplash.com/photo-1553979459-d2229ba7433a?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "École de Conduite Salam",
        "state": "Constantine",
        "address": "78 Rue Larbi Ben M'hidi, Constantine",
        "phone": "+213 31 456 789",
        "email": "contact@salam-driving.dz",
        "description": "Formation complète avec cours théoriques interactifs et pratique intensive. Instructeurs patients et professionnels.",
        "price": 23000.0,
        "rating": 4.7,
        "total_reviews": 156,
        "photos": [
            "https://images.unsplash.com/photo-1597149114808-6e43875d74ba?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "Auto École Nour",
        "state": "Blida",
        "address": "12 Rue de l'Indépendance, Blida",
        "phone": "+213 25 234 567",
        "email": "nour.autoecole@gmail.com",
        "description": "École familiale avec approche personnalisée. Formation adaptée aux besoins de chaque élève.",
        "price": 24000.0,
        "rating": 4.3,
        "total_reviews": 73,
        "photos": [
            "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "École de Conduite El Baraka",
        "state": "Sétif",
        "address": "89 Avenue du 1er Novembre, Sétif",
        "phone": "+213 36 567 890",
        "email": "elbaraka.driving@hotmail.com",
        "description": "Formation accélérée disponible. Cours de conduite en ville et sur autoroute. Excellent taux de réussite.",
        "price": 21500.0,
        "rating": 4.4,
        "total_reviews": 94,
        "photos": [
            "https://images.unsplash.com/photo-1545558014-8692077e9b5c?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "Auto École Assil",
        "state": "Annaba",
        "address": "34 Rue Mohamed Khemisti, Annaba",
        "phone": "+213 38 345 678",
        "email": "contact@assil-autoecole.dz",
        "description": "École moderne avec simulateurs de conduite. Formation théorique multimédia et pratique progressive.",
        "price": 26000.0,
        "rating": 4.6,
        "total_reviews": 112,
        "photos": [
            "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "École de Conduite Tassili",
        "state": "Ouargla",
        "address": "67 Route de Ghardaïa, Ouargla",
        "phone": "+213 29 678 901",
        "email": "tassili.ecole@yahoo.fr",
        "description": "Spécialisée dans la formation au permis de conduire toutes catégories. Instructeurs expérimentés.",
        "price": 20000.0,
        "rating": 4.1,
        "total_reviews": 58,
        "photos": [
            "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "Auto École El Fajr",
        "state": "Tlemcen",
        "address": "56 Boulevard Colonel Lotfi, Tlemcen",
        "phone": "+213 43 789 123",
        "email": "elfajr.driving@gmail.com",
        "description": "Plus de 15 ans au service de la formation routière. Pédagogie moderne et suivi personnalisé.",
        "price": 22500.0,
        "rating": 4.3,
        "total_reviews": 67,
        "photos": [
            "https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1597149114808-6e43875d74ba?w=800&h=600&fit=crop"
        ]
    }
]

async def add_sample_schools():
    """Add sample driving schools to the database"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.driving_school_platform
    
    try:
        # Clear existing schools (for testing)
        await db.driving_schools.delete_many({})
        print("Cleared existing driving schools")
        
        # Add sample managers first
        managers = []
        for i, school_data in enumerate(SAMPLE_SCHOOLS):
            # Create a manager for each school
            manager_id = str(uuid.uuid4())
            user_id = str(uuid.uuid4())
            
            # Create user account for manager
            manager_user = {
                "id": user_id,
                "email": school_data["email"],
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LQ1Gau.GY64d/OQo94YLjXQgq/f8YNqF0Dquy",  # password: "password123"
                "first_name": f"Manager {i+1}",
                "last_name": f"School {i+1}",
                "phone": school_data["phone"],
                "address": school_data["address"],
                "date_of_birth": datetime(1980, 1, 1),
                "gender": "male",
                "role": "manager",
                "state": school_data["state"],
                "profile_photo_url": None,
                "created_at": datetime.utcnow(),
                "is_active": True
            }
            
            managers.append(manager_user)
            
            # Create driving school
            school_doc = {
                "id": str(uuid.uuid4()),
                "name": school_data["name"],
                "address": school_data["address"],
                "state": school_data["state"],
                "phone": school_data["phone"],
                "email": school_data["email"],
                "description": school_data["description"],
                "logo_url": None,
                "photos": school_data["photos"],
                "price": school_data["price"],
                "rating": school_data["rating"],
                "total_reviews": school_data["total_reviews"],
                "manager_id": user_id,
                "latitude": None,
                "longitude": None,
                "created_at": datetime.utcnow()
            }
            
            # Insert the school
            await db.driving_schools.insert_one(school_doc)
            print(f"Added driving school: {school_data['name']} in {school_data['state']}")
        
        # Insert all manager users
        if managers:
            await db.users.insert_many(managers)
            print(f"Added {len(managers)} manager users")
        
        # Print statistics
        total_schools = await db.driving_schools.count_documents({})
        total_users = await db.users.count_documents({})
        
        print(f"\n✅ Sample data added successfully!")
        print(f"Total driving schools: {total_schools}")
        print(f"Total users: {total_users}")
        
        # Show schools by state
        pipeline = [
            {"$group": {"_id": "$state", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        schools_by_state = await db.driving_schools.aggregate(pipeline).to_list(length=None)
        
        print("\nSchools by state:")
        for state_info in schools_by_state:
            print(f"  {state_info['_id']}: {state_info['count']} schools")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(add_sample_schools())