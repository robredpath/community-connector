from django.conf.urls import url

from community import views

app_name = 'community'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
