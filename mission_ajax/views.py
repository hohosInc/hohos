from django.shortcuts import render

# from django.http import JsonResponse
# from django.views import View

# from .forms import PhotoForm
# from .models import Photo

  
def basics(request): 
	return render(request, 'mission_ajax/basics_new.html', {})

def effects(request):
	return render(request,'mission_ajax/jquery_effects.html', {})

def interactions(request):
	return render(request, 'mission_ajax/jquery_interactions.html', {})

def widgets(request):
	return render(request, 'mission_ajax/widgets.html', {})

def file_upload(request):
	return render(request, 'mission_ajax/file_upload.html', {})

def test(request):
	return render(request, 'mission_ajax/test.html', {})
# class BasicUploadView(View):
#     def get(self, request):
#         photos_list = Photo.objects.all()
#         return render(self.request, 'photos/basic_upload/index.html', {'photos': photos_list})

#     def post(self, request):
#         form = PhotoForm(self.request.POST, self.request.FILES)
#         if form.is_valid():
#             photo = form.save()
#             data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
#         else:
#             data = {'is_valid': False}
#         return JsonResponse(data)