import requests
import os, sys
import urllib

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eleveBot.settings")
sys.path.append(os.path.join(os.path.dirname(__file__), 'eleveBot'))

# This is so my local_settings.py gets loaded.
os.chdir(os.path.join(os.path.dirname(__file__), 'eleveBot'))

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from bot.models import *

URL_REFEICAO = "http://localhost:8000/bot/monitoramento_refeicao/"
URL_PESO = "http://localhost:8000/bot/monitoramento_peso/"


def craw_monitoramento_refeicao():

	participantesNomes = []

	for participante in Participante.objects.all():
		# participantesNomes.append(participante.nome)
		response = requests.get(URL_REFEICAO+participante.nome)
		print("Pegando CSV Refeicao de "+participante.nome)
		import pdb;
		pdb.set_trace();

		with open(participante.nome+"Refeicao.csv", 'w') as f:
			f.write(response)


def craw_monitoramento_peso():

	participantesNomes = []

	for participante in Participante.objects.all():
		# participantesNomes.append(participante.nome)
		# requests.get(URL_PESO+participante.nome)
		urllib.url_retrive(URL_PESO+participante.nome,"/Users/irenadeveloper/Documents/DownloadsMonitoramento")
		print("Pegando CSV Peso de "+participante.nome)

craw_monitoramento_refeicao()

