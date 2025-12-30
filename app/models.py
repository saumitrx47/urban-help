from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class BookingStatus(enum.Enum):
    """
    Project lifecycle status for civil construction projects.
    NOTE: Semantics updated from simple 'booking' to multi-day 'project request'.
    """
    REQUESTED = "requested"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ServiceCategory(enum.Enum):
    """
    Civil construction and infrastructure service categories.
    """
    RESIDENTIAL_CONSTRUCTION = "residential_construction"
    COMMERCIAL_CONSTRUCTION = "commercial_construction"
    ROAD_PAVEMENT_WORK = "road_pavement_work"
    STRUCTURAL_REPAIR_RETROFITTING = "structural_repair_retrofitting"
    PLUMBING_DRAINAGE_CIVIL = "plumbing_drainage_civil"
    ELECTRICAL_INFRASTRUCTURE = "electrical_infrastructure"
    PAINTING_FINISHING = "painting_finishing"
    SITE_INSPECTION_CONSULTING = "site_inspection_consulting"

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="customer")

class ServiceProfessional(Base):
    __tablename__ = "service_professionals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)

    # In the new domain this represents the contractor's primary specialization
    # within civil construction (e.g. RCC work specialist, road contractor).
    service_category = Column(SQLEnum(ServiceCategory), nullable=False)
    experience_years = Column(Integer, default=0)

    # Rating fields retained for marketplace UX
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)

    # Daily rate in INR for contractor work (INR-only, integer storage)
    daily_rate_inr = Column(Integer, nullable=False)  # All monetary values stored as integer INR

    # Contractor-specific fields
    specialization = Column(String(255))  # e.g. "Residential structural work"
    license_number = Column(String(100))
    service_areas = Column(Text)  # Free-form description of cities / localities
    daily_availability_capacity = Column(Integer, default=1)  # Number of concurrent projects per day

    bio = Column(Text)
    is_available = Column(String(10), default="true")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="professional")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(SQLEnum(ServiceCategory), nullable=False)
    description = Column(Text)

    # All base costs are stored in INR as integers (no decimals).
    # Represents a typical cost range for the project type.
    base_cost_min_inr = Column(Integer, nullable=False)  # minimum estimated cost in INR
    base_cost_max_inr = Column(Integer, nullable=False)  # maximum estimated cost in INR

    # Estimated duration for the project type in days
    estimated_duration_days = Column(Integer, nullable=False)

    # Required skill level for the service: LOW / MEDIUM / HIGH
    required_skill_level = Column(String(10), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    professional_id = Column(Integer, ForeignKey("service_professionals.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    # For civil construction this represents the planned project start date.
    project_start_date = Column(DateTime, nullable=False)

    # Estimated duration of the project in days (multi-day projects).
    estimated_duration_days = Column(Integer, nullable=False)

    # Quoted project price in INR (integer, INR-only).
    quoted_price_inr = Column(Integer, nullable=False)  # All monetary values stored as integer INR

    address = Column(Text, nullable=False)
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.REQUESTED)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="bookings")
    professional = relationship("ServiceProfessional", back_populates="bookings")
    service = relationship("Service")

