from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from main_application.forms import ContactForm
from main_application.models import Report, Blog, CustomerLead


# Create your views here.
class IndexView(View):
    def get(self, request):
        reports = Report.objects.all().order_by('-release_date', '-id')[:3]
        blogs = Blog.objects.all().order_by('-created_at', '-id')[:3]
        context = {'reports': reports, 'blogs': blogs}
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


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        context = {'form': form}
        return render(request, 'main_application/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                # Send email
                send_mail(
                    subject=subject,
                    message=f'{name} - {email}\n{message}',
                    from_email=email,
                    recipient_list=[settings.EMAIL_HOST_USER, 'kamerelinda14@gmail.com'],
                    fail_silently=False,
                )

                # Save form data to the database
                customer_lead = CustomerLead.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )

                # Return success response
                return JsonResponse({'message': 'Your message has been sent. Thank you!'})

            except Exception as e:
                # Return error response
                return JsonResponse({'errors': 'An error occurred while sending the email.'}, status=500)

        else:
            # Return form validation errors
            return JsonResponse({'errors': form.errors}, status=400)
