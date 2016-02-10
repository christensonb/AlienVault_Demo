from django.conf.urls import url

from app import views

from django.http import HttpResponse
def hello(request):
	return HttpResponse('Hello World!')

urlpatterns = [
    url(r'^test$', hello),

    url(r'^$', views.APIRoot.as_view(), name='api_root'),
	
    # -TODO: match /api/threat/ip/1.2.3.4
	url(r'api/threat/ip/(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$', views.IPDetailsView.as_view(), name='threat_details'),
	
	# -TODO: match /api/traffic
	url(r'api/traffic', views.TrackVisitsView.as_view(), name='threat_details'),
]