#!/bin/bash

echo "========================================"
echo "Solar Farm Optimizer - Quick Setup"
echo "========================================"
echo ""

echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found! Please install Python 3.11+"
    exit 1
fi
python3 --version
echo ""

echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi
echo ""

echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo ""

echo "[4/5] Installing dependencies..."
echo "This may take 5-10 minutes..."
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ""

echo "[5/5] Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file - please edit with your API keys"
else
    echo ".env file already exists"
fi
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys (optional)"
echo "2. Generate demo images: python demo_data/generate_demo_images.py"
echo "3. Run dashboard: streamlit run app.py"
echo ""
read -p "Generate demo images now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Generating demo images..."
    python demo_data/generate_demo_images.py
    echo ""
fi

echo "========================================"
echo "All Done!"
echo "========================================"
echo ""
echo "To launch the dashboard run:"
echo "  streamlit run app.py"
echo ""
