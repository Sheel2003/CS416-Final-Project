from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_events),
    path('', include('ticketmaster.urls')),
    path('register/', views.register_view, name='register'),
]
