from django.urls import path
from django.views.i18n import set_language
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard (home)
    path('dashboard/', views.home, name='home'),
    
    # Sample management
    path('samples/', views.sample_list, name='sample_list'),
    path('samples/<int:pk>/', views.sample_detail, name='sample_detail'),
    path('samples/create/', views.sample_create, name='sample_create'),
    path('samples/<int:pk>/edit/', views.sample_update, name='sample_update'),
    path('samples/<int:pk>/delete/', views.sample_delete, name='sample_delete'),
    
    # Export
    path('samples/export/', views.export_samples, name='export_samples'),
    
    # Site settings
    path('settings/', views.site_settings_view, name='site_settings'),
    
    # Language switching (using Django's built-in view)
    path('i18n/setlang/', set_language, name='set_language'),
]
