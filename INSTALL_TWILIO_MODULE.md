# Module Installation Guide - Twilio CRM Communication

## Issue: Module not appearing in Apps

Your module appears to be correctly structured but not showing in the Apps list. Here's how to fix it:

## Step 1: Verify the module is in the correct path

The module should be in:
```
E:\Projects\Aitek Solutions\Epic-CRM\addons\twilio_crm_communication\
```

Check your `odoo.conf` addons_path includes `addons` (which it does):
```
addons_path = addons,odoo/addons,addons/server_brand
```

## Step 2: Update the Apps List

Run this command in PowerShell from your project root:

```powershell
(C:\Users\Hp\anaconda3\shell\condabin\conda-hook.ps1)
conda activate crm
python odoo-bin -c odoo.conf -d epiccrm --stop-after-init
```

This will scan for new modules and update the database.

## Step 3: Install the module via Odoo UI

1. Start Odoo normally:
   ```powershell
   (C:\Users\Hp\anaconda3\shell\condabin\conda-hook.ps1)
   conda activate crm
   python odoo-bin -c odoo.conf
   ```

2. Login to Odoo (http://localhost:8069 or your configured port)

3. Go to **Apps** menu

4. Click **Update Apps List** button (the circular arrow icon)
   - This is CRITICAL - Odoo only scans for new modules when you click this

5. Remove any filters (click the X on filter chips)

6. Search for "Twilio" or "twilio_crm_communication"

7. Click **Install**

## Step 4: If module still doesn't appear

### Option A: Install via command line

```powershell
(C:\Users\Hp\anaconda3\shell\condabin\conda-hook.ps1)
conda activate crm
python odoo-bin -c odoo.conf -d epiccrm -i twilio_crm_communication --stop-after-init
```

### Option B: Check for errors

Look at the Odoo logs when starting:

```powershell
(C:\Users\Hp\anaconda3\shell\condabin\conda-hook.ps1)
conda activate crm
python odoo-bin -c odoo.conf -d epiccrm --log-level=debug 2>&1 | Tee-Object -FilePath odoo_debug.log
```

Then search odoo_debug.log for "twilio" to see any errors.

### Option C: Verify module in database

The module might be installed but in wrong state. Check with:

```powershell
(C:\Users\Hp\anaconda3\shell\condabin\conda-hook.ps1)
conda activate crm
python odoo-bin shell -c odoo.conf -d epiccrm
```

Then in the shell:
```python
module = env['ir.module.module'].search([('name', '=', 'twilio_crm_communication')])
print(f"State: {module.state if module else 'NOT FOUND'}")
# If found but in wrong state, try:
if module and module.state == 'uninstalled':
    module.button_immediate_install()
```

## Step 5: Common Issues

### Module shows "uninstallable"
- Check the __manifest__.py has `'installable': True` ✓ (already set)
- Check all dependencies are installed: base, crm, mail, contacts ✓

### Module not in list at all
- Did you click "Update Apps List"? This is required!
- Check file permissions - all files should be readable
- Restart Odoo after updating manifest

### Errors during installation
- Check Python syntax in all .py files
- Check XML syntax in all view files  
- Check CSV files don't have errors
- Look at the error in odoo logs

## Quick Verification Checklist

✓ __manifest__.py exists and has correct structure
✓ __init__.py exists in root and all subdirectories
✓ All data files listed in manifest exist
✓ Module is in addons_path
✓ Clicked "Update Apps List" in Odoo UI
✓ No Python/XML syntax errors

## Still having issues?

Share the output of:
```powershell
(C:\Users\Hp\anaconda3\shell\condabin\conda-hook.ps1)
conda activate crm
python odoo-bin -c odoo.conf -d epiccrm -i twilio_crm_communication --stop-after-init --log-level=info
```
