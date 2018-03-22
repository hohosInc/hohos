import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from feeds.models import Feed
from django_project.decorators import ajax_required
from django.http import HttpResponse, HttpResponseBadRequest



@login_required  
def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')

        try:
            search_type = request.GET.get('type')     
            if search_type not in ['feed', 'users']:
                search_type = 'feed'

        except Exception:
            search_type = 'feed'

        count = {}
        results = {}
        results['feed'] = Feed.objects.filter(post__icontains=querystring,
                                              parent=None)
        results['users'] = User.objects.filter(
            Q(username__icontains=querystring) | Q(
                first_name__icontains=querystring) | Q(
                    last_name__icontains=querystring))
        count['feed'] = results['feed'].count()
        count['users'] = results['users'].count()

        return render(request, 'search/results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type],
        })
    else:
        return render(request, 'search/search.html', {'hide_search': True})

@login_required
@ajax_required
def searchusers(request):
    users = User.objects.filter(is_active=True)
    dump = []
    # template = '<a href="/'+ '{2}' +'/" style="text-decoration:none;">'+'<img src="'+ '{0}' +'" style="max-height:25px; max-width:25px;">  <span style="color:black;">{1}</span>\
    #   (@{2})'+'</a>'
    template = '<a href="/'+ '{2}' +'/" style="text-decoration:none;">'+'<img src="'+ '{0}' +'" style="max-height:25px; max-width:25px;">  <span style="color:purple; font-size:14px;">{1}</span>\
      (@<span style="font-size:13px;"> {2} </span>)' +'</a>'
    for user in users:
        try:
            dump.append(template.format(user.profile.get_picture(),user.profile.get_screen_name(),
                                    user.username))           
        except AttributeError:
            pass
        # if user.username != request.user.username:
        #     dump.append(template.format(user.profile.get_screen_name(),
        #                                 user.username))
        # else:
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')

@login_required
@ajax_required
def searchusers_simple(request):
    users = User.objects.filter(is_active=True)
    dump = []
    for user in users:
        try:
            dump.append(user.username)           
        except AttributeError:
            pass
        # if user.username != request.user.username:
        #     dump.append(template.format(user.profile.get_screen_name(),
        #                                 user.username))
        # else:
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')