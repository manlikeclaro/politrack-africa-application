from django.urls import path

from main_application import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('blog', views.BlogView.as_view(), name='blog'),
    path('blog/<slug:slug>', views.BlogDetails.as_view(), name='blog-details'),
    path('reports', views.ReportView.as_view(), name='reports'),
    path('contact', views.ContactView.as_view(), name='contact'),
]
