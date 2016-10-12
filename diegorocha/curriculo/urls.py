from django.conf.urls import url, include
from diegorocha.curriculo import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
]
