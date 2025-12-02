@echo off
echo ========================================
echo Solar Farm Optimizer - Quick Setup
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.11+
    pause
    exit /b 1
)
echo.

echo [2/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate
echo.

echo [4/5] Installing dependencies...
echo This may take 5-10 minutes...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

echo [5/5] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo Created .env file - please edit with your API keys
) else (
    echo .env file already exists
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys (optional)
echo 2. Generate demo images: python demo_data\generate_demo_images.py
echo 3. Run dashboard: streamlit run app.py
echo.
echo Press any key to generate demo images now...
pause >nul

echo.
echo Generating demo images...
python demo_data\generate_demo_images.py
echo.

echo ========================================
echo All Done!
echo ========================================
echo.
echo To launch the dashboard run:
echo   streamlit run app.py
echo.
pause
