from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^pi/$', views.pi, name='project-pi'),
	url(r'^e/$', views.e, name='project-e'),
	url(r'^fibonacci/$', views.fibonacci, name='project-fibonacci'),
	url(r'^prime-factors/$', views.prime_factors, name='project-prime-factors'),
	url(r'^binary-converter/$', views.binary_converter, name='project-binary-converter'),
	url(r'^pi-results/$', views.pi_submit, name='pi-submit'),
]