@echo off
echo ========================================
echo    PitchIQ Docker Build Script
echo ========================================
echo.

echo Step 1: Checking Docker...
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop first.
    pause
    exit /b 1
)
echo Docker is running!
echo.

echo Step 2: Checking environment file...
if not exist .env (
    echo Creating .env file from .env.example...
    if exist .env.example (
        copy .env.example .env
        echo.
        echo IMPORTANT: Please edit .env and add your GOOGLE_API_KEY!
        echo.
        pause
    ) else (
        echo ERROR: .env.example not found!
        pause
        exit /b 1
    )
)
echo.

echo Step 3: Building Docker images...
docker-compose build
if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)
echo.

echo Step 4: Starting containers...
docker-compose up -d
if errorlevel 1 (
    echo Failed to start containers!
    pause
    exit /b 1
)
echo.

echo ========================================
echo    PitchIQ is running!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
docker-compose ps
echo.
echo To view logs: docker-compose logs -f
echo To stop:      docker-compose down
echo.
pause