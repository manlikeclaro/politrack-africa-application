from django.shortcuts import render, get_object_or_404
from django.views import View

from main_application.models import Report, Blog


# Create your views here.
class IndexView(View):
    def get(self, request):
        reports = Report.objects.all().order_by('-release_date', '-id')[:3]
        context = {'reports': reports}
        return render(request, 'main_application/index.html', context)


class BlogView(View):
    def get(self, request):
        blogs = Blog.objects.all().order_by('-created_at')
        context = {'blogs': blogs}
        return render(request, 'main_application/blog.html', context)


class BlogDetails(View):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        context = {'blog': blog}
        return render(request, 'main_application/blog-details.html', context)


class ReportView(View):
    def get(self, request):
        reports = Report.objects.all().order_by('-release_date', '-id')
        context = {'reports': reports}
        return render(request, 'main_application/all-reports.html', context)
