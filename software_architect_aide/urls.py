"""software_architect_aide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [path('admin/', admin.site.urls), path('', views.sign_in, name='sign_in'),
               path('sign_out/', views.sign_out, name='sign_out'),
               path('dashboard/', views.dashboard, name='dashboard'),
               path('dashboard/instantiate/', views.instantiate, name='instantiate'),
               path('dashboard/tradeoff/', views.tradeoff, name='tradeoff'),
               path('dashboard/evolution/', views.evolution, name='evolution'), ] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
