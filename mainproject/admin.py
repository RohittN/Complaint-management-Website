# project1/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Reporter, Supervisor, Worker, Complaint

admin.site.register(CustomUser)
admin.site.register(Reporter)
admin.site.register(Supervisor)
admin.site.register(Worker)
admin.site.register(Complaint)