# postgres_helper.ps1
# Helper script for PostgreSQL commands

$PGPASSWORD = "pitchiq_secure_password_2024"

function Show-Menu {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   PostgreSQL Helper" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Connect to database" -ForegroundColor Yellow
    Write-Host "2. View all jobs" -ForegroundColor Yellow
    Write-Host "3. View all results" -ForegroundColor Yellow
    Write-Host "4. View all users" -ForegroundColor Yellow
    Write-Host "5. Export full database (SQL)" -ForegroundColor Yellow
    Write-Host "6. Export jobs to CSV" -ForegroundColor Yellow
    Write-Host "7. Show statistics" -ForegroundColor Yellow
    Write-Host "8. Export all tables to CSV" -ForegroundColor Yellow
    Write-Host "9. Exit" -ForegroundColor Yellow
    Write-Host ""
}

function Connect-DB {
    docker exec -e PGPASSWORD=$PGPASSWORD -it pitchiq-postgres psql -U pitchiq -d pitchiq
}

function View-Jobs {
    Write-Host "`nMEMO JOBS:" -ForegroundColor Cyan
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "SELECT id, startup_description, status, created_at FROM memo_jobs ORDER BY created_at DESC;"
}

function View-Results {
    Write-Host "`nMEMO RESULTS:" -ForegroundColor Cyan
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "SELECT job_id, startup_name, confidence_score, created_at FROM memo_results ORDER BY created_at DESC;"
}

function View-Users {
    Write-Host "`nUSERS:" -ForegroundColor Cyan
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "SELECT username, email, is_active, created_at FROM users ORDER BY created_at DESC;"
}

function Export-SQL {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filename = "backup_$timestamp.sql"
    Write-Host "Exporting database to $filename ..." -ForegroundColor Yellow
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres pg_dump -U pitchiq -d pitchiq > $filename
    Write-Host "SUCCESS: Exported to $filename" -ForegroundColor Green
}

function Export-CSV-Jobs {
    Write-Host "Exporting jobs to memo_jobs.csv ..." -ForegroundColor Yellow
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "\COPY memo_jobs TO STDOUT CSV HEADER" > memo_jobs.csv
    Write-Host "SUCCESS: Exported jobs to memo_jobs.csv" -ForegroundColor Green
}

function Export-All-CSV {
    Write-Host "Exporting all tables to CSV ..." -ForegroundColor Yellow
    
    Write-Host "  Exporting memo_jobs..." -ForegroundColor Gray
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "\COPY memo_jobs TO STDOUT CSV HEADER" > memo_jobs.csv
    
    Write-Host "  Exporting memo_results..." -ForegroundColor Gray
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "\COPY memo_results TO STDOUT CSV HEADER" > memo_results.csv
    
    Write-Host "  Exporting users..." -ForegroundColor Gray
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "\COPY users TO STDOUT CSV HEADER" > users.csv
    
    Write-Host "SUCCESS: All tables exported to CSV" -ForegroundColor Green
}

function Show-Stats {
    Write-Host "`nSTATISTICS:" -ForegroundColor Cyan
    Write-Host "Table Counts:" -ForegroundColor Yellow
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "SELECT 'memo_jobs' as table_name, COUNT(*) as count FROM memo_jobs UNION SELECT 'memo_results', COUNT(*) FROM memo_results UNION SELECT 'users', COUNT(*) FROM users;"
    
    Write-Host "`nJobs by Status:" -ForegroundColor Yellow
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "SELECT status, COUNT(*) FROM memo_jobs GROUP BY status;"
    
    Write-Host "`nAverage Confidence Score:" -ForegroundColor Yellow
    docker exec -e PGPASSWORD=$PGPASSWORD pitchiq-postgres psql -U pitchiq -d pitchiq -c "SELECT AVG(confidence_score) as avg_confidence FROM memo_results;"
}

# Main loop
do {
    Show-Menu
    $choice = Read-Host "Enter your choice"
    
    switch ($choice) {
        "1" { Connect-DB }
        "2" { View-Jobs }
        "3" { View-Results }
        "4" { View-Users }
        "5" { Export-SQL }
        "6" { Export-CSV-Jobs }
        "7" { Show-Stats }
        "8" { Export-All-CSV }
        "9" { Write-Host "Goodbye!" -ForegroundColor Green; break }
        default { Write-Host "Invalid choice! Please enter 1-9" -ForegroundColor Red }
    }
    
    if ($choice -ne "9") {
        Write-Host ""
        Read-Host "Press Enter to continue"
        Clear-Host
    }
} while ($choice -ne "9")