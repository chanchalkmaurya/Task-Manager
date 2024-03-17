from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist.forms import TaskForm
from todolist.models import TaskList
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')


def tasklist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save()
        messages.success(request, ("new task added"))
        return redirect("tasklist")
    else:
        all_task = TaskList.objects.all()
        
        ## pending and completed task
        pending_task = 0
        completed_task = 0
        for task in all_task:
            if not task.done:
                pending_task += 1
            else:
                completed_task += 1
        
        parameters = {
            'title':"Task Manager",
            'all_task':all_task,
            'pending_task':pending_task,
            'completed_task':completed_task
        }
        return render(request, "task.html", parameters)
    
    
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.delete()
    messages.success(request, ("task \"" + task.task + "\" deleted."))
    return redirect("tasklist")


def edit_task(request, task_id):
    if request.method == "POST":
        task_obj = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task_obj)
        if form.is_valid():
            form.save()
            
        messages.success(request, (task_obj.task + " is updated."))
        return redirect("tasklist")
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'obj':task_obj})
    
    
def complete_uncomplete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = not task.done
    task.save()
    return redirect('tasklist')
