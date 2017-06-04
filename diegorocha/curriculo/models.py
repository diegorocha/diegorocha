from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Profile(models.Model):
    name = models.CharField('Name', max_length=100, null=True)
    title = models.CharField('Title', max_length=100)
    subtitle = models.CharField('Subtitle', max_length=100)
    profile_subtitle = models.CharField('Profile Subtitle', max_length=100)
    profile_text = models.TextField('Profile Text')
    education_subtitle = models.CharField('Education Subtitle', max_length=100, null=True)
    experience_subtitle = models.CharField('Experience Subtitle', max_length=100, null=True)
    contact_subtitle = models.CharField('Contact Subtitle', max_length=100, null=True)
    contact_address = models.CharField('Contact Address', max_length=100, null=True)
    contact_phone = models.CharField('Contact Phone', max_length=100, null=True)
    contact_email = models.EmailField('Contact E-mail', null=True)
    resumee_link = models.URLField('Link Resumee', default='')

    def __str__(self):
        return 'Profile of %s' % self.name


@python_2_unicode_compatible
class Job(models.Model):
    class Meta:
        ordering = ['-start_date', ]
    profile = models.ForeignKey(Profile, related_name='jobs')
    company = models.CharField('Company', max_length=100)
    position = models.CharField('Position', max_length=100)
    start_date = models.DateField('Start')
    end_date = models.DateField('End', null=True, blank=True)
    description = models.TextField('Description')

    def __str__(self):
        return '%s - %s' % (self.company, self.position)


@python_2_unicode_compatible
class Education(models.Model):
    class Meta:
        ordering = ['-start_year']
    EM_CURSO = 'E'
    CONCLUIDO = 'C'
    TRANCADO = 'T'
    STATUS_CHOICES = (
        (EM_CURSO, 'Em Curso'),
        (TRANCADO, 'Trancado'),
        (CONCLUIDO, 'Concluido'),
    )
    profile = models.ForeignKey(Profile, related_name='educations')
    title = models.CharField('Title', max_length=100)
    degree = models.CharField('Degree', max_length=100)
    status = models.CharField('Status', max_length=1, choices=STATUS_CHOICES, default=EM_CURSO)
    start_year = models.IntegerField('Start')
    end_year = models.IntegerField('End', null=True, blank=True)
    description = models.TextField('Description')

    def __str__(self):
        return '%s at %s' % (self.degree, self.title)


@python_2_unicode_compatible
class SocialMedia(models.Model):
    class Meta:
        ordering = ['order', 'name']
    profile = models.ForeignKey(Profile, related_name='social_media')
    name = models.CharField('Name', max_length=20)
    link = models.URLField('URL')
    icon = models.CharField('Icon', max_length=30)
    order = models.IntegerField('Order', blank=True, default=1)

    def __str__(self):
        return self.name
