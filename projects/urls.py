from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

from projects.logic.pi import calculate_pi
from projects.logic.e import calculate_e
from projects.logic.fibonacci import fib

app_name = 'projects'
urlpatterns = [
	url(r'^basic$',
		views.basic_projects,
		name='basic',
		kwargs={'current_page': 'portfolio'}),
	url(r'^tiling$',
		views.tiling,
		name='tiling',
		kwargs={'current_page':'portfolio'}),
]