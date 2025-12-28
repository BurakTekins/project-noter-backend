# Backend endpoint'lerini PowerShell ile test etmek için script
# Kullanım: .\test_api_endpoints.ps1 <student_id>

param(
    [int]$StudentId = 1
)

$BaseUrl = "http://localhost:8000/api"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Testing Backend Endpoints" -ForegroundColor Cyan
Write-Host "Student ID: $StudentId" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Enrollments
Write-Host "1. Testing /students/$StudentId/enrollments/" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/students/$StudentId/enrollments/" -Method Get
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""
Write-Host ""

# Test 2: Courses
Write-Host "2. Testing /students/$StudentId/courses/" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/students/$StudentId/courses/" -Method Get
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""
Write-Host ""

# Test 3: Learning Outcomes
Write-Host "3. Testing /students/$StudentId/learning-outcomes/" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/students/$StudentId/learning-outcomes/" -Method Get
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Test Complete" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

