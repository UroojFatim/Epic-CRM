@echo off
echo ================================================
echo Twilio CRM Communication Module Installer
echo ================================================
echo.

echo Step 1: Activating conda environment...
call C:\Users\Hp\anaconda3\shell\condabin\conda-hook.ps1
call conda activate crm

echo.
echo Step 2: Installing module twilio_crm_communication...
python odoo-bin -c odoo.conf -d epiccrm -i twilio_crm_communication --stop-after-init --log-level=info

echo.
echo ================================================
echo Installation complete!
echo ================================================
echo.
echo Next steps:
echo 1. Start Odoo: python odoo-bin -c odoo.conf
echo 2. Login to Odoo web interface
echo 3. Go to Settings and configure Twilio credentials
echo.
pause
