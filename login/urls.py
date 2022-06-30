from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views
from .views import CustomLoginView, RegisterPage

urlpatterns=[
    path('',CustomLoginView.as_view(), name='login'),
    path('logout',LogoutView.as_view(next_page='login'), name='logout'),
    path('register',RegisterPage.as_view(),name="register")
    
]