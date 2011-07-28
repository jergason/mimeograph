from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from mime.models import Mime
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core.mail import send_mail
from mimeograph_utils import get_flash_messages, set_flash_message
import re

def home(request):
    recent_posts = Mime.objects.all().order_by("-pub_date")[:5]
    return render_to_response('home.html',
            { 'flash': get_flash_messages(request),
                'mimes': recent_posts },
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
        email_re = re.compile("\w+@\w+\.\w+")
        username_re = re.compile("[\w\d]+")
        if request.POST['password'] != request.POST['password2']:
            set_flash_message(request, 'error', "Password and password confirmation did not match!")
        elif not email_re.match(request.POST['email']):
            set_flash_message(request, 'error', 'Looks like your email address didn\'t match our naive regex.')
        elif not username_re.match(request.POST['username']):
            set_flash_message(request, 'error', "Username must be alphanumeric characters only.")
        elif request.POST['password'] == "" or request.POST['username'] == '' or request.POST['email'] == '' or request.POST['password2'] == '':
            set_flash_message(request, 'error', "Fields must not be blank.")
        else:
            u = User.objects.create_user(request.POST['username'],
            request.POST['email'], request.POST['password'])
            u.save()
            authenticated_user = authenticate(username=u.username,
                    password=request.POST['password'])
            if authenticated_user is None:
                print("Uh oh, couldn't log in the user we just created!")
                set_flash_message(request,'error',"A strange error occurred. Please try loggin in manually.")
            else:
                login(request, authenticated_user)
                set_flash_message(request, 'success', "Successfully created user.  You have been logged in automatically.")
                return redirect('mime.views.own_feed')
        return redirect('shared.views.signup_view')
    else:
        signup_form = UserCreationForm()
        return render_to_response(
                'signup.html',
                { 'flash': get_flash_messages(request), 'signup_form': signup_form, 'beans': 'A BUNCH OF BEANS', },
                context_instance=RequestContext(request))

def forgot_password(request):
    if request.method == "POST":
        # see if there is a user with that usename and email address.
        # if so, reset the password and email it to them
        # if not, set an error and redirect to the same page.
        if User.objects.filter(username=request.POST['username'], email=request.POST['email']).exists():
            u = User.objects.filter(username=request.POST['username'], email=request.POST['email'])[0]
            #SECURE LIKE SONY!
            random_password = "BAKEDBEANS"
            message = "Hey, just wanted to let you know that the password for %s on Mimeograph was reset to %s. Please log in!" % (u.username, random_password)
            u.set_password(random_password)
            u.save()
            # send an email to them.
            send_mail('Password Reset on Mimeograph', message,
                    'noreply@mimeograph.com', [u.email], fail_silently=True)
            set_flash_message(request, 'success', "Password successfully reset for %s." % u.username)
            return redirect('shared.views.home')
        else:
            set_flash_message(request, 'error', "No user named %s with email address name %s." % (request.POST['username'], request.POST['email']))
            return redirect('shared.views.forgot_password')
    else:
        #show the form
        return render_to_response('reset.html', {}, context_instance=RequestContext(request))
