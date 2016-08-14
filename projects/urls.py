from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

from projects.logic.pi import calculate_pi
from projects.logic.e import calculate_e
from projects.logic.fibonacci import fib

app_name = 'projects'
urlpatterns = [
	url(r'^$',
		views.karan_project,
		name='karan',
		kwargs={'current_page': 'portfolio'}),
]