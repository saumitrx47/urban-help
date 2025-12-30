from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional
import os
import logging

from app.database import get_db, engine, Base
from app import models, schemas
from app.ai_service import get_service_recommendations

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

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
    try:
        query = db.query(models.Service)
        if category:
            try:
                category_enum = models.ServiceCategory[category.upper()]
                query = query.filter(models.Service.category == category_enum)
            except (KeyError, AttributeError) as e:
                logger.warning(f"Invalid category filter: {category}, error: {e}")
                pass
        
        services = query.all() or []
        categories = [cat.value for cat in models.ServiceCategory]
        
        return templates.TemplateResponse("services.html", {
            "request": request,
            "services": services,
            "categories": categories,
            "selected_category": category
        })
    except Exception as e:
        logger.error(f"Error in services_page: {e}", exc_info=True)
        return templates.TemplateResponse("services.html", {
            "request": request,
            "services": [],
            "categories": [],
            "selected_category": None
        })

@app.get("/professionals", response_class=HTMLResponse)
async def professionals_page(
    request: Request, 
    service_id: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Contractors listing page (civil construction contractors)"""
    try:
        query = db.query(models.ServiceProfessional).filter(
            models.ServiceProfessional.is_available == "true"
        )
        
        service = None
        if service_id:
            service = db.query(models.Service).filter(models.Service.id == service_id).first()
            if service:
                query = query.filter(models.ServiceProfessional.service_category == service.category)
        elif category:
            try:
                category_enum = models.ServiceCategory[category.upper()]
                query = query.filter(models.ServiceProfessional.service_category == category_enum)
            except (KeyError, AttributeError) as e:
                logger.warning(f"Invalid category filter: {category}, error: {e}")
                pass
        
        professionals = query.order_by(models.ServiceProfessional.rating.desc()).all() or []
        
        return templates.TemplateResponse("professionals.html", {
            "request": request,
            "professionals": professionals,
            "service": service
        })
    except Exception as e:
        logger.error(f"Error in professionals_page: {e}", exc_info=True)
        return templates.TemplateResponse("professionals.html", {
            "request": request,
            "professionals": [],
            "service": None
        })

@app.get("/book/{professional_id}", response_class=HTMLResponse)
async def book_page(request: Request, professional_id: int, service_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Project request page (request quote from contractor)"""
    try:
        professional = db.query(models.ServiceProfessional).filter(
            models.ServiceProfessional.id == professional_id
        ).first()
        
        if not professional:
            raise HTTPException(status_code=404, detail="Contractor not found")
        
        service = None
        if service_id:
            service = db.query(models.Service).filter(models.Service.id == service_id).first()
        
        services = db.query(models.Service).filter(
            models.Service.category == professional.service_category
        ).all() or []
        
        return templates.TemplateResponse("book.html", {
            "request": request,
            "professional": professional,
            "service": service,
            "services": services
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in book_page: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error loading booking page")

@app.post("/book/{professional_id}")
async def create_booking(
    professional_id: int,
    request: Request,
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    customer_address: str = Form(...),
    service_id: int = Form(...),
    # Project start date for the construction project
    project_start_date: str = Form(...),
    # Estimated duration in days for the project
    estimated_duration_days: int = Form(...),
    # Quoted project price in INR (integer)
    quoted_price_inr: int = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a project request/booking (multi-day construction project)"""
    try:
        # Verify professional exists
        professional = db.query(models.ServiceProfessional).filter(
            models.ServiceProfessional.id == professional_id
        ).first()
        if not professional:
            raise HTTPException(status_code=404, detail="Contractor not found")
        
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
        
        # Parse project start date (date only, assume 09:00 as default start time)
        try:
            project_start_datetime = datetime.strptime(project_start_date, "%Y-%m-%d")
        except ValueError as e:
            logger.error(f"Invalid date format: {project_start_date}, error: {e}")
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Create booking
        booking = models.Booking(
            customer_id=customer.id,
            professional_id=professional_id,
            service_id=service_id,
            project_start_date=project_start_datetime,
            estimated_duration_days=estimated_duration_days,
            quoted_price_inr=quoted_price_inr,
            address=customer_address,
            status=models.BookingStatus.REQUESTED,
            notes=notes
        )
        
        db.add(booking)
        db.commit()
        db.refresh(booking)
        
        return RedirectResponse(url=f"/booking/{booking.id}", status_code=303)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating booking: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating project request")

@app.get("/booking/{booking_id}", response_class=HTMLResponse)
async def booking_confirmation(request: Request, booking_id: int, db: Session = Depends(get_db)):
    """Project request confirmation page"""
    try:
        # Eagerly load relationships to avoid lazy loading issues
        booking = db.query(models.Booking).options(
            joinedload(models.Booking.customer),
            joinedload(models.Booking.professional),
            joinedload(models.Booking.service)
        ).filter(models.Booking.id == booking_id).first()
        
        if not booking:
            raise HTTPException(status_code=404, detail="Project request not found")
        
        return templates.TemplateResponse("booking_confirmation.html", {
            "request": request,
            "booking": booking
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in booking_confirmation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error loading project confirmation")

@app.get("/my-bookings", response_class=HTMLResponse)
async def my_bookings(request: Request, email: str, db: Session = Depends(get_db)):
    """Customer's projects page"""
    try:
        customer = db.query(models.Customer).filter(models.Customer.email == email).first()
        
        if not customer:
            return templates.TemplateResponse("my_bookings.html", {
                "request": request,
                "bookings": [],
                "customer": None
            })
        
        # Eagerly load relationships to avoid lazy loading issues
        bookings = db.query(models.Booking).options(
            joinedload(models.Booking.customer),
            joinedload(models.Booking.professional),
            joinedload(models.Booking.service)
        ).filter(
            models.Booking.customer_id == customer.id
        ).order_by(models.Booking.project_start_date.desc()).all() or []
        
        return templates.TemplateResponse("my_bookings.html", {
            "request": request,
            "bookings": bookings,
            "customer": customer
        })
    except Exception as e:
        logger.error(f"Error in my_bookings: {e}", exc_info=True)
        return templates.TemplateResponse("my_bookings.html", {
            "request": request,
            "bookings": [],
            "customer": None
        })

@app.post("/api/ai-recommendation")
async def ai_recommendation(request: Request, query: str = Form(...), db: Session = Depends(get_db)):
    """Get AI-powered service recommendations"""
    try:
        services = db.query(models.Service).all() or []
        services_list = [{"name": s.name, "description": s.description or ""} for s in services]
        
        recommendation = get_service_recommendations(query, services_list)
        
        return templates.TemplateResponse("ai_recommendation.html", {
            "request": request,
            "recommendation": recommendation,
            "query": query
        })
    except Exception as e:
        logger.error(f"Error in ai_recommendation: {e}", exc_info=True)
        # Return a safe fallback response
        return templates.TemplateResponse("ai_recommendation.html", {
            "request": request,
            "recommendation": "I'd be happy to help you plan your construction project. Please review the available civil construction services above and choose the one that best matches your requirements.",
            "query": query
        })

# API endpoints for data
@app.get("/api/services", response_model=List[schemas.ServiceResponse])
async def get_services(db: Session = Depends(get_db)):
    """Get all services"""
    try:
        return db.query(models.Service).all() or []
    except Exception as e:
        logger.error(f"Error in get_services API: {e}", exc_info=True)
        return []

@app.get("/api/professionals", response_model=List[schemas.ProfessionalResponse])
async def get_professionals(category: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all professionals"""
    try:
        query = db.query(models.ServiceProfessional).filter(
            models.ServiceProfessional.is_available == "true"
        )
        
        if category:
            try:
                category_enum = models.ServiceCategory[category.upper()]
                query = query.filter(models.ServiceProfessional.service_category == category_enum)
            except (KeyError, AttributeError) as e:
                logger.warning(f"Invalid category filter: {category}, error: {e}")
                pass
        
        return query.all() or []
    except Exception as e:
        logger.error(f"Error in get_professionals API: {e}", exc_info=True)
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

