# 香港細胞及幹細胞資源中心庫存管理系統
# Inventory Management System of Hong Kong Cell and Stem Cell Resource Center

A comprehensive Django web application for managing stem cell sample inventory with role-based access control, audit trails, and multilingual support.

## Features

### 1. Sample Management
- **Comprehensive Sample Information**: Store detailed information about each stem cell sample including:
  - Basic information (ID, name, type, description)
  - Source and donor information
  - Storage location and status
  - Quantity and passage number
  - Important dates (collection, storage, expiration)
  - Quality control data (viability, QC notes)
  - Sample images (automatically compressed to save storage)
  - Research use restrictions

### 2. Role-Based Access Control
- **Admin (Superuser)**: Highest authorization level
  - Full access to Django admin panel
  - Can manage all samples
  - Can manage users and groups
  - Can edit site settings (logo, site name)
  - Access to all staff features

- **Lab Staff**: Sample management capabilities
  - Add new samples to the bank
  - Edit existing samples
  - Remove samples from the bank
  - View all sample details
  - Search and filter samples
  - Export samples to Excel

### 3. Dashboard
- Real-time statistics overview
- Recently modified samples
- Samples expiring soon alerts
- Low stock warnings
- Quick actions

### 4. Multilingual Support (i18n)
- English
- Traditional Chinese (繁體中文)
- Simplified Chinese (简体中文)
- Easy language switching via dropdown

### 5. Audit Trail
- Complete history tracking for all samples
- View who changed what and when
- Compare changes between versions
- History tab on each sample detail page

### 6. Export Functionality
- Export to Excel (.xlsx)
- Select specific columns to export
- Export filtered or selected samples
- Styled Excel output with headers

### 7. Modern User Interface
- Clean, professional dashboard design
- Responsive sidebar navigation
- Mobile-friendly layout
- Beautiful login page
- Customizable site logo and name

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository** (if from git):
   ```bash
   git clone <repository-url>
   cd StemCellResourceBank_v0
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional but recommended for production):
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-domain.pythonanywhere.com,localhost
   ```

5. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Compile translation files**:
   ```bash
   python manage.py compilemessages
   ```

7. **Set up user groups** (Lab Staff permissions):
   ```bash
   python manage.py setup_groups
   ```

8. **Create demo data** (optional but recommended for testing):
   ```bash
   python manage.py create_demo_data
   ```
   This command creates:
   - Admin user (username: `admin`, password: `admin123`)
   - Lab staff user (username: `labstaff`, password: `staff123`)
   - 6 sample stem cell samples with realistic data

9. **Create a superuser** (if not using demo data):
   ```bash
   python manage.py createsuperuser
   ```

10. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

11. **Access the application**:
    - Login page: http://localhost:8000/
    - Dashboard: http://localhost:8000/dashboard/
    - Samples: http://localhost:8000/samples/
    - Admin panel: http://localhost:8000/admin/
    - Site settings: http://localhost:8000/settings/

## Usage Guide

### For Lab Staff
1. Go to the login page at http://localhost:8000/
2. Log in with your credentials
3. View the dashboard for overview and recent activity
4. Navigate to "Samples" to view all samples
5. Click "Add Sample" to create a new sample
6. Use search and filter tools to find samples
7. Click on a sample to view details and history
8. Use Export button to download samples as Excel

### For Administrators
1. Log in with admin credentials
2. Access all Lab Staff functions plus:
   - Visit "Site Settings" to update logo and site names
   - Access Django admin panel for user management
   - Create and manage user accounts
   - Assign users to Lab Staff group

### Changing Language
- Click the language dropdown in the sidebar (globe icon)
- Select your preferred language:
  - English
  - 繁體中文 (Traditional Chinese)
  - 简体中文 (Simplified Chinese)

## Project Structure

```
StemCellResourceBank_v0/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings (with i18n config)
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── samples/               # Main application
│   ├── management/        # Custom management commands
│   │   └── commands/
│   │       ├── setup_groups.py      # Set up user groups
│   │       └── create_demo_data.py  # Create demo data
│   ├── templates/         # HTML templates
│   │   └── samples/
│   │       ├── base.html              # Base template with sidebar
│   │       ├── login.html             # Login page
│   │       ├── home.html              # Dashboard
│   │       ├── sample_list.html       # Sample list with export
│   │       ├── sample_detail.html     # Sample detail with history
│   │       ├── sample_form.html       # Add/Edit form
│   │       ├── sample_confirm_delete.html
│   │       └── site_settings.html     # Site configuration
│   ├── templatetags/      # Custom template tags
│   │   └── sample_tags.py
│   ├── admin.py           # Admin panel with history
│   ├── context_processors.py  # Site settings context
│   ├── forms.py           # Django forms with validation
│   ├── models.py          # Database models with history
│   ├── urls.py            # App URL configuration
│   └── views.py           # View functions
├── locale/                # Translation files
│   ├── zh_Hant/          # Traditional Chinese
│   └── zh_Hans/          # Simplified Chinese
├── static/                # Static files
├── media/                 # User-uploaded files
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## PythonAnywhere Deployment

### Storage Considerations
- Free tier: 512 MB disk space
- Sample images are automatically compressed (max 500KB each)
- Consider upgrading to Hacker plan ($5/month) for 1GB
- Alternative: Use Cloudinary for media storage (free tier: 25GB)

### Deployment Steps
1. Upload project to PythonAnywhere
2. Create virtual environment and install dependencies
3. Set environment variables in `.env`
4. Configure WSGI file
5. Set up static and media file serving
6. Run migrations and create superuser

## Security & Permissions

### Authentication
- All pages require login (no public access)
- Django's built-in authentication system
- Password hashing and security
- Session-based authentication

### Authorization Levels
1. **Lab Staff Group**: Full CRUD on samples, export capability
2. **Superusers**: Full access including site settings and admin panel

## Customization

### Adding New Sample Types
Edit `samples/models.py`, modify the `SAMPLE_TYPE_CHOICES`:
```python
SAMPLE_TYPE_CHOICES = [
    ('IPSC', _('Induced Pluripotent Stem Cell')),
    # Add your new type here
    ('NEW_TYPE', _('New Type Description')),
]
```

### Updating Translations
1. Edit `.po` files in `locale/zh_Hant/LC_MESSAGES/` and `locale/zh_Hans/LC_MESSAGES/`
2. Run `python manage.py compilemessages`

### Customizing Site Branding
1. Log in as admin
2. Go to Site Settings
3. Upload logo and edit site names for each language

## Dependencies

- Django 4.2 - Web framework
- Pillow - Image processing and compression
- django-simple-history - Audit trail
- openpyxl - Excel export
- python-decouple - Environment variables

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic
```

### Database errors
```bash
python manage.py makemigrations
python manage.py migrate
```

### Translation not working
```bash
python manage.py compilemessages
```

### Permission denied errors
Make sure Lab Staff group is created:
```bash
python manage.py setup_groups
```

## License

This project is created for research and educational purposes.

---

**Version**: 2.0.0  
**Last Updated**: December 2025
