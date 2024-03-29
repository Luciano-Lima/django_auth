from django.shortcuts import render, redirect, reverse 
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
# auth for the authorisation logout function # 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UseRegistrationForm

# Create your views here.
def index(request):
    """Return the index.html file"""
    return render(request, 'index.html')
    
@login_required()
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect(reverse('index'))
    
def login(request):
    """Return a login page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            messages.success(request, "You have successfully logged in!")

            if user:
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})
    
    
def registration(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
        
    if request.method == "POST":
        registration_form = UseRegistrationForm(request.POST)
        
        if registration_form.is_valid():    
            registration_form.save()
            
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
                                    
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Unabel to register your account at this time")
                
    else:
        registration_form = UseRegistrationForm()
    return render(request, 'registration.html',{'registration_form': registration_form})
            
        
def user_profile(request):
    """retrieving the user from the database with get"""
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {'profile': user})
    
    