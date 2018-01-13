# from urllib import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from comments.forms import CommentForm
from comments.models import Comment
from .models import Post
from .forms import PostForm

  
# Create your views here.

def post_list(request, slug=None):
	form = PostForm(request.POST or None, request.FILES or None)

	queryset_list = Post.objects.all()
	title = 'Here\'s the list of all the posts'
	query = request.GET.get('q')
	if query and not request.FILES:
		queryset_list = queryset_list.filter(
							Q(title__icontains=query)
							# Q(content__icontains=query) 
								).distinct()      # distinct makes all the results to be different
	# comments = []
	queryset = queryset_list;
	# for instance in queryset:
	# 	comments.append(instance.comments)
	# for item in comments:
	# 	for subitem in item:
	# 		print subitem.content
	context = {
	'form':form,
	'title':'Create a new Post',
	'title': title,
	'object_list' : queryset,
	# 'comments':comments,
	} 

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		print instance.user


	return render(request,'post_list.html',context)


def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)  # if u dont to do or None then it'll give error on emepty data sending
	# , request.FILES or None
	context = {
	'form':form,
	'title':'Create a new Post',
	}

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
	# 	messages.success(request,'successfuly created post')
	# 	messages.success(request,'<a href="">saved</a>', extra_tags='html_safe')
	# 	# this messages are shown at the next request which is the url where redirected below
	# 	# and this message is shown once only and there might be used more than one messages like this one
	# 	# return HttpResponseRedirect(instance.get_absolute_url())
	# 	return redirect("posts:list")
	# else:
	# 	messages.error(request,'successfuly not created post')

	return render(request,'post_create.html',context)


def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	# if instance.publish > timezone.now().date() or instance.draft:
	# 	if not request.user.is_staff or not request.user.is_superuser:
	# 		raise Http404
	# share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial=initial_data )   #,initial=initial_data
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None 
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


	comments = instance.comments
	context = {
		"title": instance.title,
		"instance": instance,
		# "share_string": share_string,
		"comments": comments,
		"comment_form":form,
	}
	return render(request, "post_detail.html", context)


def post_update(request, slug=None):
	# if not request.user.is_staff or not request.user.is_superuser:
	# 	raise Http404

	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None,request.FILES or None ,instance=instance)
	context = {
	'form':form,
	'title':'Create a new Post',
	}

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

		# messages.success(request,'<a href="">successfully edited this post</a>', extra_tags='html_safe')
		# messages.success(request,'you can further edit this post')
		return redirect("posts:list")

	return render(request,'post_update.html',context)



def post_delete(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	# messages.success(request,'post successfully deleted')

	return redirect("posts:list")

