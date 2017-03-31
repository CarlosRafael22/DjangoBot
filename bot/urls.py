from django.conf.urls import url
from bot import views

urlpatterns = [
	url(r'^bot/monitoramento_refeicao/(?P<participanteName>[\w]+)/$', views.export_csv_refeicao),
	
]

# #Using format suffixes gives us URLs that explicitly refer to a given format, 
# #and means our API will be able to handle URLs such as http://example.com/api/items/4.json.
# urlpatterns = format_suffix_patterns(urlpatterns)