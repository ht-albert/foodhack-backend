from django.conf.urls import url
from dish import views

urlpatterns = [
    url(r'get_list/$', views.get_list),
    # url(r'get_info/$', views.get_info)
]
