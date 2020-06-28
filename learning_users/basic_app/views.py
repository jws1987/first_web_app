from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

#
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse('Hello!')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            print(user_form)
            user = user_form.save()
            print('----------------')
            print(user)

            user.set_password(user.password)
            print('----------------')
            print(user)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print("error")
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context_dict = {'user_form':user_form,
                    'profile_form':profile_form,
                    'registered':registered}
    return render(request,'basic_app/registration.html',context_dict)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("SOMEONE TRIED TO LOGIN AND FAILED")
            print("Username: {} / Password: {}".format(username,password))
            return HttpResponse("INVALID LOGIN DETAILS SUPPLIED")
    else:
        return render(request,'basic_app/login.html',{})
