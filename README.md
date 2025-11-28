# Stem Cell Resource Bank

A comprehensive Django web application for managing stem cell samples with role-based access control and public dissemination capabilities.

## Features

### 1. Sample Management
- **Comprehensive Sample Information**: Store detailed information about each stem cell sample including:
  - Basic information (ID, name, type, description)
  - Source and donor information
  - Storage location and status
  - Quantity and passage number
  - Important dates (collection, storage, expiration)
  - Quality control data (viability, QC notes)
  - Sample images
  - Research use restrictions

### 2. Role-Based Access Control
- **Admin (Superuser)**: Highest authorization level
  - Full access to Django admin panel
  - Can manage all samples
  - Can manage users and groups
  - Access to all staff features

- **Lab Staff**: Sample management capabilities
  - Add new samples to the bank
  - Edit existing samples
  - Remove samples from the bank
  - View all sample details
  - Search and filter samples

- **Public (Unauthenticated)**: Read-only access
  - Browse all samples
  - View sample details
  - Search and filter samples
  - No edit or delete capabilities

### 3. Modern User Interface
- Beautiful, responsive design using Bootstrap 5
- Gradient color schemes and smooth animations
- Intuitive navigation and user experience
- Mobile-friendly responsive layout
- Advanced search and filtering capabilities
- Visual status badges and indicators

### 4. Additional Features
- Image upload for samples
- Advanced search functionality
- Filter by sample type and status
- Automatic timestamp tracking
- User activity tracking (who created samples)
- Quality control progress visualization

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

4. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Set up user groups** (Lab Staff permissions):
   ```bash
   python manage.py setup_groups
   ```

6. **Create demo data** (optional but recommended for testing):
   ```bash
   python manage.py create_demo_data
   ```
   This command creates:
   - Admin user (username: `admin`, password: `admin123`)
   - Lab staff user (username: `labstaff`, password: `staff123`)
   - 6 sample stem cell samples with realistic data

7. **Create a superuser** (if not using demo data):
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the application**:
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/
   - Public samples: http://localhost:8000/public/
   - Sample management: http://localhost:8000/samples/ (requires login)

## Usage Guide

### For Public Users
1. Visit the homepage at http://localhost:8000/
2. Click "Browse Samples" to view all available samples
3. Use search and filters to find specific samples
4. Click on any sample to view detailed information
5. No login required for browsing

### For Lab Staff
1. Click "Staff Login" in the navigation menu
2. Log in with your lab staff credentials
3. Navigate to "Manage Samples" to view all samples
4. Click "Add New Sample" to add a new sample
5. Use the search and filter tools to find samples
6. Click on a sample to view full details
7. Use Edit/Delete buttons to modify or remove samples

### For Administrators
1. Log in at http://localhost:8000/admin/ with admin credentials
2. Access the full Django admin interface
3. Manage users, groups, and permissions
4. Perform all lab staff functions plus:
   - Create and manage user accounts
   - Assign users to Lab Staff group
   - Configure system settings
   - Bulk operations on samples

## Project Structure

