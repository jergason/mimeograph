from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout
from django.template import RequestContext

def home(request):
    return render_to_response(
            'home.html',
            {},
            context_instance=RequestContext(request)
    )


def logout_view(request):
    logout(request)
    return redirect('shared.views.home')
