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
from django.urls import path, include

from . import views

urlpatterns = [path('admin/', admin.site.urls), path('dashboard/', views.dashboard, name='dashboard'),
               path('dashboard/architecture/create/upload/', views.create_upload, name='create_upload'),
               path('dashboard/architecture/create/reference/', views.create_reference, name='create_reference'),
               path('dashboard/architecture/create/manual/', views.create_manual, name='create_manual'),
               path('dashboard/architecture/delete/<int:architecture_id>', views.architecture_delete,
                    name='architecture_delete'),
               path('dashboard/architecture/export/<int:architecture_id>', views.architecture_export,
                    name='architecture_export'),
               path('dashboard/tradeoff/', views.tradeoff, name='tradeoff'),
               path('dashboard/evolution/', views.evolution, name='evolution'),
               path('dashboard/ontospy_report/', views.ontospy_report, name='ontospy_report'),
               path('dashboard/report/html_multi/<str:file_name>/', views.report_multi,
                    name='report-multi-index'),
               path('dashboard/report/html_multi/', views.report_multi_index, name='report-multi_index'),
               path('dashboard/report/<str:report_name>/', views.report, name='report'),
               path('dashboard/delete_all_architectures/', views.delete_all_architectures,
                    name='delete_all_architectures'),
               path('', include('accounts.urls', namespace='accounts')),
               ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
