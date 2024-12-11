from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

def loginpage(request):
    return render(request, 'loginpage.html')

SUPERVISOR_USERNAME = 'admin123'
SUPERVISOR_PASSWORD = 'Super@123'

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check for supervisor login
        if username == SUPERVISOR_USERNAME and password == SUPERVISOR_PASSWORD:
            request.session['role'] = 'supervisor'
            return redirect('supervisor_dashboard')

        # Authenticate worker or reporter
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Check the user's role and redirect accordingly
            if user.role == 'REPORTER':
                return redirect('reporter_dashboard')
            elif user.role == 'WORKER':
                return redirect('worker_dashboard')
            elif user.role == 'SUPERVISOR':
                return redirect('supervisor_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('loginpage')

    return render(request, 'loginpage.html')


def workerregister(request):
    return render(request,'workerregister.html')

def workerregform(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        job = request.POST['job']
        
        # Create Worker instance and save
        worker = Worker(firstname=firstname, lastname=lastname, email=email, phone=phone, 
                        username=username, password=password, job=job)
        worker.save()
        messages.success(request, 'Worker registered successfully')
        return redirect('supervisor_dashboard')
    
    return render(request, 'workerregister.html')


def userregister(request):
    return render(request, 'register.html')

# Reporter registration view
def reporterregform(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        confpassword = request.POST['confpassword']

        if password != confpassword:
            messages.error(request, 'Passwords do not match')
            return redirect('userregister')

        # Create Reporter instance and save
        reporter = Reporter(firstname=firstname, lastname=lastname, email=email, phone=phone, 
                            username=username, password=password, confpassword=confpassword)
        reporter.save()
        messages.success(request, 'Reporter registered successfully')
        return redirect('login')
    
    return render(request, 'register.html')


@login_required
def reporter_dashboard(request):
    if request.user.role != CustomUser.Role.REPORTER:
        return redirect('loginpage')
    reporter = Reporter.objects.get(user=request.user)
    complaints = Complaint.objects.filter(reporter=reporter).order_by('-created_at')
    return render(request, 'reporter.html', {'complaints': complaints})

@login_required
def filereport(request):
    if request.user.role != CustomUser.Role.REPORTER:
        return redirect('loginpage')
    return render(request, 'filereport.html')

@login_required
def submit_complaint(request):
    if request.user.role != CustomUser.Role.REPORTER:
        return redirect('loginpage')

    if request.method == 'POST':
        try:
            reporter = Reporter.objects.get(user=request.user)
       
            complaint = Complaint.objects.create(
                reporter=reporter,
                title=request.POST.get('title'),
                genre=request.POST.get('genre'),
                description=request.POST.get('description'),
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'),
                status='PENDING'
            )
           
            if 'image' in request.FILES:
                complaint.image = request.FILES['image']
                complaint.save()
            
            messages.success(request, 'Complaint submitted successfully!')
            return redirect('reporter_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error submitting complaint: {str(e)}')
            return redirect('filereport')
    
    return render(request, 'filereport.html')



@login_required
def supervisor_dashboard(request):
    if request.user.role != CustomUser.Role.SUPERVISOR:
        return redirect('loginpage')
    
    complaints = Complaint.objects.all().order_by('-created_at')
    workers = Worker.objects.all()  # Fetch all workers
    return render(request, 'supervisor.html', {
        'complaints': complaints,
        'workers': workers
    })


@login_required
def assign_complaint(request, complaint_id):
    if request.user.role != CustomUser.Role.SUPERVISOR:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('supervisor_dashboard')
    
    if request.method == 'POST':
        try:
            # Retrieve the complaint
            complaint = get_object_or_404(Complaint, id=complaint_id)

            # Get the selected worker's username from the form submission
            worker_username = request.POST.get('worker_username')
            worker = get_object_or_404(Worker, user__username=worker_username)
            
            # Ensure the complaint is in the "PENDING" state
            if complaint.status == 'PENDING':
                complaint.assigned_to = worker
                complaint.status = 'IN_PROGRESS'
                complaint.save()

                messages.success(request, f'Complaint assigned to {worker.user.get_full_name()} successfully!')
            else:
                messages.error(request, 'Complaint is not in PENDING status.')
        except Exception as e:
            messages.error(request, f'Error assigning complaint: {str(e)}')

    return redirect('supervisor_dashboard')


def logout_user(request):
    request.session.flush() 
    return redirect('loginpage')


@login_required
def worker_dashboard(request):
    try:
        worker = Worker.objects.get(user=request.user)
        complaints = Complaint.objects.filter(assigned_to=worker)

        return render(request, 'worker.html', {
            'complaints': complaints
        })
    except Worker.DoesNotExist:
        messages.error(request, 'You are not assigned as a Worker in the system.')
        return redirect('loginpage')
    

@login_required
def start_work(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    
    if complaint.assigned_to.user == request.user and complaint.status == 'PENDING':
        complaint.status = 'IN_PROGRESS'
        complaint.save()

    return redirect('worker_dashboard')

def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if complaint.assigned_to is None or complaint.assigned_to.user != request.user:
        return redirect('worker_dashboard')  
    complaint.status = 'RESOLVED'
    complaint.save()
    return redirect('worker_dashboard')


def close_complaint(request, complaint_id):

    complaint = get_object_or_404(Complaint, id=complaint_id)
    if complaint.status != "PENDING":
        return redirect('supervisor_dashboard') 
    complaint.status = 'CLOSED'
    complaint.save()

    return redirect('supervisor_dashboard')

def complaints_list(request):
    complaints = Complaint.objects.all()  
    return render(request, 'supervisor/complaints_list.html', {'complaints': complaints})
