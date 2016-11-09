from django.views import generic
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from diegorocha.curriculo import models
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import ensure_csrf_cookie


default_cache = cache_page(60 * 30)


@method_decorator(default_cache, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
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


@method_decorator(default_cache, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class NotFoundView(generic.View):
    template_name = 'not-found.html'

    def dispatch(self, request, *args, **kwargs):
        return render(request, self.template_name)