```
StemCellResourceBank_v0/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings file
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── samples/               # Main application
│   ├── management/        # Custom management commands
│   │   └── commands/
│   │       ├── setup_groups.py      # Set up user groups
│   │       └── create_demo_data.py  # Create demo data
│   ├── templates/         # HTML templates
│   │   └── samples/
│   │       ├── base.html             # Base template
│   │       ├── home.html             # Homepage
│   │       ├── login.html            # Login page
│   │       ├── public_list.html      # Public sample list
│   │       ├── public_detail.html    # Public sample detail
│   │       ├── sample_list.html      # Staff sample list
│   │       ├── sample_detail.html    # Staff sample detail
│   │       ├── sample_form.html      # Add/Edit form
│   │       └── sample_confirm_delete.html  # Delete confirmation
│   ├── admin.py           # Admin panel configuration
│   ├── forms.py           # Django forms
│   ├── models.py          # Database models
│   ├── urls.py            # App URL configuration
│   └── views.py           # View functions
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded files
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## Database Models

### Sample Model
The main model storing stem cell sample information with the following fields:

**Basic Information:**
- `sample_id`: Unique identifier (e.g., IPSC-2024-001)
- `name`: Sample name
- `sample_type`: Type of stem cell (iPSC, ESC, MSC, HSC, NSC, Other)
- `description`: Detailed description

**Source & Storage:**
- `source`: Source institution or lab
- `donor_info`: Donor information and consent details
- `storage_location`: Physical storage location

**Status & Quantity:**
- `status`: Current status (Available, In Use, Depleted, Reserved, Quarantine)
- `quantity`: Number of vials
- `passage_number`: Cell passage number

**Dates:**
- `collection_date`: When sample was collected
- `storage_date`: When sample was stored
- `expiration_date`: Sample expiration date

**Quality Control:**
- `viability`: Cell viability percentage
- `quality_control_notes`: QC test results and notes

**Additional:**
- `research_use_only`: Boolean flag
- `image`: Sample image
- `created_by`: User who created the record
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Security & Permissions

### Authentication
- Django's built-in authentication system
- Password hashing and security
- Session-based authentication

### Authorization Levels
1. **Anonymous Users**: Read-only public access
2. **Lab Staff Group**: Full CRUD operations on samples
3. **Superusers**: Full system access including admin panel

### Permission Checks
- View decorators enforce authentication
- `@login_required` for staff-only pages
- `@user_passes_test` for permission verification
- Public views accessible without authentication

## Customization

### Adding New Sample Types
Edit `samples/models.py`, modify the `SAMPLE_TYPE_CHOICES`:
```python
SAMPLE_TYPE_CHOICES = [
    ('IPSC', 'Induced Pluripotent Stem Cell'),
    ('ESC', 'Embryonic Stem Cell'),
    # Add your new type here
    ('NEW_TYPE', 'New Type Description'),
]
```

### Changing Status Options
Edit `samples/models.py`, modify the `STATUS_CHOICES`:
```python
STATUS_CHOICES = [
    ('AVAILABLE', 'Available'),
    # Add your new status here
    ('NEW_STATUS', 'New Status'),
]
```

### Customizing the UI
- Edit templates in `samples/templates/samples/`
- Modify CSS in `samples/templates/samples/base.html` (inline styles)
- Add custom CSS files in `static/css/`

## Management Commands

### Setup Groups
```bash
python manage.py setup_groups
```
Creates the Lab Staff group with appropriate permissions.

### Create Demo Data
```bash
python manage.py create_demo_data
```
Populates the database with:
- Sample users (admin and lab staff)
- Sample stem cell records

## Deployment Considerations

For production deployment, remember to:

1. **Change SECRET_KEY** in `config/settings.py`
2. **Set DEBUG = False** in `config/settings.py`
3. **Configure ALLOWED_HOSTS** appropriately
4. **Use a production database** (PostgreSQL, MySQL)
5. **Collect static files**: `python manage.py collectstatic`
6. **Use a proper web server** (Gunicorn, uWSGI with Nginx)
7. **Set up HTTPS/SSL** certificates
8. **Configure media file serving**
9. **Set up proper backup procedures**
10. **Review security settings** using `python manage.py check --deploy`

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

### Permission denied errors
Make sure Lab Staff group is created:
```bash
python manage.py setup_groups
```

### Cannot login
Reset user password:
```bash
python manage.py changepassword username
```

## Support & Contributing

For issues, questions, or contributions, please refer to the project's issue tracker or contact the development team.

## License

This project is created for research and educational purposes.

## Acknowledgments

Built with:
- Django 4.2 - Web framework
- Bootstrap 5 - UI framework
- Bootstrap Icons - Icon library
- SQLite - Database (development)

---

**Version**: 1.0.0  
**Last Updated**: November 2024

