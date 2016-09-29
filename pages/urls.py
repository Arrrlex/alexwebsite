from django.conf.urls import url

from . import views

from django.views.generic import TemplateView

urlpatterns = [
	url(r'^$', 
		TemplateView.as_view(template_name='pages/index.html'), 
		kwargs={'current_page': 'index'}, 
		name='index'),
	url(r'^cv$',
		TemplateView.as_view(template_name='pages/cv.html'),
		kwargs={'current_page': 'cv'},
		name='cv'),
	url(r'^contact$',
		TemplateView.as_view(template_name='pages/contact.html'),
		kwargs={'current_page': 'contact'},
		name='contact'),
]