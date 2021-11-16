from django.shortcuts import render,redirect
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm  #to create user
from .forms import RegisterForm  #to create user
#UserCreationForm is default django utility(form) and we can use it to create new users
#But, say if we want to add extra fields to the register form, we will have to create a seperate class as we have done in forms.py


# Create your views here.
def register(response):
    if response.method == "POST":
        #form = UserCreationForm(response.POST)
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            my_group = Group.objects.get(name='new_user')
            user = User.objects.get(username= response.POST["username"])
            my_group.user_set.add(user)
        return redirect("/")
    else:
        #form = UserCreationForm()
        form = RegisterForm()
    return render(response, "register.html", {"form":form})
