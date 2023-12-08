"""
URL configuration for projectfinal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from ticketmaster import views
from django.contrib import admin

# Adrian: Created urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('results/', views.post_events, name='ticketmaster-results'),
    path('create/', views.create_bookmark, name='create-bookmark'),
    path('bookmarks/', views.view_bookmarks, name='ticketmaster-bookmarks'),
    path('update/', views.update_bookmark, name='update-bookmark'),
    path('delete/', views.delete_bookmark, name='delete-bookmark'),
    path('register/', views.register_view, name='register-user'),
    path('login/', views.login_view, name='login-user'),
    path('logout/', views.logout_view, name='logout')
]
