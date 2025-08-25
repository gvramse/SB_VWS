@echo off
echo Starting Django Workflow System...
echo.

REM Activate virtual environment
call .\venv\Scripts\activate.bat

REM Check if Django is installed
python -c "import django; print('Django version:', django.get_version())" 2>nul
if errorlevel 1 (
    echo Installing Django packages...
    pip install -r requirements.txt
)

REM Apply migrations
echo Applying database migrations...
python manage.py migrate

REM Start development server
echo Starting development server...
echo.
echo Application will be available at: http://127.0.0.1:8000
echo Admin panel: http://127.0.0.1:8000/admin
echo.
echo Press Ctrl+C to stop the server
python manage.py runserver 127.0.0.1:8000
