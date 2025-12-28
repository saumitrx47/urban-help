#!/bin/bash

# Quick start script for ServiceHub

echo "🚀 Starting ServiceHub..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please update it with your database URL and OpenAI API key."
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check if database is set up
echo "📦 Setting up database..."
python3 seed_data.py

# Start the server
echo "🌐 Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

