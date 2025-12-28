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
    hourly_rate: float
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
    hourly_rate: float
    bio: Optional[str]
    is_available: str
    
    class Config:
        from_attributes = True

class ServiceCreate(BaseModel):
    name: str
    category: ServiceCategory
    description: Optional[str] = None
    base_price: float
    duration_hours: float

class ServiceResponse(BaseModel):
    id: int
    name: str
    category: ServiceCategory
    description: Optional[str]
    base_price: float
    duration_hours: float
    
    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    customer_id: int
    professional_id: int
    service_id: int
    booking_date: datetime
    duration_hours: float
    address: str
    notes: Optional[str] = None

class BookingResponse(BaseModel):
    id: int
    customer_id: int
    professional_id: int
    service_id: int
    booking_date: datetime
    duration_hours: float
    total_price: float
    address: str
    status: BookingStatus
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

