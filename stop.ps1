# stop.ps1
Write-Host "Stopping PitchIQ containers..." -ForegroundColor Yellow
docker-compose down
Write-Host "✅ Containers stopped" -ForegroundColor Green