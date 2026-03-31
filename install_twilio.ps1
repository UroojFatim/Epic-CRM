# Twilio CRM Communication Module Installer
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Twilio CRM Communication Module Installer" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Activating conda environment..." -ForegroundColor Yellow
& "C:\Users\Hp\anaconda3\shell\condabin\conda-hook.ps1"
conda activate crm

Write-Host ""
Write-Host "Step 2: Installing module twilio_crm_communication..." -ForegroundColor Yellow
python odoo-bin -c odoo.conf -d epiccrm -i twilio_crm_communication --stop-after-init --log-level=info

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "Installation successful!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Start Odoo: python odoo-bin -c odoo.conf" -ForegroundColor White
    Write-Host "2. Login to Odoo web interface" -ForegroundColor White
    Write-Host "3. Go to Settings -> Twilio (CRM Calls & SMS)" -ForegroundColor White
    Write-Host "4. Configure your Twilio credentials" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "Installation failed! Check the errors above." -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
