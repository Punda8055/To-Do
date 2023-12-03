from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import todo
# here we can write the logics
@login_required #without login we cannot able to acces the home page
def home(request):
    if request.method=='POST':
        task=request.POST.get('task')
        new_todo=todo(user=request.user,todo_name=task)
        new_todo.save()
    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos,'name':request.user #show the data and  user name
    }
    return render(request, 'todoapp/todo.html', context)
def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
#some additional validation
        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('/')
#check user exist or not
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists, User another.')
            return redirect('/')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})
def LogoutView(request):
    logout(request)
    return redirect('login')
def loginpage(request):
    if not request.user.is_authenticated:# it check user already logined
        if request.method=="POST":
            username=request.POST.get('uname')
            password=request.POST.get('pass')
# to check the database if user is exist or not
            validate_user=authenticate(username=username,password=password)
            if validate_user is not None:
                login(request,validate_user)
                return redirect('home-page')
        # if doesn't exist
            else:
                messages.error(request,"wrong user details")
                return redirect('login')
        return render(request,'todoapp/login.html',{})
    else:
        return redirect('home-page') # if user already logined it directly go to the home page
# delete the data based on database id
def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')


def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')