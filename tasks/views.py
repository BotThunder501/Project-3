from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Task
from .forms import TaskForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    return render(request, 'registration/logout.html')

@login_required
def task_list(request):
    sort = request.GET.get('sort')
    if sort == 'due_date_asc':
        tasks = Task.objects.all().order_by('due_date')
    elif sort == 'due_date_desc':
        tasks = Task.objects.all().order_by('-due_date')
    elif sort == 'priority_low':
        tasks = Task.objects.filter(priority='L')  # Filter for low priority
    elif sort == 'priority_medium':
        tasks = Task.objects.filter(priority='M')  # Filter for medium priority
    elif sort == 'priority_high':
        tasks = Task.objects.filter(priority='H')  # Filter for high priority
    else:
        tasks = Task.objects.all()  # Default order
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('task_list')