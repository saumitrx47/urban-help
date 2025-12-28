# ServiceHub - Service Booking Platform

A modern service booking platform similar to Urban Company, built with FastAPI, PostgreSQL, and OpenAI integration.

## Features

- 🏠 **Service Categories**: Cleaning, Plumbing, Electrical, Beauty, Massage, Appliance Repair, Carpentry, Painting
- 👥 **Service Professionals**: Browse verified professionals with ratings and reviews
- 📅 **Booking System**: Easy booking flow with date/time selection
- 🤖 **AI Recommendations**: OpenAI-powered service recommendations
- 📱 **Responsive Design**: Modern, mobile-friendly UI
- ✅ **Booking Management**: View and manage your bookings

## Tech Stack

- **Frontend**: HTML + CSS + JavaScript (Jinja2 templates)
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **AI**: OpenAI API (GPT-3.5-turbo)
- **Hosting**: Railway / Render ready

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Database Setup

Create a PostgreSQL database and set up the connection string:

```bash
# Create .env file
cp .env.example .env

# Edit .env with your database URL and OpenAI API key
DATABASE_URL=postgresql://user:password@localhost:5432/booking_db
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

### 3. Initialize Database and Seed Data

```bash
# Run the seed script to create tables and populate initial data
python seed_data.py
```

### 4. Run the Application

```bash
# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000` in your browser.

## Deployment

### Railway

1. Connect your GitHub repository to Railway
2. Add environment variables:
   - `DATABASE_URL` (Railway will auto-create a PostgreSQL database)
   - `OPENAI_API_KEY`
   - `SECRET_KEY`
3. Deploy! Railway will automatically detect the Python app and use the `railway.json` configuration.

### Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables:
   - `DATABASE_URL` (create a PostgreSQL database on Render)
   - `OPENAI_API_KEY`
   - `SECRET_KEY`
5. Deploy!

Alternatively, use the `render.yaml` file for automated setup.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── ai_service.py        # OpenAI integration
├── templates/               # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── services.html
│   ├── professionals.html
│   ├── book.html
│   ├── booking_confirmation.html
│   └── my_bookings.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── requirements.txt
├── seed_data.py            # Database seeding script
├── railway.json            # Railway deployment config
├── render.yaml             # Render deployment config
└── README.md
```

## API Endpoints

- `GET /` - Home page
- `GET /services` - Browse services (with optional category filter)
- `GET /professionals` - View service professionals
- `GET /book/{professional_id}` - Booking form
- `POST /book/{professional_id}` - Create booking
- `GET /booking/{booking_id}` - Booking confirmation
- `GET /my-bookings` - View customer bookings
- `POST /api/ai-recommendation` - Get AI service recommendations
- `GET /api/services` - API endpoint for services
- `GET /api/professionals` - API endpoint for professionals

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key for AI recommendations
- `SECRET_KEY`: Secret key for session management (generate a random string)

## License

MIT License

