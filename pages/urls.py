from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^cv$', views.cv_index, name='cv_index'),
	url(r'^contact$', views.contact, name='contact'),
]