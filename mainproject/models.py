from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=15, default='0000000000')
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Reporter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Supervisor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Worker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=50, choices=[
        ('ELECTRICIAN', 'Electrician'),
        ('PLUMBER', 'Plumber'),
        ('CLEANER', 'Cleaner'),
        ('WASTE_DISPOSER', 'Waste Disposer'),
        ('OTHER', 'Other')
    ], default='OTHER')

    def __str__(self):
        return self.user.username

class Complaint(models.Model):
    GENRE_CHOICES = [
        ('1', 'Cleaning'),
        ('2', 'Water Supply'),
        ('3', 'Electricity'),
        ('4', 'Garbage Collection'),
        ('5', 'Others')
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed')
    ]

    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, default=1)  # Added default value
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='default_genre')
    description = models.TextField()
    image = models.ImageField(upload_to='complaint_images/', null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
