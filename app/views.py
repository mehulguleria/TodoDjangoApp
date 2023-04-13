from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from account.models import User
from app.models import Todo


def home(request):
    return render(request,'home.html')


def registeruser(request):
    
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if password != password1:
            return render(request,'register.html',{'error':'password not matching'})
        if User.objects.filter(email=email).exists():
            return render(request,'register.html',{'error':'email already exist.'})
        
        user = User.objects.create_user(email=email,name=name,password=password)
        user.save()
        return redirect(f'/verify/{email}')

    return render(request,'register.html')


def verify(request,email):

    if request.method == "POST":
        code = request.POST.get('code')

        try:
            if User.objects.get(email=email,verify=code):
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
                return redirect('/login')
            else:
                return render(request,'afterreg.html',{'error':'invalid code','email':email})
        except ObjectDoesNotExist:
            return render(request,'afterreg.html',{'error':'invalid code'})
    
    return render(request,'afterreg.html')


def userlogin(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email,password=password)

        if user:
            login(request,user)
            return redirect('/profile')
        else:
            return render(request,'login.html',{'error':'invalid credentials'})
    
    return render(request,'login.html')


@login_required(login_url='/login')
def userprofile(request):

    todolist = list(Todo.objects.filter(user=request.user,is_completed=False))

    return render(request,'profile.html',{'todolist':todolist})


@login_required(login_url='/login')
def createtodo(request):

    if request.method=="POST":
        title = request.POST.get('title')
        description = request.POST.get('description')

        todo = Todo.objects.create(user=request.user, title=title, description=description)
        todo.save()
        return redirect('/profile')
    
    return render(request,'createtodo.html')


@login_required(login_url='/login')
def detailtodo(request,id):
    try:
        todo = Todo.objects.get(id=id,user=request.user)
        return render(request,'detailtodo.html',{'todo':todo})
    except ObjectDoesNotExist:
        return render(request,'error.html')
    

@login_required(login_url='/login')
def completetodo(request,id):
    try:
        todo = Todo.objects.get(id=id,user=request.user)
        todo.is_completed = True
        todo.save()
        return redirect('/profile')
    except ObjectDoesNotExist:
        return render(request,'error.html')
    

@login_required(login_url='/login')
def history(request):

    todolist = Todo.objects.filter(user=request.user,is_completed=True)
    return render(request,'history.html',{'todolist':todolist})


@login_required(login_url='/login')
def userlogout(request):

    logout(request)
    return redirect('/login')

