from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext

def home(request):
    return render_to_response('home.html',
            {},
            context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect('shared.views.home')

def signup_view(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        # if form.is_valid():
            #create the new user
        if request.POST['password'] != request.POST['password2']:
            #TODO: set a validation error
            print("passwords didn't match!")
        else:
            u = User.objects.create_user(request.POST['username'],
            request.POST['email'], request.POST['password'])
        # u = User.objects.create_user(form.cleaned_data['username'],
        #             form.cleaned_data['email'], form.cleaned_data['password'])
            u.save()
            logged_in = authenticate(username=u.username,
                    password=request.POST['password'])
            if logged_in is None:
                print("Uh oh, couldn't log in the user we just created!")
            else:
                login(request, logged_in)
        return redirect('mime.views.own_feed')
    else:
        signup_form = UserCreationForm()
        # print(signup_form.to_p())
        return render_to_response(
                'signup.html',
                { 'signup_form': signup_form, 'beans': 'A BUNCH OF BEANS', },
                context_instance=RequestContext(request))
