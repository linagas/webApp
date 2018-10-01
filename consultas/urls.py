from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(
        r'^$',
        views.ConsultarSebif.as_view(),
        name="detail"
    ),
]