from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from mime.models import Following, Mime, MimeForm
from datetime import datetime

@login_required
def own_feed(request):
    followees = Following.objects.filter(follower=request.user)

    #TODO: remove self from followees
    followees = request.user.get_profile().get_all_followees()
    #get most recent posts by followees ordered by time
    posts = {}

    posts = Mime.objects.filter(author__in=followees).order_by('-pub_date')[:10]
    form = MimeForm()
    return render_to_response('own_feed.html',
            {
                'u': request.user,
                'mimes': posts,
                'followees': followees,
                'form': form,
            },
            context_instance=RequestContext(request))


def other_feed(request, user_name):
    """Look at a user's feed of posts. If the user is logged in, then they will
    be able to follow the user and those they follow."""
    user = User.objects.filter(username=user_name)
    #if they are trying to look at their own page, then
    #show the correct one
    if request.user.username == user_name:
        return redirect('mime.views.own_feed')
    if user.count() == 0:
        print("Other feed for %s not found" % user_name)
        raise Http404
    else:
        user = user[0]
        posts = Mime.objects.filter(author=user)
        following = Following.objects.filter(follower=User.objects.get(username=request.username),
                followee=User.objects.get(username=user_name)).exists()
        return render_to_response('feed.html',
                { 'u': user, 'posts': posts, 'other_user': user_name,
                    'following': following },
            context_instance=RequestContext(request))

@login_required
def follow(request):
    if request.method == "POST":
        followee_id = request.POST['id']
        #TODO: make sure they are not already following
        following, already_follow = Following.objects.get_or_create(followee=MimographProfile.get(pk=followee_id),
                follower=request.user.get_profile())
        following.save()
        #TODO: set a flash notice that they have been followed, and redirect to the user's feed
    return redirect("mime.views.own_feed")


@login_required
def unfollow(request):
    if request.method == "POST":
        Following.objects.filter(follower=request.user.get_profile(),
                followee=MimeographProfile.objects.get(pk=request.POST['id'])).delete()
    return redirect('mime.views.own_feed')



@login_required
def mime_create(request):
    # return render_to_response('test.html')
    print("INSIDE CREATE MIME!")
    if request.method == "POST":
        form = MimeForm(request.POST)
        if form.is_valid():
            #process data, create the Mime, set the session and redirect
            mime = Mime(author=request.user.get_profile(),
                    content=form.cleaned_data['content'],
                    pub_date=datetime.now())
            if mime.save():
                #TODO: set the session
                print("Mime is saved!")
    return redirect('mime.views.own_feed')

@login_required
def mime_delete(request):
    #make sure the user is trying to delete their own mime.
    #if not, set a flash notice and redirect.
    #TODO: catch DoesNotExist errors
    if request.method == "POST":
        mime = Mime.objects.get(pk=request.POST['id'])
        if mime.author != request.user.get_profile():
            print("tried to delete a mime that is not yours!")
        else:
            mime.delete()
    return redirect('mime.views.own_feed')
