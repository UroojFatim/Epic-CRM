#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to assign Twilio Admin group to an Odoo user
"""
import getpass
import xmlrpc.client

# Connection parameters
HOST = 'localhost'
PORT = 8069
DB = 'epiccrm'

def assign_twilio_admin():
    print("=" * 60)
    print("Assign Twilio Admin Group to User")
    print("=" * 60)
    
    # Get credentials
    username = input("Enter your Odoo username (email): ").strip()
    password = getpass.getpass("Enter your password: ").strip()
    
    if not username or not password:
        print("\nERROR: Username and password are required!")
        return
    
    try:
        print("\nConnecting to Odoo...")
        url = f"http://{HOST}:{PORT}"
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        
        print(f"Logging in as '{username}'...")
        uid = common.authenticate(DB, username, password, {})
        if not uid:
            print("\nERROR: Authentication failed. Check username/password.")
            return
        
        print("Logged in successfully!")
        
        # Get current user
        current_user = models.execute_kw(
            DB,
            uid,
            password,
            'res.users',
            'read',
            [[uid]],
            {'fields': ['name', 'groups_id']},
        )[0]
        print(f"\nCurrent user: {current_user['name']} (ID: {uid})")

        # Find Twilio Admin group by XML ID via public model methods
        xmlid_records = models.execute_kw(
            DB,
            uid,
            password,
            'ir.model.data',
            'search_read',
            [[
                ('module', '=', 'twilio_crm_communication'),
                ('name', '=', 'group_twilio_admin'),
                ('model', '=', 'res.groups'),
            ]],
            {'fields': ['res_id'], 'limit': 1},
        )
        group_id = xmlid_records[0]['res_id'] if xmlid_records else False

        if not group_id:
            print("\nERROR: Twilio Admin group not found!")
            print("Make sure the module is installed properly.")
            return

        print(f"Found Twilio Admin group (ID: {group_id})")

        # Check if user already has the group
        if group_id in current_user['groups_id']:
            print("\nUser already has Twilio Admin permission!")
        else:
            print("\nAssigning Twilio Admin group to user...")
            models.execute_kw(
                DB,
                uid,
                password,
                'res.users',
                'write',
                [[uid], {'groups_id': [(4, group_id)]}],
            )
            print("SUCCESS: Twilio Admin group assigned!")
        
        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Refresh your browser (F5)")
        print("2. Go to Settings")
        print("3. Look for 'Twilio (CRM Calls & SMS)' section")
        print("4. Configure your Twilio credentials")
        print("5. Go to CRM > Configuration > Twilio to see menus")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nMake sure:")
        print("- Odoo server is running")
        print("- Username and password are correct")
        print("- Database name in this script matches your database")

if __name__ == '__main__':
    assign_twilio_admin()
