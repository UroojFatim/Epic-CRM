# -*- coding: utf-8 -*-
{
    "name": "CRM Telephony (Base)",
    "version": "17.0.1.0.0",
    "category": "CRM",
    "summary": "Provider-agnostic telephony core for CRM: numbers, logs, buttons, tenant tokens",
    "license": "LGPL-3",
    "depends": ["base", "crm"],
    "data": [
        "security/ir.model.access.csv",
        "views/telephony_account_views.xml",
        "views/telephony_number_views.xml",
        "views/crm_lead_views.xml",
    ],
    "installable": True,
}
