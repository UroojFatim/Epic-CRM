# -*- coding: utf-8 -*-
import logging
import requests
from urllib.parse import urljoin
from odoo import models, api

_logger = logging.getLogger(__name__)

TWILIO_SMS_API = "https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
TWILIO_CALL_API = "https://api.twilio.com/2010-04-01/Accounts/{sid}/Calls.json"

class TwilioProvider(models.AbstractModel):
    _name = "twilio.provider"
    _description = "Twilio Provider Service"

    @api.model
    def _status_urls(self, account):
        base = account.public_base_url.rstrip("/") + "/t/%s/" % account.tenant_token
        return {
            "sms_status": urljoin(base, "twilio/sms/status"),
            "voice_status": urljoin(base, "twilio/voice/status"),
            "voice_inbound": urljoin(base, "twilio/voice/inbound"),
        }

    @api.model
    def send_sms(self, account, to, body, lead=None):
        account._ensure_ready()
        if account.dry_run:
            self.env["telephony.message"].sudo().create({
                "account_id": account.id, "lead_id": lead.id if lead else False,
                "direction": "out", "frm": account.default_sms_from, "to": to,
                "body": body, "provider": "twilio", "status": "DRY-RUN"
            })
            return "DRY-RUN"
        url = TWILIO_SMS_API.format(sid=account.account_sid)
        status_urls = self._status_urls(account)
        data = {
            "To": to,
            "From": account.default_sms_from,
            "Body": body,
            "StatusCallback": status_urls["sms_status"],
        }
        resp = requests.post(url, data=data, auth=(account.account_sid, account.auth_token), timeout=20)
        resp.raise_for_status()
        j = resp.json()
        self.env["telephony.message"].sudo().create({
            "account_id": account.id,
            "lead_id": lead.id if lead else False,
            "direction": "out",
            "frm": account.default_sms_from,
            "to": to,
            "body": body,
            "provider": "twilio",
            "provider_sid": j.get("sid"),
            "status": j.get("status"),
            "price": float(j.get("price", 0) or 0),
            "price_unit": j.get("price_unit") or "USD",
        })
        return j.get("status") or "queued"

    @api.model
    def start_call(self, account, to, lead=None, use_bot=False):
        account._ensure_ready()
        status_urls = self._status_urls(account)
        if account.dry_run:
            self.env["telephony.call"].sudo().create({
                "account_id": account.id, "lead_id": lead.id if lead else False,
                "direction": "out", "frm": account.default_voice_from, "to": to,
                "provider": "twilio", "status": "DRY-RUN"
            })
            return "DRY-RUN"
        # If use_bot, Twilio fetches TwiML from our inbound endpoint and we return bot flow
        voice_url = status_urls["voice_inbound"]
        if not use_bot:
            # add a query flag so the controller knows to skip bot
            voice_url = voice_url + "?human=1"
        data = {
            "To": to,
            "From": account.default_voice_from,
            "Url": voice_url,
            "StatusCallback": status_urls["voice_status"],
            "StatusCallbackEvent": "initiated ringing answered completed",
        }
        url = TWILIO_CALL_API.format(sid=account.account_sid)
        resp = requests.post(url, data=data, auth=(account.account_sid, account.auth_token), timeout=20)
        resp.raise_for_status()
        j = resp.json()
        self.env["telephony.call"].sudo().create({
            "account_id": account.id,
            "lead_id": lead.id if lead else False,
            "direction": "out",
            "frm": account.default_voice_from,
            "to": to,
            "provider": "twilio",
            "provider_sid": j.get("sid"),
            "status": j.get("status"),
        })
        return j.get("status") or "queued"
