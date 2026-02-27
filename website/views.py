from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .forms import SignUpForm, AddRecordForm, CallHistoryForm, EmailForm, TaskForm
from .models import Record, CallHistory, Email, Task


def home(request):
    records = Record.objects.all()
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    
    # Search functionality
    if search_query:
        records = records.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(company__icontains=search_query)
        )
    
    # Status filter
    if status_filter:
        if status_filter == 'active':
            records = records.filter(is_active=True)
        elif status_filter == 'inactive':
            records = records.filter(is_active=False)
    
    # Customer type filter
    if type_filter:
        records = records.filter(customer_type=type_filter)

    # Check to see if logging in 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There was an error Logging In, Please Try Again.....")
            return redirect('home')
    else:
        return render(request, 'home.html', {
            'records': records,
            'search_query': search_query,
            'status_filter': status_filter,
            'type_filter': type_filter
        })

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out....")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Succesfully Registered! Welcome")
            return redirect('home')
    
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=pk)
        call_history = customer_record.call_history.all()
        emails = customer_record.emails.all()
        tasks = customer_record.tasks.all()
        
        return render(request, 'record.html', {
            'customer_record': customer_record,
            'call_history': call_history,
            'emails': emails,
            'tasks': tasks
        })
    
    else:
        messages.success(request, "You Must Be Logged In To View That Page")
        return redirect('home')

def toggle_record_status(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.is_active = not record.is_active
        record.save()
        status = "activated" if record.is_active else "deactivated"
        messages.success(request, f"Record {status} successfully")
        return redirect('record', pk=pk)
    else:
        messages.success(request, "You Must Be Logged In To Do That.....")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('home')
    
    else:
        messages.success(request, "You Must Be Logged In To Do That.....")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In....")
        return redirect('home')    
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated....")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    
    else: 
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

def add_call_history(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = CallHistoryForm(request.POST or None)
        
        if request.method == "POST":
            if form.is_valid():
                call = form.save(commit=False)
                call.record = record
                call.save()
                # Update last_contacted field
                record.last_contacted = timezone.now()
                record.save()
                messages.success(request, "Call logged successfully")
                return redirect('record', pk=pk)
        
        return render(request, 'add_call.html', {'form': form, 'record': record})
    else:
        messages.success(request, "You Must Be Logged In....")
        return redirect('home')

def add_email(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = EmailForm(request.POST or None)
        
        if request.method == "POST":
            if form.is_valid():
                email = form.save(commit=False)
                email.record = record
                email.save()
                # Update last_contacted field
                record.last_contacted = timezone.now()
                record.save()
                messages.success(request, "Email logged successfully")
                return redirect('record', pk=pk)
        
        return render(request, 'add_email.html', {'form': form, 'record': record})
    else:
        messages.success(request, "You Must Be Logged In....")
        return redirect('home')

def add_task(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = TaskForm(request.POST or None)
        
        if request.method == "POST":
            if form.is_valid():
                task = form.save(commit=False)
                task.record = record
                task.save()
                messages.success(request, "Task created successfully")
                return redirect('record', pk=pk)
        
        return render(request, 'add_task.html', {'form': form, 'record': record})
    else:
        messages.success(request, "You Must Be Logged In....")
        return redirect('home')

def delete_call(request, call_id, pk):
    if request.user.is_authenticated:
        call = CallHistory.objects.get(id=call_id)
        call.delete()
        messages.success(request, "Call record deleted")
        return redirect('record', pk=pk)
    else:
        messages.success(request, "You Must Be Logged In....")
        return redirect('home')

def delete_task(request, task_id, pk):
    if request.user.is_authenticated:
        task = Task.objects.get(id=task_id)
        task.delete()
        messages.success(request, "Task deleted")
        return redirect('record', pk=pk)
    else:
        messages.success(request, "You Must Be Logged In....")
        return redirect('home')