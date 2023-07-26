from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Create your views here.
@login_required(login_url='login')
def home(request):
    logout(request)
    return redirect('login')      

def sign_up(request):
    if request.method == 'POST':
        uname = request.POST.get('username')   
        email = request.POST.get('email')   
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password2')   

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            # Create and save the user in the User model (optional)
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)

            # Save the user profile data in the UserProfile model
            user_profile = UserProfile(username=uname, email=email, password=pass1)
            user_profile.save()

            return redirect('login')

    return render(request, 'signup.html') 

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            return HttpResponse ("Provide correct credentials!!!")

    return render (request,'login.html')




def dashboard(request):
    
    total_users = UserProfile.objects.all().count() 

    # Check if the user is authenticated before accessing UserProfile
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(username=request.user.username)
        except UserProfile.DoesNotExist:
            user_profile = None
    else:
        user_profile = None
    
    # Fetch all registered users from UserProfile model
    all_users = UserProfile.objects.all()

    return render(request, 'dashboard.html', {'total_users': total_users, 'user_profile': user_profile, 'all_users': all_users})



@login_required(login_url='login')
def user_profile(request):
    # Retrieve the user profile of the logged-in user
    user_profile = UserProfile.objects.get(username=request.user.username)
    
    return render(request, 'user_profile.html', {'user_profile': user_profile})  
