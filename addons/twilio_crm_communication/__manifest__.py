# -*- coding: utf-8 -*-
{
    'name': 'Twilio Calls & SMS from CRM Leads',
    'version': '17.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Twilio Calls & SMS from CRM Leads',
    'description': """
Twilio CRM Communication
========================
Make calls and send SMS from CRM leads using Twilio.
    """,
    'author': 'Aitek Solutions',
    'website': 'https://www.odoo.com',
    'depends': ['base', 'crm', 'mail', 'contacts'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_view.xml',
        'views/crm_lead_view.xml',
        'views/twilio_logs_views.xml',
        'wizard/twilio_sms_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
