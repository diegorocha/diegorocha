from django.contrib import admin
from diegorocha.curriculo.views import NotFoundView
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('diegorocha.curriculo.urls', namespace='curriculo')),
]

handler404 = NotFoundView.as_view()
