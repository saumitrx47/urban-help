from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional
import os

from app.database import get_db, engine, Base
from app import models, schemas
from app.ai_service import get_service_recommendations

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Service Booking Platform")

# Templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with service categories"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/services", response_class=HTMLResponse)
async def services_page(request: Request, category: Optional[str] = None, db: Session = Depends(get_db)):
    """Services listing page"""
    query = db.query(models.Service)
    if category:
        try:
            category_enum = models.ServiceCategory[category.upper()]
            query = query.filter(models.Service.category == category_enum)
        except:
            pass
    
    services = query.all()
    categories = [cat.value for cat in models.ServiceCategory]
    
    return templates.TemplateResponse("services.html", {
        "request": request,
        "services": services,
        "categories": categories,
        "selected_category": category
    })

@app.get("/professionals", response_class=HTMLResponse)
async def professionals_page(
    request: Request, 
    service_id: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Service professionals listing page"""
    query = db.query(models.ServiceProfessional).filter(
        models.ServiceProfessional.is_available == "true"
    )
    
    if service_id:
        service = db.query(models.Service).filter(models.Service.id == service_id).first()
        if service:
            query = query.filter(models.ServiceProfessional.service_category == service.category)
    elif category:
        try:
            category_enum = models.ServiceCategory[category.upper()]
            query = query.filter(models.ServiceProfessional.service_category == category_enum)
        except:
            pass
    
    professionals = query.order_by(models.ServiceProfessional.rating.desc()).all()
    
    service = None
    if service_id:
        service = db.query(models.Service).filter(models.Service.id == service_id).first()
    
    return templates.TemplateResponse("professionals.html", {
        "request": request,
        "professionals": professionals,
        "service": service
    })

@app.get("/book/{professional_id}", response_class=HTMLResponse)
async def book_page(request: Request, professional_id: int, service_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Booking page"""
    professional = db.query(models.ServiceProfessional).filter(
        models.ServiceProfessional.id == professional_id
    ).first()
    
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    
    service = None
    if service_id:
        service = db.query(models.Service).filter(models.Service.id == service_id).first()
    
    services = db.query(models.Service).filter(
        models.Service.category == professional.service_category
    ).all()
    
    return templates.TemplateResponse("book.html", {
        "request": request,
        "professional": professional,
        "service": service,
        "services": services
    })

@app.post("/book/{professional_id}")
async def create_booking(
    professional_id: int,
    request: Request,
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    customer_address: str = Form(...),
    service_id: int = Form(...),
    booking_date: str = Form(...),
    booking_time: str = Form(...),
    duration_hours: float = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a booking"""
    # Get or create customer
    customer = db.query(models.Customer).filter(
        models.Customer.email == customer_email
    ).first()
    
    if not customer:
        customer = models.Customer(
            name=customer_name,
            email=customer_email,
            phone=customer_phone,
            address=customer_address
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
    
    # Get service
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Parse booking date and time
    booking_datetime = datetime.strptime(f"{booking_date} {booking_time}", "%Y-%m-%d %H:%M")
    
    # Calculate total price
    professional = db.query(models.ServiceProfessional).filter(
        models.ServiceProfessional.id == professional_id
    ).first()
    total_price = professional.hourly_rate * duration_hours
    
    # Create booking
    booking = models.Booking(
        customer_id=customer.id,
        professional_id=professional_id,
        service_id=service_id,
        booking_date=booking_datetime,
        duration_hours=duration_hours,
        total_price=total_price,
        address=customer_address,
        status=models.BookingStatus.PENDING,
        notes=notes
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    return RedirectResponse(url=f"/booking/{booking.id}", status_code=303)

@app.get("/booking/{booking_id}", response_class=HTMLResponse)
async def booking_confirmation(request: Request, booking_id: int, db: Session = Depends(get_db)):
    """Booking confirmation page"""
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return templates.TemplateResponse("booking_confirmation.html", {
        "request": request,
        "booking": booking
    })

@app.get("/my-bookings", response_class=HTMLResponse)
async def my_bookings(request: Request, email: str, db: Session = Depends(get_db)):
    """Customer's bookings page"""
    customer = db.query(models.Customer).filter(models.Customer.email == email).first()
    
    if not customer:
        return templates.TemplateResponse("my_bookings.html", {
            "request": request,
            "bookings": [],
            "customer": None
        })
    
    bookings = db.query(models.Booking).filter(
        models.Booking.customer_id == customer.id
    ).order_by(models.Booking.booking_date.desc()).all()
    
    return templates.TemplateResponse("my_bookings.html", {
        "request": request,
        "bookings": bookings,
        "customer": customer
    })

@app.post("/api/ai-recommendation")
async def ai_recommendation(request: Request, query: str = Form(...), db: Session = Depends(get_db)):
    """Get AI-powered service recommendations"""
    services = db.query(models.Service).all()
    services_list = [{"name": s.name, "description": s.description or ""} for s in services]
    
    recommendation = get_service_recommendations(query, services_list)
    
    return templates.TemplateResponse("ai_recommendation.html", {
        "request": request,
        "recommendation": recommendation,
        "query": query
    })

# API endpoints for data
@app.get("/api/services", response_model=List[schemas.ServiceResponse])
async def get_services(db: Session = Depends(get_db)):
    """Get all services"""
    return db.query(models.Service).all()

@app.get("/api/professionals", response_model=List[schemas.ProfessionalResponse])
async def get_professionals(category: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all professionals"""
    query = db.query(models.ServiceProfessional).filter(
        models.ServiceProfessional.is_available == "true"
    )
    
    if category:
        try:
            category_enum = models.ServiceCategory[category.upper()]
            query = query.filter(models.ServiceProfessional.service_category == category_enum)
        except:
            pass
    
    return query.all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

