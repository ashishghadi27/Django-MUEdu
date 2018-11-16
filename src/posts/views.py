from urllib.parse import quote
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def posts_create(request):
	print(request.user)
	if str(request.user) is "AnonymousUser":
		print("here")
		return redirect("/login")

	if request.user.is_staff or request.user.is_superuser:
		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, "Successfully Created")
			return HttpResponseRedirect(instance.get_absolute_url())

		context = {

			"form": form,
		}
		return render(request, "post_form.html", context)
	elif not request.user.is_staff:
		return redirect("/")

def posts_detail(request, id=None):
	instance = get_object_or_404(Post,id=id)
	share_string = quote(instance.content)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	context = {
		"title":instance.title,
		"instance":instance,
		"share_string":share_string, 
	}
	return render(request, "post_detail.html", context)

def posts_list(request):
	queryset_list = Post.objects.active() #.order_by("-timestamp")

	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list, 10)
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list": queryset,
		"title":"List"
	}
	return render(request, "Home_page.html", context)

def posts_update(request, id=None):
	if request.user.is_staff or request.user.is_superuser:
		
		instance = get_object_or_404(Post,id=id)
		form = PostForm(request.POST or None, request.FILES or None, instance=instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, "Successfully Updated")
			return HttpResponseRedirect(instance.get_absolute_url())
		

		context = {
			"title":instance.title,
			"instance":instance,
			"form":form,
		}
		return render(request, "post_form.html", context)

	else:
		raise Http404

def posts_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,id=id)
	instance.delete()
	messages.success(request, "Successfully Deleted")
	return redirect("posts:list")

def no_staff(request):
	return render(request, "nostaff.html", {})