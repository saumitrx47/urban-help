from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ServiceCategory(enum.Enum):
    CLEANING = "cleaning"
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    BEAUTY = "beauty"
    MASSAGE = "massage"
    APPLIANCE_REPAIR = "appliance_repair"
    CARPENTRY = "carpentry"
    PAINTING = "painting"

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
    service_category = Column(SQLEnum(ServiceCategory), nullable=False)
    experience_years = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    hourly_rate = Column(Float, nullable=False)
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
    base_price = Column(Float, nullable=False)
    duration_hours = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    professional_id = Column(Integer, ForeignKey("service_professionals.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False)
    duration_hours = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    address = Column(Text, nullable=False)
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="bookings")
    professional = relationship("ServiceProfessional", back_populates="bookings")
    service = relationship("Service")

