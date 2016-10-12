from django.views import generic
from django.conf import settings
from django.http import JsonResponse
from diegorocha.curriculo import models
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage


class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def profile(self):
        profile = models.Profile.objects.first()
        return profile


class SendContactView(generic.View):

    def post(self, request, *args, **kwargs):
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('from_email', '')
        profile = models.Profile.objects.first()
        response = {'success': False}
        if subject and message and from_email and profile:
            try:
                email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [profile.contact_email], reply_to=[from_email])
                if email.send():
                    response['success'] = True
            except Exception as ex:
                response['error'] = str(ex)
        return JsonResponse(response)
