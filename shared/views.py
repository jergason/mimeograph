from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from mimeograph_utils import get_flash_messages, set_flash_message

def home(request):
    return render_to_response('home.html',
            { 'flash': get_flash_messages(request) },
            context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    print("session for logout_view is this:")
    print(request.session)
    set_flash_message(request, 'success', "You were successfully logged out.")
    print(request.session['flash'])
    return redirect('shared.views.home')

def signup_view(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        # if form.is_valid():
            #create the new user
        if request.POST['password'] != request.POST['password2']:
            #TODO: set a validation error
            set_flash_message(request, 'error', "Password and password confirmation did not match!")
        else:
            u = User.objects.create_user(request.POST['username'],
            request.POST['email'], request.POST['password'])
        # u = User.objects.create_user(form.cleaned_data['username'],
        #             form.cleaned_data['email'], form.cleaned_data['password'])
            u.save()
            authenticated_user = authenticate(username=u.username,
                    password=request.POST['password'])
            if authenticated_user is None:
                print("Uh oh, couldn't log in the user we just created!")
                set_flash_message(request,'error',"A strange error occurred. Please try loggin in manually.")
            else:
                if login(request, logged_in):
                    set_flash_message(request, 'success', "Successfully created user.  You have been logged in automatically.")
                else:
                    set_flash_message(request, 'error', "A strange error occurred. Please try loggin in manually.")
        return redirect('mime.views.own_feed')
    else:
        signup_form = UserCreationForm()
        # print(signup_form.to_p())
        return render_to_response(
                'signup.html',
                { 'flash': get_flash_messages(request), 'signup_form': signup_form, 'beans': 'A BUNCH OF BEANS', },
                context_instance=RequestContext(request))
