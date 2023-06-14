from django.contrib import admin
from django.urls import path, include
from projectsyte import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.Login.as_view, name="login"),
    path('create_post/', views.create_post, name='create_post'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)