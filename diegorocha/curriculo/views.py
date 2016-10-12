from django.views import generic
from diegorocha.curriculo import models
from django.shortcuts import get_object_or_404


class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def profile(self):
        profile = models.Profile.objects.first()
        return profile
