from django.shortcuts import render
from .models import (Participante, Log_Refeicao, Log_Peso)
from django.http import HttpResponse
from datetime import datetime
import pytz

# Create your views here.

def export_csv_refeicao(request, participanteName):
    import csv
    from django.utils.encoding import smart_str

    # import pdb;
    # pdb.set_trace();

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+participanteName+'Log_Refeicao.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Refeição"),
        smart_str(u"Descrição"),
        smart_str(u"Dia"),
    ])

    # Usado para a conversao do datetime
    local_tz = pytz.timezone("America/Recife")

    # Fazendo a query para pegar as informacoes da refeicao do participante
    participante = Participante.objects.get(nome=participanteName)
    refeicoes = Log_Refeicao.objects.filter(participante=participante)
    for log in refeicoes:
        # Convertando de datetime UTC para local
        local_dt = local_tz.normalize(log.data.astimezone(local_tz))
        writer.writerow([
            smart_str(log.refeicao_nome),
            smart_str(log.descricao_refeicao),
            smart_str(local_dt.strftime("%d/%m/%Y %H:%M:%S")),
        ])
    return response

def export_csv_peso(request, participanteName):
    import csv
    from django.utils.encoding import smart_str

    # import pdb;
    # pdb.set_trace();

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+participanteName+'Log_Peso.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Peso"),
        smart_str(u"Data"),
    ])

    # Usado para a conversao do datetime
    local_tz = pytz.timezone("America/Recife") 

    # Fazendo a query para pegar as informacoes da refeicao do participante
    # GAMBIARRA PARA SE O NOME DO PARTICIPANTE TIVER DOIS MAS A GNT SO PODE DIGITAR SEM COLOCAR ESPA
    participante = Participante.objects.get(nome=participanteName)
    log_peso = Log_Peso.objects.get(participante=participante)
    
    for log in log_peso.history.all():
        # Convertando de datetime UTC para local
        local_dt = local_tz.normalize(log.data.astimezone(local_tz))
        writer.writerow([
            smart_str(log.peso),
            smart_str(local_dt.strftime("%d/%m/%Y %H:%M:%S")),
        ])
    return response
# export_csv.short_description = u"Export CSV"
