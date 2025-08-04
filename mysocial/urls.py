from django.urls import path
from . import views



urlpatterns  = [
    path('registration/',views.Registration.as_view(),name='registration/'),
    path('login/',views.loginview.as_view(),name='login/'),
    path('forget/',views.forget_password.as_view(),name='forget/')
]