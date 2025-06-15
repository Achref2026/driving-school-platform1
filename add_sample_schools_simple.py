#!/usr/bin/env python3
"""Add a few sample driving schools to the database"""

import asyncio
import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient

# Database setup
MONGO_URL = 'mongodb://localhost:27017'
client = AsyncIOMotorClient(MONGO_URL)
db = client.driving_school_platform

ALGERIAN_STATES = [
    "Adrar", "Chlef", "Laghouat", "Oum El Bouaghi", "Batna", "Béjaïa", "Biskra", 
    "Béchar", "Blida", "Bouira", "Tamanrasset", "Tébessa", "Tlemcen", "Tiaret", 
    "Tizi Ouzou", "Alger", "Djelfa", "Jijel", "Sétif", "Saïda", "Skikda", 
    "Sidi Bel Abbès", "Annaba", "Guelma", "Constantine", "Médéa", "Mostaganem", 
    "M'Sila", "Mascara", "Ouargla", "Oran", "El Bayadh", "Illizi", 
    "Bordj Bou Arréridj", "Boumerdès", "El Tarf", "Tindouf", "Tissemsilt", 
    "El Oued", "Khenchela", "Souk Ahras", "Tipaza", "Mila", "Aïn Defla", 
    "Naâma", "Aïn Témouchent", "Ghardaïa", "Relizane"
]

sample_schools = [
    {
        "name": "Auto École Excellence",
        "address": "15 Rue Didouche Mourad",
        "state": "Alger",
        "phone": "0213-21-123456",
        "email": "contact@excellence-auto.dz",
        "description": "École de conduite moderne avec des instructeurs qualifiés et des véhicules récents.",
        "price": 45000.0,
        "rating": 4.5,
        "total_reviews": 127
    },
    {
        "name": "Conduite Sûre Oran",
        "address": "Avenue Ahmed Ben Bella",
        "state": "Oran",
        "phone": "0213-41-987654",
        "email": "info@conduite-sure.dz",
        "description": "Formation complète à la conduite avec cours théoriques et pratiques personnalisés.",
        "price": 38000.0,
        "rating": 4.2,
        "total_reviews": 89
    },
    {
        "name": "École Nationale de Conduite",
        "address": "Boulevard Zighout Youcef",
        "state": "Constantine",
        "phone": "0213-31-456789",
        "email": "contact@enc-constantine.dz",
        "description": "École de conduite avec plus de 20 ans d'expérience dans la formation des conducteurs.",
        "price": 42000.0,
        "rating": 4.7,
        "total_reviews": 203
    },
    {
        "name": "Auto Formation Blida",
        "address": "Rue des Martyrs",
        "state": "Blida",
        "phone": "0213-25-345678",
        "email": "info@autoformation-blida.dz",
        "description": "Formation à la conduite dans un environnement moderne avec des instructeurs professionnels.",
        "price": 35000.0,
        "rating": 4.0,
        "total_reviews": 56
    },
    {
        "name": "Driving School Annaba",
        "address": "Cours de la Révolution",
        "state": "Annaba",
        "phone": "0213-38-234567",
        "email": "contact@driving-annaba.dz",
        "description": "École de conduite bilingue avec formation théorique et pratique complète.",
        "price": 40000.0,
        "rating": 4.3,
        "total_reviews": 78
    },
    {
        "name": "École Moderne Sétif",
        "address": "Avenue 8 Mai 1945",
        "state": "Sétif",
        "phone": "0213-36-123789",
        "email": "info@ecole-moderne.dz",
        "description": "Formation moderne à la conduite avec simulateurs et véhicules équipés.",
        "price": 43000.0,
        "rating": 4.6,
        "total_reviews": 134
    }
]

async def add_sample_schools():
    """Add sample driving schools to the database"""
    print("Adding sample driving schools...")
    
    # Check if schools already exist
    existing_count = await db.driving_schools.count_documents({})
    if existing_count > 0:
        print(f"Found {existing_count} existing schools. Skipping sample data creation.")
        return
    
    # Create dummy manager user IDs for each school
    schools_to_insert = []
    
    for school_data in sample_schools:
        # Create a dummy manager ID (in real app, this would be linked to actual manager users)
        manager_id = str(uuid.uuid4())
        
        school_doc = {
            "id": str(uuid.uuid4()),
            "name": school_data["name"],
            "address": school_data["address"],
            "state": school_data["state"],
            "phone": school_data["phone"],
            "email": school_data["email"],
            "description": school_data["description"],
            "logo_url": None,
            "photos": [],
            "price": school_data["price"],
            "rating": school_data["rating"],
            "total_reviews": school_data["total_reviews"],
            "manager_id": manager_id,
            "latitude": None,
            "longitude": None,
            "created_at": datetime.utcnow()
        }
        schools_to_insert.append(school_doc)
    
    # Insert all schools
    result = await db.driving_schools.insert_many(schools_to_insert)
    print(f"Successfully added {len(result.inserted_ids)} sample driving schools!")
    
    # Print the schools for verification
    print("\nAdded schools:")
    for school in schools_to_insert:
        print(f"- {school['name']} in {school['state']} ({school['price']} DA)")

async def main():
    try:
        await add_sample_schools()
        print("\nSample data creation completed successfully!")
    except Exception as e:
        print(f"Error creating sample data: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())