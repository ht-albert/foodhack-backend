from django.conf.urls import url
from ingredients import views

urlpatterns = [
    url(r'get_list/$', views.get_random_item),
]
