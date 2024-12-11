"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('reporter/dashboard/', views.reporter_dashboard, name='reporter_dashboard'),
    path('filereport/', views.filereport, name='filereport'),
    path('supervisor/dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),


    path('assign_complaint/<int:complaint_id>/', views.assign_complaint, name='assign_complaint'),
    path('close/<int:complaint_id>/', views.close_complaint, name='close_complaint'),
    
   
    path('worker/dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('worker/start/<int:complaint_id>/', views.start_work, name='start_work'),  
    path('worker/resolve/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'), 
    
   
    path('loginpage/', views.loginpage, name='loginpage'),
    path('loginform/', views.user_login, name='loginform'),
    path('logout/', views.logout_user, name='logout'),


    path('userregister/', views.userregister, name='userregister'),
    path('workerregister/', views.workerregister, name='workerregister'),
    path('worker_register/', views.workerregform, name='worker_register'),
    path('reporter_register/', views.reporterregform, name='reporter_register'),
    
   
    path('complaints/', views.complaints_list, name='complaints_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)