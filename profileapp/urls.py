from django.urls import path
from . import views



urlpatterns  = [ 
    path('upload_profile',views.uplaod_profile.as_view(),name='upload_profile'),
    path('update_profile',views.update_profile.as_view(),name='update_profile')
 
]