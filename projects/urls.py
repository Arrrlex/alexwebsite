from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

from projects.logic.pi import calculate_pi
from projects.logic.e import calculate_e
from projects.logic.fibonacci import fib

app_name = 'projects'
urlpatterns = [
	url(r'^$',
		TemplateView.as_view(template_name='projects/index.html'),
		name='index'),
	url(r'^pi/$',
		views.project,
		kwargs={
		'template_page': 'projects/pi.html',
		'submit': 'projects:pi',
		'calculate': calculate_pi
		},
		name='pi'),
	url(r'^e/$',
		views.project,
		kwargs={
		'template_page': 'projects/e.html',
		'submit': 'projects:e',
		'calculate': calculate_e
		},
		name='e'),
	url(r'^fibonacci/$',
		views.project,
		kwargs={
		'template_page': 'projects/fibonacci.html',
		'submit': 'projects:fibonacci',
		'calculate': fib},
		name='fibonacci'),
	url(r'^prime-factors/$', views.prime_factors, name='prime-factors'),
	url(r'^binary-converter/$', views.binary_converter, name='binary-converter'),
]