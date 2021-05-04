from django.conf.urls import url, include
from diegorocha.curriculo import views

app_name = 'curriculo'
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contact/$', views.SendContactView.as_view(), name='send-contact'),
    url(r'^healthcheck/$', views.HealthCheckView.as_view(), name='healthcheck'),
]
