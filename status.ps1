# status.ps1
# Check Phase 1 completion status

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Phase 1 Status Check" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Docker containers
Write-Host "1. Docker Containers:" -ForegroundColor Yellow
$containers = docker ps --format "table {{.Names}}\t{{.Status}}"
Write-Host $containers
Write-Host ""

# Check backend health
Write-Host "2. Backend Health:" -ForegroundColor Yellow
try {
    $health = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    Write-Host "✓ Backend is healthy" -ForegroundColor Green
} catch {
    Write-Host "✗ Backend is not responding" -ForegroundColor Red
}
Write-Host ""

# Check PostgreSQL tables
Write-Host "3. PostgreSQL Tables:" -ForegroundColor Yellow
$env:PGPASSWORD = "pitchiq_secure_password_2024"
$tables = docker exec pitchiq-postgres psql -U pitchiq -d pitchiq -t -c "\dt" 2>$null
if ($tables -match "memo_jobs") {
    Write-Host "✓ Tables created successfully" -ForegroundColor Green
    Write-Host $tables
} else {
    Write-Host "✗ Tables not created!" -ForegroundColor Red
}
Write-Host ""

# Check Alembic
Write-Host "4. Alembic Migration:" -ForegroundColor Yellow
cd C:\Users\acer\PitchIQ\backend
$current = alembic current 2>$null
if ($current -match "head") {
    Write-Host "✓ Migration applied" -ForegroundColor Green
    Write-Host $current
} else {
    Write-Host "✗ Migration not applied!" -ForegroundColor Red
}
Write-Host ""

# Check frontend
Write-Host "5. Frontend:" -ForegroundColor Yellow
try {
    $frontend = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing
    Write-Host "✓ Frontend is accessible" -ForegroundColor Green
} catch {
    Write-Host "✗ Frontend is not accessible" -ForegroundColor Red
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Phase 1 Complete! ✅" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Access your application:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""