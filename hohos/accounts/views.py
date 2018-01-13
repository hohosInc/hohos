# from django.contrib.auth import (
#     authenticate,
#     get_user_model,
#     login,
#     logout,

#     )
# from django.shortcuts import render, redirect

# from .forms import UserLoginForm, UserRegisterForm

# def login_view(request):
#     print(request.user.is_authenticated())
#     next = request.GET.get('next')
#     title = "Login"
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         if next:
#             return redirect(next)
#         return redirect("/")
#     return render(request, "form.html", {"form":form, "title": title})


# def register_view(request):
#     print(request.user.is_authenticated())
#     next = request.GET.get('next')
#     title = "Register"
#     form = UserRegisterForm(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         password = form.cleaned_data.get('password')
#         user.set_password(password)
#         user.save()
#         new_user = authenticate(username=user.username, password=password)
#         login(request, new_user)
#         if next:
#             return redirect(next)
#         return redirect("/")

#     context = {
#         "form": form,
#         "title": title
#     }
#     return render(request, "form.html", context)


# def logout_view(request):
#     logout(request)
#     return redirect("/")


from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
# from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from .models import UserProfile


def registration(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('home')
        if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    user = User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'],
                                                    password=form.cleaned_data['password'])
                    user.save()
                    styler = UserProfile(user=user,name=form.cleaned_data['name'],birthday=form.cleaned_data['birthday'])
                    styler.save()
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request,'registration_form.html',{'form':form})

        else:
                ''' user is not submitting the form, show them a blank registration form '''
                form = RegistrationForm()
                context = {'form': form}
                return render(request,'registration_form.html', context) 
                    #context_instance=RequestContext(request))


def Login(request):
        if request.user.is_authenticated():
                return redirect('home')
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        styler = authenticate(username=username, password=password)
                        if styler is not None:
                                login(request,styler)
                                return redirect('home')
                        else:
                                return render(request,'login_form.html', {'form': form})
                else:
                        return render(request,'login_form.html', {'form': form})
        else:
                ''' user is not submitting the form, show the login form '''
                form = LoginForm()
                context = {'form': form}
                return render(request,'login_form.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('/')
