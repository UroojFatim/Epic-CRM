#!/usr/bin/env python3
import subprocess
import sys

# Run Odoo shell command to check module
cmd = '''
module = env['ir.module.module'].search([('name', '=', 'twilio_crm_communication')])
if module:
    print("Module FOUND in database")
    print(f"  Name: {module.name}")
    print(f"  State: {module.state}")
    print(f"  Installed: {module.state == 'installed'}")
    print(f"  Summary: {module.summary}")
else:
    print("Module NOT FOUND in database")
    print("  This means Odoo has not scanned the module yet")
'''

print("Checking module status in database...")
print("=" * 60)

result = subprocess.run(
    ['python', 'odoo-bin', 'shell', '-c', 'odoo.conf', '-d', 'epiccrm', '--no-http'],
    input=cmd,
    capture_output=True,
    text=True,
    timeout=30
)

print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)
