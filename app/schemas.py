from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models import BookingStatus, ServiceCategory

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProfessionalCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    service_category: ServiceCategory
    experience_years: int = 0
    # Daily rate in INR (integer, INR-only)
    daily_rate_inr: int
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    service_areas: Optional[str] = None
    daily_availability_capacity: int = 1
    bio: Optional[str] = None

class ProfessionalResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    service_category: ServiceCategory
    experience_years: int
    rating: float
    total_reviews: int
    daily_rate_inr: int
    specialization: Optional[str]
    license_number: Optional[str]
    service_areas: Optional[str]
    daily_availability_capacity: int
    bio: Optional[str]
    is_available: str
    
    class Config:
        from_attributes = True

class ServiceCreate(BaseModel):
    name: str
    category: ServiceCategory
    description: Optional[str] = None
    # Base cost range in INR (integers, INR-only)
    base_cost_min_inr: int
    base_cost_max_inr: int
    # Estimated duration for the project type in days
    estimated_duration_days: int
    # Required skill level: LOW / MEDIUM / HIGH
    required_skill_level: str

class ServiceResponse(BaseModel):
    id: int
    name: str
    category: ServiceCategory
    description: Optional[str]
    base_cost_min_inr: int
    base_cost_max_inr: int
    estimated_duration_days: int
    required_skill_level: str
    
    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    customer_id: int
    professional_id: int
    service_id: int
    # Project start date for civil construction projects
    project_start_date: datetime
    # Estimated project duration in days
    estimated_duration_days: int
    # Quoted project price in INR (integer, INR-only)
    quoted_price_inr: int
    address: str
    notes: Optional[str] = None

class BookingResponse(BaseModel):
    id: int
    customer_id: int
    professional_id: int
    service_id: int
    project_start_date: datetime
    estimated_duration_days: int
    quoted_price_inr: int
    address: str
    status: BookingStatus
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

