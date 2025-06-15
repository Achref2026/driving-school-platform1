#!/usr/bin/env python3
"""
Script to set up sample data for the Algerian Driving School Platform
"""
import asyncio
import uuid
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os
from passlib.context import CryptContext

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Algerian States (58 wilayas)
ALGERIAN_STATES = [
    "Adrar", "Chlef", "Laghouat", "Oum El Bouaghi", "Batna", "Béjaïa", "Biskra", 
    "Béchar", "Blida", "Bouira", "Tamanrasset", "Tébessa", "Tlemcen", "Tiaret", 
    "Tizi Ouzou", "Alger", "Djelfa", "Jijel", "Sétif", "Saïda", "Skikda", 
    "Sidi Bel Abbès", "Annaba", "Guelma", "Constantine", "Médéa", "Mostaganem", 
    "M'Sila", "Mascara", "Ouargla", "Oran", "El Bayadh", "Illizi", 
    "Bordj Bou Arréridj", "Boumerdès", "El Tarf", "Tindouf", "Tissemsilt", 
    "El Oued", "Khenchela", "Souk Ahras", "Tipaza", "Mila", "Aïn Defla", 
    "Naâma", "Aïn Témouchent", "Ghardaïa", "Relizane", "Timimoun", 
    "Bordj Badji Mokhtar", "Ouled Djellal", "Béni Abbès", "In Salah", 
    "In Guezzam", "Touggourt", "Djanet", "El M'Ghair", "El Meniaa"
]

