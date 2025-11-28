from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('public/', views.public_sample_list, name='public_sample_list'),
    path('public/<int:pk>/', views.public_sample_detail, name='public_sample_detail'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Staff/Admin views
    path('samples/', views.sample_list, name='sample_list'),
    path('samples/<int:pk>/', views.sample_detail, name='sample_detail'),
    path('samples/create/', views.sample_create, name='sample_create'),
    path('samples/<int:pk>/edit/', views.sample_update, name='sample_update'),
    path('samples/<int:pk>/delete/', views.sample_delete, name='sample_delete'),
]

