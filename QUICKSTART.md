# Quick Start Guide

## Your Application is Ready! 🎉

The Django Stem Cell Resource Bank application has been successfully built and configured.

## What's Been Created

✅ **Complete Django Application** with:
- Sample management system
- User authentication and authorization
- Modern, responsive UI with Bootstrap 5
- Role-based access control (Admin, Lab Staff, Public)
- Public read-only view for dissemination
- Image upload capability
- Advanced search and filtering

✅ **Pre-configured with**:
- Database migrations applied
- User groups set up (Lab Staff)
- Demo data created (6 sample records)
- 2 test users created

## Access the Application

The development server is running at: **http://localhost:8000/**

### Available Pages

1. **Homepage**: http://localhost:8000/
   - Overview and statistics
   - Recent samples
   - Call-to-action buttons

2. **Public Sample Browser**: http://localhost:8000/public/
   - Read-only access for everyone
   - Search and filter samples
   - View sample details

3. **Staff Sample Management**: http://localhost:8000/samples/
   - Requires login
   - Full CRUD operations
   - Add/Edit/Delete samples

4. **Admin Panel**: http://localhost:8000/admin/
   - Requires superuser login
   - Full system administration

5. **Staff Login**: http://localhost:8000/login/
   - For lab staff and admin access

## Test Accounts

### Admin Account (Highest Authorization)
- **Username**: `admin`
- **Password**: `admin123`
- **Capabilities**: Full access to everything, including admin panel

### Lab Staff Account
- **Username**: `labstaff`
- **Password**: `staff123`
- **Capabilities**: Add, edit, and delete samples

### Public Access
- **No login required**
- **Capabilities**: View all samples (read-only)

## Demo Data

6 sample stem cell records have been created:
1. **IPSC-2024-001**: Human iPSC Line - Patient A
2. **ESC-2024-002**: Human Embryonic Stem Cell H9
3. **MSC-2024-003**: Bone Marrow MSC
4. **HSC-2024-004**: Cord Blood Hematopoietic Stem Cells
5. **NSC-2024-005**: Neural Stem Cells
6. **IPSC-2024-006**: Disease-specific iPSC - Parkinson's

## Quick Testing Guide

### Test as Public User (No Login)
1. Go to http://localhost:8000/
2. Click "Browse Samples" or "Public View"
3. Search, filter, and view samples
4. Try to access staff features - you'll be redirected to login

### Test as Lab Staff
1. Go to http://localhost:8000/login/
2. Login with `labstaff` / `staff123`
3. Click "Manage Samples"
4. Try adding a new sample
5. Edit an existing sample
6. View sample details

### Test as Admin
1. Go to http://localhost:8000/admin/
2. Login with `admin` / `admin123`
3. Explore the admin interface
4. View users, groups, and samples
5. Access staff features from the main site

## Key Features to Test

### 1. Sample Management (Lab Staff/Admin)
- ✅ Add new samples with comprehensive information
- ✅ Edit existing samples
- ✅ Delete samples with confirmation
- ✅ Upload sample images
- ✅ Track quality control data

### 2. Search & Filter
- ✅ Search by ID, name, description, type
- ✅ Filter by sample type (iPSC, ESC, MSC, etc.)
- ✅ Filter by status (Available, In Use, etc.)

### 3. Public View
- ✅ Browse all samples without login
- ✅ View detailed sample information
- ✅ Search and filter capabilities
- ✅ No edit/delete buttons (read-only)

### 4. User Interface
- ✅ Modern, gradient-based design
- ✅ Responsive (works on mobile, tablet, desktop)
- ✅ Smooth animations and transitions
- ✅ Intuitive navigation
- ✅ Status badges with color coding
- ✅ Visual progress bars for viability

## Common Tasks

### Add a New Sample
1. Login as staff or admin
2. Go to "Manage Samples"
3. Click "Add New Sample"
4. Fill in required fields (marked with *)
5. Optionally upload an image
6. Click "Create Sample"

### Search for Samples
1. Go to Public View or Manage Samples
2. Use the search box to enter keywords
3. Or use the filter dropdowns
4. Click "Apply Filters"

### Edit a Sample
1. Login as staff or admin
2. Find the sample in "Manage Samples"
3. Click the edit (pencil) icon or view details
4. Click "Edit Sample"
5. Modify fields
6. Click "Update Sample"

### Delete a Sample
1. Login as staff or admin
2. Find the sample in "Manage Samples"
3. Click the delete (trash) icon
4. Confirm deletion

## File Structure Overview

```
StemCellResourceBank_v0/
├── config/              # Django settings
├── samples/             # Main app
│   ├── templates/       # HTML templates
│   ├── management/      # Custom commands
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   └── forms.py         # Forms
├── static/              # CSS, JS, images
├── media/               # Uploaded files
├── db.sqlite3           # Database
├── requirements.txt     # Dependencies
├── README.md           # Full documentation
└── manage.py           # Django CLI
```

## Next Steps

1. **Explore the Application**
   - Try all features with different user roles
   - Add your own samples
   - Upload images

2. **Customize**
   - Edit templates in `samples/templates/`
   - Modify styles in `base.html`
   - Add new fields to the Sample model

3. **Production Deployment**
   - See README.md for deployment checklist
   - Change SECRET_KEY
   - Set DEBUG = False
   - Configure proper database
   - Set up web server (Gunicorn + Nginx)

4. **Create Real Users**
   ```bash
   python manage.py createsuperuser
   ```
   Then use admin panel to create staff users

## Troubleshooting

### Server Not Running?
```bash
cd /Users/huaisong/Documents/GitHub/StemCellResourceBank_v0
source venv/bin/activate
python manage.py runserver
```

### Forgot Password?
```bash
python manage.py changepassword username
```

### Need to Reset Database?
```bash
rm db.sqlite3
python manage.py migrate
python manage.py setup_groups
python manage.py create_demo_data
```

## Support

For detailed documentation, see `README.md`

## Enjoy Your Application! 🚀

You now have a fully functional stem cell resource bank management system with:
- ✅ Beautiful, modern UI
- ✅ Role-based access control
- ✅ Public dissemination capabilities
- ✅ Comprehensive sample tracking
- ✅ Search and filter functionality
- ✅ Image upload support

Happy coding!

