import sys
sys.path.insert(0, '.')
from odoo import api, SUPERUSER_ID
from odoo.tools import config

config.parse_config(['-c', 'odoo.conf'])
db = 'epiccrm'

try:
    registry = api.Registry(db)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        module = env['ir.module.module'].search([('name', '=', 'twilio_crm_communication')], limit=1)
        if module:
            print(f'Module found!')
            print(f'  ID: {module.id}')
            print(f'  State: {module.state}')
            print(f'  Summary: {module.summary}')
            print(f'  Category: {module.category_id.name if module.category_id else "N/A"}')
        else:
            print('Module NOT FOUND in database')
            print('Checking if module exists in filesystem...')
            import os
            path = 'addons/twilio_crm_communication/__manifest__.py'
            print(f'  Manifest exists: {os.path.exists(path)}')
except Exception as e:
    print(f'Error: {e}')
