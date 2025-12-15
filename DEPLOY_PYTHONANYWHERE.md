# PythonAnywhere Deployment Guide

This guide explains how to deploy and update the Stem Cell Resource Bank on PythonAnywhere.

## Initial Deployment (First Time Only)

### Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com/
2. Sign up for a free account (or paid if you need more resources)

### Step 2: Upload Your Code

**Option A: Using Git (Recommended)**
1. Open a Bash console from your PythonAnywhere dashboard
2. Clone your repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/StemCellResourceBank_v0.git
   ```

**Option B: Upload ZIP file**
1. Zip your project folder (excluding `venv/` folder)
2. Upload via Files tab on PythonAnywhere
3. Open Bash console and unzip:
   ```bash
   unzip StemCellResourceBank_v0.zip
   ```

### Step 3: Create Virtual Environment
```bash
cd StemCellResourceBank_v0
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in your project root:
```bash
nano .env
```

Add these lines:
```
SECRET_KEY=your-super-secret-key-generate-a-random-one
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com,localhost
```

Generate a secret key with:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Initialize Database
```bash
python manage.py migrate
python manage.py setup_groups
python manage.py compilemessages
python manage.py createsuperuser
```

### Step 6: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 7: Configure Web App
1. Go to **Web** tab on PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (NOT Django)
4. Select Python 3.9

### Step 8: Configure WSGI File
Click on the WSGI configuration file link and replace its contents with:

```python
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/StemCellResourceBank_v0'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable to tell Django where settings are
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Load environment variables from .env file
from pathlib import Path
from dotenv import load_dotenv
env_path = Path(project_home) / '.env'
load_dotenv(dotenv_path=env_path)

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv', 'bin', 'activate_this.py')
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Note:** Replace `YOUR_USERNAME` with your actual PythonAnywhere username.

### Step 9: Configure Virtual Environment Path
In the Web tab, set the **Virtualenv** path to:
```
/home/YOUR_USERNAME/StemCellResourceBank_v0/venv
```

### Step 10: Configure Static Files
In the Web tab, under **Static files**, add:

| URL | Directory |
|-----|-----------|
| /static/ | /home/YOUR_USERNAME/StemCellResourceBank_v0/staticfiles |
| /media/ | /home/YOUR_USERNAME/StemCellResourceBank_v0/media |

### Step 11: Reload Web App
Click the **Reload** button on the Web tab.

Your site should now be live at: `https://YOUR_USERNAME.pythonanywhere.com/`

---

## Updating Your Deployment

When you make changes to your code and want to update the live site:

### Method 1: Using Git (Recommended)

1. **Push changes to GitHub** (from your local machine):
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```

2. **Open Bash console on PythonAnywhere**:
   ```bash
   cd StemCellResourceBank_v0
   source venv/bin/activate
   git pull
   ```

3. **Apply any database changes** (if models changed):
   ```bash
   python manage.py migrate
   ```

4. **Update translations** (if translation files changed):
   ```bash
   python manage.py compilemessages
   ```

5. **Collect static files** (if CSS/JS changed):
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Reload the web app**:
   - Go to Web tab → Click **Reload**
   - Or use the API:
   ```bash
   touch /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py
   ```

### Method 2: Manual File Upload

1. Upload changed files via the **Files** tab
2. Open Bash console
3. Run necessary commands (migrate, collectstatic, etc.)
4. Reload web app

---

## Quick Update Script

Create a file called `update.sh` in your project root:

```bash
#!/bin/bash
cd /home/YOUR_USERNAME/StemCellResourceBank_v0
source venv/bin/activate

echo "Pulling latest changes..."
git pull

echo "Installing any new dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Compiling translations..."
python manage.py compilemessages

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Reloading web app..."
touch /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py

echo "Done! Your site has been updated."
```

Make it executable:
```bash
chmod +x update.sh
```

Then just run `./update.sh` whenever you need to update.

---

## Common Issues & Solutions

### "ModuleNotFoundError: No module named 'xxx'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "OperationalError: no such table"
```bash
python manage.py migrate
```

### Static files not loading
1. Make sure you ran `python manage.py collectstatic`
2. Check the static file paths in Web tab
3. Hard refresh your browser (Ctrl+Shift+R)

### Translation not working
```bash
python manage.py compilemessages
```
Then reload the web app.

### Changes not showing
1. Clear browser cache
2. Make sure you clicked **Reload** in the Web tab
3. Check error logs in Web tab

### "DisallowedHost" error
Add your domain to `.env`:
```
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com,localhost
```

---

## Storage Management (Free Tier: 512MB)

### Check current usage:
Look at the **Files** tab - it shows your disk usage.

### Tips to save space:
1. Images are automatically compressed (max 500KB each)
2. Delete old log files:
   ```bash
   rm -rf /home/YOUR_USERNAME/.local/share/pip/log/*
   ```
3. Clear pip cache:
   ```bash
   pip cache purge
   ```
4. Remove `.pyc` files:
   ```bash
   find . -name "*.pyc" -delete
   find . -name "__pycache__" -type d -delete
   ```

### When to upgrade:
- If you have many sample images
- If database grows significantly
- Consider Hacker plan ($5/month) for 1GB

---

## Troubleshooting Logs

View error logs in the **Web** tab:
- **Error log**: Shows Python errors
- **Access log**: Shows HTTP requests
- **Server log**: Shows server-level issues

---

## Security Checklist

Before going live, ensure:
- [ ] `DEBUG=False` in `.env`
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` set correctly
- [ ] Changed default admin password
- [ ] HTTPS is enabled (automatic on PythonAnywhere)

