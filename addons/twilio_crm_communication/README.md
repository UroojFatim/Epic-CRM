# Twilio CRM Communication

Twilio Calls & SMS from CRM Leads for Odoo 17.

## 1) Install Python dependency (`twilio`)

Install in the same Python environment used by Odoo:

```bash
pip install twilio
```

If you use a virtual environment or conda, activate it first, then install.

## 2) Install module in Odoo

1. Place `twilio_crm_communication` in your Odoo addons path.
2. Restart Odoo.
3. Apps → Update Apps List.
4. Search for **Twilio Calls & SMS from CRM Leads** and install.

## 3) Configure Twilio settings

Go to **Settings → Twilio (CRM Calls & SMS)** and set:

- Twilio Account SID
- Twilio Auth Token
- Twilio From Number (E.164, e.g. `+14155552671`)
- Twilio Webhook Base URL (public HTTPS base URL)
- Twilio TwiML App SID (optional)

## 4) Webhook mode

If using webhook mode (without TwiML App SID):

- Set `twilio_webhook_base_url` to a public HTTPS URL reachable by Twilio.
- Ensure these routes are publicly reachable:
  - `GET /twilio/voice/twiml`
  - `POST /twilio/voice/status`
- Allow inbound requests through your reverse proxy/firewall.

## 5) TwiML App mode

If using a TwiML App, set **Twilio TwiML App SID** (`twilio_twiml_app_sid`).
In this mode, outbound calls use `application_sid` instead of TwiML URL generation.

## 6) Troubleshooting

- **Missing configuration**: Fill required Twilio settings (SID, token, from number, webhook base URL).
- **Phone format issues**: Use E.164 format where possible (numbers starting with `+`).
- **Permission denied**: Assign users to `Twilio User` (or `Twilio Admin`) groups.
- **No call/SMS buttons**: Confirm user group and that lead has phone or mobile.