# Sample driving schools data
SAMPLE_SCHOOLS = [
    {
        "name": "École de Conduite Alger Centre",
        "address": "15 Rue Didouche Mourad, Centre-ville",
        "state": "Alger", 
        "phone": "+213 21 63 52 41",
        "email": "contact@ecole-alger-centre.dz",
        "description": "École de conduite moderne au cœur d'Alger avec instructeurs qualifiés et véhicules récents. Formation théorique et pratique de qualité.",
        "price": 45000.0,
        "rating": 4.5,
        "total_reviews": 127,
        "photos": [
            "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "Auto-École Oran Moderne",
        "address": "Boulevard de la Révolution, Oran",
        "state": "Oran",
        "phone": "+213 41 33 17 22", 
        "email": "info@autoecole-oran.dz",
        "description": "Formation de conduite complète avec simulateurs de conduite et piste d'entraînement privée. Taux de réussite élevé.",
        "price": 42000.0,
        "rating": 4.3,
        "total_reviews": 89,
        "photos": [
            "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "École de Conduite Constantine",
        "address": "Place Ahmed Bey, Constantine",
        "state": "Constantine",
        "phone": "+213 31 92 15 73",
        "email": "constantine.conduite@gmail.com", 
        "description": "École expérimentée depuis 1995. Formation adaptée aux routes de montagne avec instructeurs spécialisés.",
        "price": 38000.0,
        "rating": 4.7,
        "total_reviews": 156,
        "photos": [
            "https://images.unsplash.com/photo-1502736876607-ddd1bcf4ed54?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "Auto-École Sétif Pro",
        "address": "Avenue de l'ALN, Sétif",
        "state": "Sétif",
        "phone": "+213 36 84 29 17",
        "email": "setif.pro@autoecole.dz",
        "description": "Formation intensive et traditionnelle. Équipe pédagogique expérimentée avec focus sur la sécurité routière.",
        "price": 35000.0,
        "rating": 4.2,
        "total_reviews": 73,
        "photos": [
            "https://images.unsplash.com/photo-1517104226610-a94df3acbb0b?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "École de Conduite Annaba",
        "address": "Rue de la Révolution, Annaba",
        "state": "Annaba",
        "phone": "+213 38 45 16 29",
        "email": "annaba.conduite@outlook.com",
        "description": "Formation complète avec cours théoriques en arabe et français. Parking privé pour apprentissage.",
        "price": 40000.0,
        "rating": 4.1,
        "total_reviews": 92,
        "photos": [
            "https://images.unsplash.com/photo-1562141961-42905b8893c3?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "Auto-École Tlemcen",
        "address": "Boulevard Colonel Lotfi, Tlemcen",
        "state": "Tlemcen",
        "phone": "+213 43 26 78 45",
        "email": "tlemcen.autoecole@yahoo.fr",
        "description": "École familiale avec approche personnalisée. Formation théorique renforcée et pratique progressive.",
        "price": 37000.0,
        "rating": 4.4,
        "total_reviews": 64,
        "photos": [
            "https://images.unsplash.com/photo-1486848538113-ce1a4923fbc5?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "École Elite Batna",
        "address": "Rue Mustapha Ben Boulaïd, Batna",
        "state": "Batna",
        "phone": "+213 33 81 54 37",
        "email": "elite.batna@gmail.com",
        "description": "Formation d'excellence avec véhicules neufs et instructeurs certifiés. Cours théoriques interactifs.",
        "price": 41000.0,
        "rating": 4.6,
        "total_reviews": 118,
        "photos": [
            "https://images.unsplash.com/photo-1603386329225-868f9b1ee6c9?w=800&h=600&fit=crop"
        ]
    },
    {
        "name": "Auto-École Blida Centre",
        "address": "Place de la Liberté, Blida",
        "state": "Blida",
        "phone": "+213 25 43 67 89",
        "email": "blida.centre@autoecole.dz",
        "description": "Proximité avec Alger, formation accélérée disponible. Instructeurs bilingues arabe-français.",
        "price": 43000.0,
        "rating": 4.0,
        "total_reviews": 85,
        "photos": [
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=600&fit=crop"
        ]
    }
]

async def setup_sample_data():
    """Set up sample data in MongoDB"""
    print("🚀 Setting up sample data for Algerian Driving School Platform...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.driving_school_platform
    
    try:
        # Clear existing data (optional - comment out to keep existing data)
        print("🧹 Clearing existing data...")
        await db.users.delete_many({})
        await db.driving_schools.delete_many({})
        
        # Create sample manager users and driving schools
        print("👥 Creating sample managers and driving schools...")
        
        for i, school_data in enumerate(SAMPLE_SCHOOLS):
            # Create manager user for each school
            manager_id = str(uuid.uuid4())
            manager_email = f"manager{i+1}@{school_data['name'].lower().replace(' ', '').replace('é', 'e').replace('è', 'e')}school.dz"
            
            manager_user = {
                "id": manager_id,
                "email": manager_email,
                "password_hash": pwd_context.hash("manager123"),  # Default password
                "first_name": f"Manager",
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
            
            await db.users.insert_one(manager_user)
            
            # Create driving school
            school_id = str(uuid.uuid4()) 
            school_doc = {
                "id": school_id,
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
                "manager_id": manager_id,
                "latitude": None,
                "longitude": None,
                "created_at": datetime.utcnow()
            }
            
            await db.driving_schools.insert_one(school_doc)
            print(f"✅ Created: {school_data['name']} in {school_data['state']}")
        
        # Create a test student user
        print("👨‍🎓 Creating test student user...")
        student_id = str(uuid.uuid4())
        student_user = {
            "id": student_id,
            "email": "student@test.dz",
            "password_hash": pwd_context.hash("student123"),
            "first_name": "Ahmed",
            "last_name": "Benali",
            "phone": "+213 55 123 456 789",
            "address": "Rue de la Paix, Alger",
            "date_of_birth": datetime(1995, 5, 15),
            "gender": "male",
            "role": "guest",  # Will become student after enrollment
            "state": "Alger",
            "profile_photo_url": None,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        await db.users.insert_one(student_user)
        
        # Verify data creation
        school_count = await db.driving_schools.count_documents({})
        user_count = await db.users.count_documents({})
        
        print(f"\n✨ Sample data setup completed!")
        print(f"📊 Created {school_count} driving schools")
        print(f"👥 Created {user_count} users")
        print(f"🗺️  Covering {len(set(school['state'] for school in SAMPLE_SCHOOLS))} different states")
        
        print("\n🔑 Test Login Credentials:")
        print("Student: student@test.dz / student123")
        print("Manager Examples:")
        for i in range(min(3, len(SAMPLE_SCHOOLS))):
            school = SAMPLE_SCHOOLS[i]
            email = f"manager{i+1}@{school['name'].lower().replace(' ', '').replace('é', 'e').replace('è', 'e')}school.dz"
            print(f"  {school['name']}: {email} / manager123")
        
    except Exception as e:
        print(f"❌ Error setting up sample data: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(setup_sample_data())