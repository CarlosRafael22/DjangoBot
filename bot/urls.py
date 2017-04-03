from django.conf.urls import url
from bot import views

# Modificado o regex para aceitar com espaco ou nao: _refeicao/Rosangela ou _refeicao/Carlos Rafael
urlpatterns = [
	url(r'^bot/monitoramento_refeicao/(?P<participanteName>[\w]+\s*[\w]+)/$', views.export_csv_refeicao),
	url(r'^bot/monitoramento_peso/(?P<participanteName>[\w]+\s*[\w]+)/$', views.export_csv_peso),
	# url(r'^bot/monitoramento_refeicao/$', views.export_csv_refeicao_todos),
	# url(r'^bot/monitoramento_peso/$', views.export_csv_peso_todos),
	
]

# #Using format suffixes gives us URLs that explicitly refer to a given format, 
# #and means our API will be able to handle URLs such as http://example.com/api/items/4.json.
# urlpatterns = format_suffix_patterns(urlpatterns)