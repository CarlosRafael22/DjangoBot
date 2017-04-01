from django.shortcuts import render
from .models import (Participante, Log_Refeicao, Log_Peso)
from django.http import HttpResponse

# Create your views here.

def export_csv_refeicao(request, participanteName):
    import csv
    from django.utils.encoding import smart_str

    # import pdb;
    # pdb.set_trace();

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+participanteName+'.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Refeição"),
        smart_str(u"Descrição"),
        smart_str(u"Dia"),
    ])

    # Fazendo a query para pegar as informacoes da refeicao do participante
    participante = Participante.objects.get(nome=participanteName)
    refeicoes = Log_Refeicao.objects.filter(participante=participante)
    for obj in refeicoes:
        writer.writerow([
            smart_str(obj.refeicao_nome),
            smart_str(obj.descricao_refeicao),
            smart_str(obj.data.strftime("%Y-%m-%d %H:%M:%S")),
        ])
    return response

# def export_csv_peso(request, participanteName):
#     import csv
#     from django.utils.encoding import smart_str

#     # import pdb;
#     # pdb.set_trace();

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename='+participanteName+'.csv'
#     writer = csv.writer(response, csv.excel)
#     response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
#     writer.writerow([
#         smart_str(u"Peso"),
#         smart_str(u"Data"),
#     ])

#     # Fazendo a query para pegar as informacoes da refeicao do participante
#     participante = Participante.objects.get(nome=participanteName)
#     log_peso = Log_Peso.objects.filter(participante=participante)
#     for obj in refeicoes:
#         writer.writerow([
#             smart_str(obj.refeicao_nome),
#             smart_str(obj.descricao_refeicao),
#             smart_str(obj.data.strftime("%Y-%m-%d %H:%M:%S")),
#         ])
#     return response
# export_csv.short_description = u"Export CSV"
