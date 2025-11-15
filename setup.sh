#!/bin/bash

# Project Noter Backend Setup Script

echo "🚀 Setting up Project Noter Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🗄️  Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "📊 Populating Program Learning Outcomes..."
python manage.py populate_plos

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the development server:"
echo "  1. source venv/bin/activate"
echo "  2. python manage.py runserver"
echo ""
echo "To create an admin user:"
echo "  python manage.py createsuperuser"
echo ""
echo "API will be available at: http://localhost:8000/api/"
echo "Admin panel will be at: http://localhost:8000/admin/"
