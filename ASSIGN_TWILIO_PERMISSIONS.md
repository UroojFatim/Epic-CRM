# How to Assign Twilio Permissions

## The Problem
The Twilio menus and settings are only visible to users with the "Twilio Admin" group.
You need to grant yourself this permission.

## Solution 1: Via UI (Easiest)

1. **Login to Odoo** as an administrator user
2. **Go to Settings** (⚙️ icon in top menu)
3. **Click "Users & Companies" → Users**
4. **Find and click your user** (the one you're logged in as)
5. **Click "Edit"**
6. **Scroll down to "Access Rights" tab**
7. **Look for the "CRM" section**
8. **Find "Twilio CRM Communication"** field
9. **Set it to "Twilio Admin"** (dropdown)
10. **Click "Save"**
11. **Refresh your browser** (F5)
12. **Go to Settings** → You should now see "Twilio (CRM Calls & SMS)" section!

## Solution 2: Via Command Line (Faster)

Run this script to automatically assign Twilio Admin to the main admin user:

```powershell
conda activate crm
python assign_twilio_admin.py
```

The script will ask for your username and assign the Twilio Admin group.

## Solution 3: Manual Database Assignment

If you know your user ID, you can directly add the group in the Odoo shell.

## After Assigning Permissions

Once you have the Twilio Admin role:
- ✅ Settings will show "Twilio (CRM Calls & SMS)" section
- ✅ CRM menu will show "Configuration → Twilio" submenu
- ✅ You can configure Twilio credentials
- ✅ Call/SMS buttons will appear on CRM leads

## Security Levels

**Twilio User**: Can use Call/SMS buttons, create logs
**Twilio Admin**: All of the above + configure settings + view all logs

For testing, use Twilio Admin. For regular users, assign Twilio User.
