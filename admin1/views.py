import email
from django.shortcuts import render
from ast import If
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
# Create your views here.
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def adminsignin(request):
        if 'username' in request.session:
            return redirect(adminhome)

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass1')
            user = authenticate(username=username, password=password)
           
            if user is not None and user.is_superuser:
                request.session['username'] = username
                login(request, user)
                return redirect(adminhome)
            else:
                messages.error(request, "enter correct details")
                return redirect(adminsignin)
        return render(request, "authentication/adminlogin.html")

def adminhome(request):
    if 'username' in request.session:
        values=User.objects.all()
        return render(request, "authentication/adminindex.html",{"values":values})


def deleteuser(request,id):
    #  if request.method =='POST': 
        deluser=User.objects.get(id=id)
        deluser.delete()

        return redirect(adminhome)

def updateuser(request,id):
    myuser = User.objects.get(id=id)

    if request.method =='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email  = request.POST.get('email')
        # myuser = User.objects.get(id=id)
        myuser.first_name=first_name
        myuser.last_name=last_name
        myuser.email=email
        myuser.save()
        return redirect(adminhome)

    return render(request,'authentication/updateuser.html',{"values":myuser})
    
def logoutadmin(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect(adminsignin)         
def search(request):

    if request.method == 'POST':
        searchvalue = request.POST.get('search')
        searchdata = User.objects.filter(username__icontains = searchvalue)

    values = {
            'searchresult':searchdata
        }
    return render(request,'authentication/search.html',values)

def adduser(request):

    if request.method =="POST":

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
       
        #validation
        if password1 == password2:
            if username=="":
                messages.error(request,"username is empty")
                return render(request,'authentication/adduser.html')
            elif len(username)<2:
                messages.error(request,"username is too short")
                return render(request,'authentication/adduser.html')
            elif not username.isalpha():
                messages.error(request,"username must contain alphabets")
                return render(request,'authentication/adduser.html')
            elif not username.isidentifier():
                messages.error(request,"username start must start with alphabets")
                return render(request,'authentication/adduser.html')
            elif User.objects.filter(username = username):
                messages.error(request,"username exits")
                return render(request,'authentication/adduser.html')
            elif email=="":
                messages.error(request,"email field is empty")
                return render(request,'authentication/adduser.html')
            elif len(email)<2:
                messages.error(request,"email is too short")
                return render(request,'authentication/adduser.html')

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'signup.html')

            elif User.objects.filter(email=email):
                messages.error(request,"email already exist try another")
                return render(request,'authentication/adduser.html')
            else:
                myuser =User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password1,email=email)
                myuser.save()

                messages.success(request, "Your account has been successfully created.")

                return redirect(adminhome)

    return render(request, "authentication/adduser.html")
