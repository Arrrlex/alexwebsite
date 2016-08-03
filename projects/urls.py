from django.conf.urls import url

from . import views

app_name = 'projects'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^pi/$', views.pi, name='pi'),
	url(r'^e/$', views.e, name='e'),
	url(r'^fibonacci/$', views.fibonacci, name='fibonacci'),
	url(r'^prime-factors/$', views.prime_factors, name='prime-factors'),
	url(r'^binary-converter/$', views.binary_converter, name='binary-converter'),
	url(r'^pi-results/$', views.pi_submit, name='pi-submit'),
	url(r'^e-results/$', views.e_submit, name='e-submit'),
]