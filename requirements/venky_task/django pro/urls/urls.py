"""HotelRoomBooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from hrb import views
admin.site.site_header = "HARI HOTEL Admin"
admin.site.site_title = "HARI Admin Portal"
admin.site.index_title = "Welcome to HARI HOTEL"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^signup/', views.signup_view),
    url(r'^logout123/', views.logout_view),
    url(r'^userhome/', views.userhome),
    url(r'^bookroom', views.bookroom_view),
    url(r'^login/', views.login),
    url('accounts/', include('django.contrib.auth.urls')),
]
