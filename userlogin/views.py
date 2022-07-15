from django.shortcuts import render
from ast import If
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control



def signup(request):

    if request.method =="POST":

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if username=="":
                messages.error(request,"username is empty")
                return render(request,'authentication/signup.html')
            elif len(username)<2:
                messages.error(request,"username is too short")
                return render(request,'authentication/signup.html')
            elif not username.isalpha():
                messages.error(request,"username must contain alphabets")
                return render(request,'authentication/signup.html')
            elif not username.isidentifier():
                messages.error(request,"username start must start with alphabets")
                return render(request,'authentication/signup.html')
            elif User.objects.filter(username = username):
                messages.error(request,"username exits")
                return render(request,'authentication/signup.html')
            elif email=="":
                messages.error(request,"email field is empty")
                return render(request,'authentication/signup.html')
            elif len(email)<2:
                messages.error(request,"email is too short")
                return render(request,'authentication/signup.html')

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'signup.html')

            elif User.objects.filter(email=email):
                messages.error(request,"email already exist try another")
                return render(request,'authentication/signup.html')
            else:
                myuser =User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password1,email=email)
                myuser.save()

                messages.success(request, "Your account has been successfully created.")

                return redirect(home)

    return render(request, "authentication/signup.html")

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def signin(request):
        if 'username' in request.session:
            return redirect(home)

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass1')
            user = authenticate(username=username, password=password)
           
            if user is None:
                messages.error(request, "enter correct details")
                return redirect(signin)
            else:
                request.session['username'] = username
                login(request, user)
                return redirect(home)

        return render(request, "authentication/signin.html")

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def home(request):
    if "username" in request.session:
        return render(request, "authentication/index.html")
    return redirect(signin)

def signout(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect(signin)    