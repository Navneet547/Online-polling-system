from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
   
class LoginView(View):
   def get(self, request):
      return render(request,'login.html')
   def post(self,request):
      username=request.POST.get('username')
      password=request.POST.get('password')
      user = authenticate(request, username=username, password=password)

      if user is not None:
            login(request, user)
            return redirect("poll:poll-list")
      else:
            return render(request, 'login.html', {"message": "**Wrong email or password**"})
      
   
class RegisterView(View):
   def get(self, request):
      return render(request,'register.html')
   def post(self,request):
      firstname=request.POST.get('first_name')
      lastname=request.POST.get('last_name')
      username=request.POST.get('username')
      email=request.POST.get('email')
      password=request.POST.get('password')
      cpassword=request.POST.get('cpassword')

      useralready=User.objects.filter(username=username)
      if useralready.exists():
         message = "username already exists!"
         return render(request,'register.html',{'message':message})

      if cpassword==password:
         user=User.objects.create(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email
         )
         user.set_password(password)
         user.save()
         return redirect('accounts:login')
      else:
         # messages.alert(request,"Confirm password does not match!")
         message = "Confirm password does not match!"
         return render(request,'register.html',{'message':message})


class LogoutView(View):
   def get(self,request):
    #   request.session.clear()
    logout(request)
    return redirect('accounts:login')


class Home(View):
   # @method_decorator(login_required(login_url='login'))
   def get(self,request):
      return render(request,"home.html")

class About(View):
   @method_decorator(login_required(login_url='accounts:login'))
   def get(self,request):
      return render(request,"about.html")