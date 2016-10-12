from django.contrib import admin
from diegorocha.curriculo import models


class JobsInline(admin.StackedInline):
    extra = 0
    model = models.Job


class EducationInline(admin.StackedInline):
    extra = 0
    model = models.Education


class SocialMediaInline(admin.StackedInline):
    extra = 0
    model = models.SocialMedia


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = (SocialMediaInline, EducationInline, JobsInline, )
