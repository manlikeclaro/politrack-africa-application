import cloudinary
from decouple import config
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from main_application.forms import ContactForm
from main_application.models import Report, Blog, CustomerMessage

# Retrieve Cloudinary cloud name from env variables
# cloud_name = config('CLOUD_NAME')
# api_key = config('API_KEY')
# api_secret = config('API_SECRET')


# Construct the download URL using the cloud name and asset ID
# def generate_download_url(cloud_name, asset_id):
#     return f"https://res-console.cloudinary.com/{cloud_name}/media_explorer_thumbnails/{asset_id}/download"


# Create your views here.
class IndexView(View):
    def get(self, request):
        blogs = Blog.objects.all().order_by('-created_at', '-id')[:3]
        reports = Report.objects.all().order_by('-release_date', '-id')[:3]

        # Generate download URLs for each report using cloudinary
        # for report in reports:
        #     if report.cloudinary_asset_id:  # Check if cloudinary_url is not empty
        #         asset_id = report.cloudinary_asset_id  # Retrieve Cloudinary asset ID
        #         report.download_url = generate_download_url(cloud_name, asset_id)  # Generate download URL
        #     else:
        #         report.download_url = None

        context = {'reports': reports, 'blogs': blogs}
        return render(request, 'main_application/index.html', context)


class BlogView(View):
    def get(self, request):
        blogs = Blog.objects.all().order_by('-created_at')
        context = {'blogs': blogs}
        return render(request, 'main_application/all-blogs.html', context)


class BlogDetails(View):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        context = {'blog': blog}
        return render(request, 'main_application/blog-details.html', context)


class ReportView(View):
    def get(self, request):
        reports = Report.objects.all().order_by('-release_date', '-id')

        # Generate download URLs for each report
        # for report in reports:
        #     if report.cloudinary_asset_id:  # Check if cloudinary_url is not empty
        #         asset_id = report.cloudinary_asset_id  # Retrieve Cloudinary asset ID
        #         report.download_url = generate_download_url(cloud_name, asset_id)  # Generate download URL
        #     else:
        #         report.download_url = None

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
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER, email],
                    fail_silently=False,
                )

                # Save form data to the database
                customer_message = CustomerMessage.objects.create(
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
