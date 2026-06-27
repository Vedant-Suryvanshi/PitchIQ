# restart.ps1
Write-Host "Restarting PitchIQ..." -ForegroundColor Yellow
docker-compose restart
Write-Host "✅ Containers restarted" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "Backend:  http://localhost:8000" -ForegroundColor White