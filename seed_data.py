"""
Seed script to populate initial data for the booking platform
Run this after setting up the database
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.models import ServiceCategory, BookingStatus
from datetime import datetime, timedelta

def seed_data():
    db = SessionLocal()
    
    try:
        # Create Construction Services (all costs in INR as integers)
        services_data = [
            {
                "name": "G+2 Residential Building Construction",
                "category": ServiceCategory.RESIDENTIAL_CONSTRUCTION,
                "description": "Turnkey construction for a G+2 residential building including RCC, brickwork, plastering, and finishing.",
                "base_cost_min_inr": 2500000,
                "base_cost_max_inr": 4500000,
                "estimated_duration_days": 180,
                "required_skill_level": "HIGH",
            },
            {
                "name": "Small Commercial Shop Construction",
                "category": ServiceCategory.COMMERCIAL_CONSTRUCTION,
                "description": "Construction of a ground-floor commercial shop with RCC structure and basic finishing.",
                "base_cost_min_inr": 800000,
                "base_cost_max_inr": 1500000,
                "estimated_duration_days": 90,
                "required_skill_level": "MEDIUM",
            },
            {
                "name": "Asphalt Road Resurfacing",
                "category": ServiceCategory.ROAD_PAVEMENT_WORK,
                "description": "Resurfacing of internal roads with asphalt including base preparation.",
                "base_cost_min_inr": 500000,
                "base_cost_max_inr": 2000000,
                "estimated_duration_days": 30,
                "required_skill_level": "MEDIUM",
            },
            {
                "name": "Structural Crack Repair & Jacketing",
                "category": ServiceCategory.STRUCTURAL_REPAIR_RETROFITTING,
                "description": "Column and beam jacketing, crack repair, and structural strengthening for existing RCC structures.",
                "base_cost_min_inr": 300000,
                "base_cost_max_inr": 1200000,
                "estimated_duration_days": 45,
                "required_skill_level": "HIGH",
            },
            {
                "name": "Underground Drainage & STP Connection",
                "category": ServiceCategory.PLUMBING_DRAINAGE_CIVIL,
                "description": "Laying underground drainage lines, manholes, and connecting to sewage treatment plant.",
                "base_cost_min_inr": 600000,
                "base_cost_max_inr": 1800000,
                "estimated_duration_days": 60,
                "required_skill_level": "HIGH",
            },
            {
                "name": "LT Electrical Infrastructure for Apartment Block",
                "category": ServiceCategory.ELECTRICAL_INFRASTRUCTURE,
                "description": "LT panel, cabling, earthing, and internal electrical infrastructure for a residential block.",
                "base_cost_min_inr": 700000,
                "base_cost_max_inr": 1500000,
                "estimated_duration_days": 75,
                "required_skill_level": "HIGH",
            },
            {
                "name": "Exterior Repainting of Residential Complex",
                "category": ServiceCategory.PAINTING_FINISHING,
                "description": "Scaffolding, surface preparation, and exterior repainting of multi-storey residential blocks.",
                "base_cost_min_inr": 400000,
                "base_cost_max_inr": 1200000,
                "estimated_duration_days": 40,
                "required_skill_level": "MEDIUM",
            },
            {
                "name": "Site Inspection & Structural Health Audit",
                "category": ServiceCategory.SITE_INSPECTION_CONSULTING,
                "description": "On-site inspection by a structural engineer with a detailed health and safety report.",
                "base_cost_min_inr": 25000,
                "base_cost_max_inr": 75000,
                "estimated_duration_days": 7,
                "required_skill_level": "HIGH",
            },
        ]
        
        for service_data in services_data:
            service = models.Service(**service_data)
            db.add(service)
        
        db.commit()
        print("✓ Services created")
        
        # Create Contractors (Service Professionals) - all rates in INR per day
        professionals_data = [
            {
                "name": "Rohit Sharma",
                "email": "rohit.sharma.contracts@example.com",
                "phone": "+91-98765-00001",
                "service_category": ServiceCategory.RESIDENTIAL_CONSTRUCTION,
                "experience_years": 12,
                "rating": 4.8,
                "total_reviews": 120,
                "daily_rate_inr": 25000,
                "specialization": "G+2 RCC residential structures",
                "license_number": "MH/ENGG/LIC/2020/RC001",
                "service_areas": "Mumbai, Thane, Navi Mumbai",
                "daily_availability_capacity": 2,
                "bio": "Civil contractor specialising in RCC frame residential projects with turnkey delivery.",
                "is_available": "true",
            },
            {
                "name": "Priya Nair",
                "email": "priya.nair.projects@example.com",
                "phone": "+91-98765-00002",
                "service_category": ServiceCategory.COMMERCIAL_CONSTRUCTION,
                "experience_years": 15,
                "rating": 4.9,
                "total_reviews": 95,
                "daily_rate_inr": 32000,
                "specialization": "Commercial shell and core works",
                "license_number": "KA/ENGG/LIC/2018/CC015",
                "service_areas": "Bengaluru, Mysuru",
                "daily_availability_capacity": 1,
                "bio": "Handles mid-size commercial and retail construction projects with strong schedule control.",
                "is_available": "true",
            },
            {
                "name": "Sanjay Patil",
                "email": "sanjay.patil.roads@example.com",
                "phone": "+91-98765-00003",
                "service_category": ServiceCategory.ROAD_PAVEMENT_WORK,
                "experience_years": 10,
                "rating": 4.7,
                "total_reviews": 150,
                "daily_rate_inr": 28000,
                "specialization": "Asphalt and paver block roads",
                "license_number": "MH/PWD/ROAD/2017/045",
                "service_areas": "Pune, Pimpri-Chinchwad",
                "daily_availability_capacity": 2,
                "bio": "Road contractor experienced with municipal and private roadway works.",
                "is_available": "true",
            },
            {
                "name": "Ananya Rao",
                "email": "ananya.rao.struct@example.com",
                "phone": "+91-98765-00004",
                "service_category": ServiceCategory.STRUCTURAL_REPAIR_RETROFITTING,
                "experience_years": 9,
                "rating": 4.9,
                "total_reviews": 200,
                "daily_rate_inr": 30000,
                "specialization": "Structural repair, retrofitting and jacketing",
                "license_number": "KA/STRUCT/LIC/2019/007",
                "service_areas": "Bengaluru, Hyderabad",
                "daily_availability_capacity": 1,
                "bio": "Works closely with structural consultants on complex repair and retrofitting jobs.",
                "is_available": "true",
            },
            {
                "name": "Imran Khan",
                "email": "imran.khan.civilplumbing@example.com",
                "phone": "+91-98765-00005",
                "service_category": ServiceCategory.PLUMBING_DRAINAGE_CIVIL,
                "experience_years": 11,
                "rating": 4.8,
                "total_reviews": 180,
                "daily_rate_inr": 22000,
                "specialization": "UG drainage, manholes, and STP connectivity",
                "license_number": "DL/CIVIL/PLUMB/2016/112",
                "service_areas": "Delhi, Gurugram, Noida",
                "daily_availability_capacity": 2,
                "bio": "Specialist in large scale civil plumbing and drainage works for townships and complexes.",
                "is_available": "true",
            },
            {
                "name": "Meera Iyer",
                "email": "meera.iyer.electrical@example.com",
                "phone": "+91-98765-00006",
                "service_category": ServiceCategory.ELECTRICAL_INFRASTRUCTURE,
                "experience_years": 13,
                "rating": 4.6,
                "total_reviews": 110,
                "daily_rate_inr": 26000,
                "specialization": "LT panels, earthing, and building electrical infra",
                "license_number": "TN/ELC/LIC/2015/089",
                "service_areas": "Chennai, Coimbatore",
                "daily_availability_capacity": 1,
                "bio": "Licensed electrical contractor with experience in residential and commercial infra projects.",
                "is_available": "true",
            },
            {
                "name": "Arjun Singh",
                "email": "arjun.singh.painting@example.com",
                "phone": "+91-98765-00007",
                "service_category": ServiceCategory.PAINTING_FINISHING,
                "experience_years": 12,
                "rating": 4.9,
                "total_reviews": 140,
                "daily_rate_inr": 18000,
                "specialization": "Exterior painting and finishing for high-rise buildings",
                "license_number": "RJ/FINISH/LIC/2014/022",
                "service_areas": "Jaipur, Udaipur",
                "daily_availability_capacity": 3,
                "bio": "Focuses on durable exterior finishes with proper surface preparation.",
                "is_available": "true",
            },
            {
                "name": "Dr. Kavita Desai",
                "email": "kavita.desai.consult@example.com",
                "phone": "+91-98765-00008",
                "service_category": ServiceCategory.SITE_INSPECTION_CONSULTING,
                "experience_years": 16,
                "rating": 4.7,
                "total_reviews": 90,
                "daily_rate_inr": 35000,
                "specialization": "Structural audit and site inspections",
                "license_number": "GJ/STRUCT/CONS/2012/033",
                "service_areas": "Ahmedabad, Vadodara, Surat",
                "daily_availability_capacity": 1,
                "bio": "Chartered structural engineer providing detailed site inspection and audit reports.",
                "is_available": "true",
            },
        ]
        
        for prof_data in professionals_data:
            professional = models.ServiceProfessional(**prof_data)
            db.add(professional)
        
        db.commit()
        print("✓ Service professionals created")
        
        # Create sample customers
        customers_data = [
            {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0201",
                "address": "123 Main St, City, State 12345"
            },
            {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+1-555-0202",
                "address": "456 Oak Ave, City, State 12345"
            }
        ]
        
        for customer_data in customers_data:
            customer = models.Customer(**customer_data)
            db.add(customer)
        
        db.commit()
        print("✓ Sample customers created")
        
        print("\n✅ Seed data created successfully!")
        print("\nYou can now start the application and browse services.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables first
    models.Base.metadata.create_all(bind=engine)
    print("Creating database tables...")
    seed_data()

