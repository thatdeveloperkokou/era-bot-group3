#!/bin/bash

# Setup script for environment variables
# This script helps you create .env files for both frontend and backend

echo "🚀 Setting up environment variables..."
echo ""

# Backend .env
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env file..."
    cp backend/env.example backend/.env
    echo "✅ Created backend/.env"
    echo "⚠️  Please edit backend/.env and add your email configuration"
else
    echo "ℹ️  backend/.env already exists"
fi

# Frontend .env
if [ ! -f "frontend/.env" ]; then
    echo "📝 Creating frontend/.env file..."
    cp frontend/env.example frontend/.env
    echo "✅ Created frontend/.env"
    echo "⚠️  Please edit frontend/.env and add your Google Places API key"
else
    echo "ℹ️  frontend/.env already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your email configuration"
echo "2. Edit frontend/.env and add your Google Places API key"
echo "3. Restart your servers"
echo ""
echo "For detailed instructions, see SETUP_GUIDE.md"

