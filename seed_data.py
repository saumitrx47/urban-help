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
        # Create Services
        services_data = [
            {
                "name": "Deep House Cleaning",
                "category": ServiceCategory.CLEANING,
                "description": "Comprehensive cleaning service for your entire home",
                "base_price": 80.00,
                "duration_hours": 4.0
            },
            {
                "name": "Office Cleaning",
                "category": ServiceCategory.CLEANING,
                "description": "Professional office cleaning service",
                "base_price": 100.00,
                "duration_hours": 3.0
            },
            {
                "name": "Leak Repair",
                "category": ServiceCategory.PLUMBING,
                "description": "Fix leaks and plumbing issues",
                "base_price": 120.00,
                "duration_hours": 2.0
            },
            {
                "name": "Faucet Installation",
                "category": ServiceCategory.PLUMBING,
                "description": "Install new faucets and fixtures",
                "base_price": 150.00,
                "duration_hours": 2.5
            },
            {
                "name": "Electrical Wiring",
                "category": ServiceCategory.ELECTRICAL,
                "description": "Professional electrical wiring and repairs",
                "base_price": 200.00,
                "duration_hours": 3.0
            },
            {
                "name": "Haircut & Styling",
                "category": ServiceCategory.BEAUTY,
                "description": "Professional haircut and styling service",
                "base_price": 50.00,
                "duration_hours": 1.0
            },
            {
                "name": "Full Body Massage",
                "category": ServiceCategory.MASSAGE,
                "description": "Relaxing full body massage therapy",
                "base_price": 100.00,
                "duration_hours": 1.5
            },
            {
                "name": "Refrigerator Repair",
                "category": ServiceCategory.APPLIANCE_REPAIR,
                "description": "Expert refrigerator repair and maintenance",
                "base_price": 150.00,
                "duration_hours": 2.0
            },
            {
                "name": "Custom Furniture",
                "category": ServiceCategory.CARPENTRY,
                "description": "Custom furniture design and construction",
                "base_price": 300.00,
                "duration_hours": 6.0
            },
            {
                "name": "Interior Painting",
                "category": ServiceCategory.PAINTING,
                "description": "Professional interior painting service",
                "base_price": 250.00,
                "duration_hours": 4.0
            }
        ]
        
        for service_data in services_data:
            service = models.Service(**service_data)
            db.add(service)
        
        db.commit()
        print("✓ Services created")
        
        # Create Service Professionals
        professionals_data = [
            {
                "name": "Sarah Johnson",
                "email": "sarah.johnson@example.com",
                "phone": "+1-555-0101",
                "service_category": ServiceCategory.CLEANING,
                "experience_years": 5,
                "rating": 4.8,
                "total_reviews": 120,
                "hourly_rate": 25.00,
                "bio": "Experienced cleaner with attention to detail",
                "is_available": "true"
            },
            {
                "name": "Mike Chen",
                "email": "mike.chen@example.com",
                "phone": "+1-555-0102",
                "service_category": ServiceCategory.PLUMBING,
                "experience_years": 8,
                "rating": 4.9,
                "total_reviews": 95,
                "hourly_rate": 60.00,
                "bio": "Licensed plumber with 8 years of experience",
                "is_available": "true"
            },
            {
                "name": "David Rodriguez",
                "email": "david.rodriguez@example.com",
                "phone": "+1-555-0103",
                "service_category": ServiceCategory.ELECTRICAL,
                "experience_years": 10,
                "rating": 4.7,
                "total_reviews": 150,
                "hourly_rate": 70.00,
                "bio": "Certified electrician, safety first",
                "is_available": "true"
            },
            {
                "name": "Emma Williams",
                "email": "emma.williams@example.com",
                "phone": "+1-555-0104",
                "service_category": ServiceCategory.BEAUTY,
                "experience_years": 6,
                "rating": 4.9,
                "total_reviews": 200,
                "hourly_rate": 50.00,
                "bio": "Professional hairstylist and makeup artist",
                "is_available": "true"
            },
            {
                "name": "James Anderson",
                "email": "james.anderson@example.com",
                "phone": "+1-555-0105",
                "service_category": ServiceCategory.MASSAGE,
                "experience_years": 7,
                "rating": 4.8,
                "total_reviews": 180,
                "hourly_rate": 65.00,
                "bio": "Licensed massage therapist specializing in relaxation",
                "is_available": "true"
            },
            {
                "name": "Lisa Park",
                "email": "lisa.park@example.com",
                "phone": "+1-555-0106",
                "service_category": ServiceCategory.APPLIANCE_REPAIR,
                "experience_years": 9,
                "rating": 4.6,
                "total_reviews": 110,
                "hourly_rate": 55.00,
                "bio": "Expert appliance repair technician",
                "is_available": "true"
            },
            {
                "name": "Robert Taylor",
                "email": "robert.taylor@example.com",
                "phone": "+1-555-0107",
                "service_category": ServiceCategory.CARPENTRY,
                "experience_years": 12,
                "rating": 4.9,
                "total_reviews": 140,
                "hourly_rate": 50.00,
                "bio": "Master carpenter with custom furniture expertise",
                "is_available": "true"
            },
            {
                "name": "Maria Garcia",
                "email": "maria.garcia@example.com",
                "phone": "+1-555-0108",
                "service_category": ServiceCategory.PAINTING,
                "experience_years": 6,
                "rating": 4.7,
                "total_reviews": 90,
                "hourly_rate": 45.00,
                "bio": "Professional painter with an eye for detail",
                "is_available": "true"
            }
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

