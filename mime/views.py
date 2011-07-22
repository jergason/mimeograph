from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from mime.models import Following, Mime

@login_required
def own_feed(request):
    followees = Following.objects.filter(follower=request.user)
    # for f in followees:

    #get most recent posts by followees ordered by time
    # sets = []
    # for f in Following.objects.filter(follower=request.user:
        
    return render_to_response('feed.html', { 'u': request.user },
            context_instance=RequestContext(request))


def other_feed(request, user_name):
    """Look at a user's feed of posts. If the user is logged in, then they will
    be able to follow the user and those they follow."""
    user = User.objects.filter(username=user_name)
    if user.count() == 0:
        raise Http404
    else:
        user = user[0]
        posts = Mime.objects.filter(author=user)
        #TODO: how to get their followers?
        return render_to_reponse('feed.html',
            { 'u': user, 'posts': posts },
            context_instance=RequestContext(request))

@login_required
def follow(request, user_name):
    # if !user.is_authenticated():
        #TODO: set session
    #make sure it is a POST form submission
    if request.method == "POST":
        return redirect("mime.views.own_feed")
        #get user ID from hidden field, and follow him.
        #set a flash notice that they have been followed, and redirect to the
        # user's feed
