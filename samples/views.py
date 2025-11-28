from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .models import Sample
from .forms import SampleForm


# Permission checking functions
def is_staff_or_admin(user):
    """Check if user is staff member or admin"""
    return user.is_authenticated and (user.groups.filter(name='Lab Staff').exists() or user.is_superuser)


def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and user.is_superuser


# Public views
def home(request):
    """Home page - accessible to everyone"""
    recent_samples = Sample.objects.filter(status='AVAILABLE')[:6]
    context = {
        'recent_samples': recent_samples,
        'total_samples': Sample.objects.count(),
        'available_samples': Sample.objects.filter(status='AVAILABLE').count(),
    }
    return render(request, 'samples/home.html', context)


def public_sample_list(request):
    """Public read-only view of all available samples"""
    samples = Sample.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        samples = samples.filter(
            Q(sample_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(sample_type__icontains=search_query)
        )
    
    # Filter by type
    sample_type = request.GET.get('type', '')
    if sample_type:
        samples = samples.filter(sample_type=sample_type)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        samples = samples.filter(status=status)
    
    context = {
        'samples': samples,
        'search_query': search_query,
        'selected_type': sample_type,
        'selected_status': status,
        'sample_types': Sample.SAMPLE_TYPE_CHOICES,
        'status_choices': Sample.STATUS_CHOICES,
    }
    return render(request, 'samples/public_list.html', context)


def public_sample_detail(request, pk):
    """Public read-only view of a single sample"""
    sample = get_object_or_404(Sample, pk=pk)
    return render(request, 'samples/public_detail.html', {'sample': sample})


# Authentication views
def login_view(request):
    """Login view"""
    if request.user.is_authenticated:
        return redirect('sample_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'sample_list')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'samples/login.html', {'form': form})


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


# Staff and Admin views - require authentication and permissions
@login_required
@user_passes_test(is_staff_or_admin, login_url='login')
def sample_list(request):
    """List all samples - for lab staff and admins"""
    samples = Sample.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        samples = samples.filter(
            Q(sample_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(sample_type__icontains=search_query) |
            Q(storage_location__icontains=search_query)
        )
    
    # Filter by type
    sample_type = request.GET.get('type', '')
    if sample_type:
        samples = samples.filter(sample_type=sample_type)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        samples = samples.filter(status=status)
    
    context = {
        'samples': samples,
        'search_query': search_query,
        'selected_type': sample_type,
        'selected_status': status,
        'sample_types': Sample.SAMPLE_TYPE_CHOICES,
        'status_choices': Sample.STATUS_CHOICES,
    }
    return render(request, 'samples/sample_list.html', context)


@login_required
@user_passes_test(is_staff_or_admin, login_url='login')
def sample_detail(request, pk):
    """View sample details - for lab staff and admins"""
    sample = get_object_or_404(Sample, pk=pk)
    return render(request, 'samples/sample_detail.html', {'sample': sample})


@login_required
@user_passes_test(is_staff_or_admin, login_url='login')
def sample_create(request):
    """Create a new sample - for lab staff and admins"""
    if request.method == 'POST':
        form = SampleForm(request.POST, request.FILES)
        if form.is_valid():
            sample = form.save(commit=False)
            sample.created_by = request.user
            sample.save()
            messages.success(request, f'Sample {sample.sample_id} created successfully!')
            return redirect('sample_detail', pk=sample.pk)
    else:
        form = SampleForm()
    
    return render(request, 'samples/sample_form.html', {
        'form': form,
        'title': 'Add New Sample',
        'button_text': 'Create Sample'
    })


@login_required
@user_passes_test(is_staff_or_admin, login_url='login')
def sample_update(request, pk):
    """Update an existing sample - for lab staff and admins"""
    sample = get_object_or_404(Sample, pk=pk)
    
    if request.method == 'POST':
        form = SampleForm(request.POST, request.FILES, instance=sample)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sample {sample.sample_id} updated successfully!')
            return redirect('sample_detail', pk=sample.pk)
    else:
        form = SampleForm(instance=sample)
    
    return render(request, 'samples/sample_form.html', {
        'form': form,
        'sample': sample,
        'title': f'Edit Sample: {sample.sample_id}',
        'button_text': 'Update Sample'
    })


@login_required
@user_passes_test(is_staff_or_admin, login_url='login')
def sample_delete(request, pk):
    """Delete a sample - for lab staff and admins"""
    sample = get_object_or_404(Sample, pk=pk)
    
    if request.method == 'POST':
        sample_id = sample.sample_id
        sample.delete()
        messages.success(request, f'Sample {sample_id} deleted successfully!')
        return redirect('sample_list')
    
    return render(request, 'samples/sample_confirm_delete.html', {'sample': sample})
