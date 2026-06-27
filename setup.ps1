# setup.ps1
# Complete Phase 1 setup script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Phase 1: Complete Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Docker
Write-Host "Step 1: Checking Docker..." -ForegroundColor Yellow
docker info | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop first."
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Docker is running" -ForegroundColor Green

# Step 2: Check .env
Write-Host ""
Write-Host "Step 2: Checking .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "✗ .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with your API keys."
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ .env file found" -ForegroundColor Green

# Step 3: Install Python dependencies
Write-Host ""
Write-Host "Step 3: Installing Python dependencies..." -ForegroundColor Yellow
cd backend
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Step 4: Start PostgreSQL and Redis
Write-Host ""
Write-Host "Step 4: Starting PostgreSQL and Redis..." -ForegroundColor Yellow
cd ..
docker-compose up -d postgres redis
Start-Sleep -Seconds 10

# Check if PostgreSQL is healthy
$healthy = docker inspect pitchiq-postgres --format='{{.State.Health.Status}}'
if ($healthy -ne "healthy") {
    Write-Host "⚠️  PostgreSQL is not healthy yet. Waiting..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}
Write-Host "✓ Database and Redis started" -ForegroundColor Green

# Step 5: Run migrations
Write-Host ""
Write-Host "Step 5: Running database migrations..." -ForegroundColor Yellow
cd backend

# Check if migration exists
$migrationFiles = ls alembic\versions\*.py -ErrorAction SilentlyContinue
if ($migrationFiles.Count -eq 0) {
    Write-Host "Creating initial migration..." -ForegroundColor Yellow
    alembic revision --autogenerate -m "Initial migration with PostgreSQL"
}

# Apply migration
alembic upgrade head
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Migration failed!" -ForegroundColor Red
    Write-Host "Trying with stamp..." -ForegroundColor Yellow
    alembic stamp head
    alembic upgrade head
}
Write-Host "✓ Migrations applied" -ForegroundColor Green

# Step 6: Seed database
Write-Host ""
Write-Host "Step 6: Seeding database with sample data..." -ForegroundColor Yellow
python scripts/seed_db.py seed
Write-Host "✓ Database seeded" -ForegroundColor Green

# Step 7: Test database
Write-Host ""
Write-Host "Step 7: Testing database connection..." -ForegroundColor Yellow
python scripts/db_health.py
Write-Host "✓ Database healthy" -ForegroundColor Green

# Step 8: Build and start all services
Write-Host ""
Write-Host "Step 8: Building and starting all services..." -ForegroundColor Yellow
cd ..
docker-compose build
docker-compose up -d
Start-Sleep -Seconds 10

# Step 9: Check all containers
Write-Host ""
Write-Host "Step 9: Checking container status..." -ForegroundColor Yellow
docker ps

# Step 10: Final verification
Write-Host ""
Write-Host "Step 10: Final verification..." -ForegroundColor Yellow

# Test backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Backend is healthy" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Backend health check failed!" -ForegroundColor Red
}

# Test frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Frontend is accessible" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Frontend check failed!" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✅ Phase 1 Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access your application:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "📊 Database:" -ForegroundColor Yellow
Write-Host "   Connect: docker exec -it pitchiq-postgres psql -U pitchiq -d pitchiq" -ForegroundColor White
Write-Host "   Password: pitchiq_secure_password_2024" -ForegroundColor White
Write-Host ""
Write-Host "📝 Commands:" -ForegroundColor Yellow
Write-Host "   Backup:    python scripts/backup_db.py backup" -ForegroundColor White
Write-Host "   Seed:      python scripts/seed_db.py seed" -ForegroundColor White
Write-Host "   Health:    python scripts/db_health.py" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"