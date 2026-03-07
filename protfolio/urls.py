# file path: protfolio/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Main pages
    path('', views.home, name='home'),
    path('services/', views.services_page, name='services'),
    path('blog/', views.blog_page, name='blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('about-us/', views.about_us_page, name='about_us'),
    path('reviews/', views.review_page, name='review_page'),
    path('reviews/submit/', views.submit_review, name='submit_review'),

    # Service CRUD
    path('services/new/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_update, name='service_update'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),

    # Blog Post CRUD
    path('blog/new/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/edit/', views.blog_update, name='blog_update'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),

    # Developer CRUD
    path('developer/new/', views.developer_create, name='developer_create'),
    path('developer/<int:pk>/edit/', views.developer_update, name='developer_update'),
    path('developer/<int:pk>/delete/', views.developer_delete, name='developer_delete'),

    # Client CRUD
    path('client/new/', views.client_create, name='client_create'),
    path('client/<int:pk>/edit/', views.client_update, name='client_update'),
    path('client/<int:pk>/delete/', views.client_delete, name='client_delete'),

    # Superadmin Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/users/', views.user_management, name='user_management'),

    path('contact/', views.contact, name='contact'),
]