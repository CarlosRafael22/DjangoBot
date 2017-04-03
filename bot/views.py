from django.shortcuts import render
from .models import (Participante, Log_Refeicao, Log_Peso)
from django.http import HttpResponse
from datetime import datetime
import pytz

# Create your views here.

# OPCOES DE REFEICOES
CAFE_DA_MANHA = "Café da manhã"
LANCHE_MANHA = "Lanche da manhã"
ALMOCO = "Almoço"
LANCHE_TARDE = "Lanche da tarde"
JANTAR= "Jantar"
LANCHE_NOITE = "Lanche da noite"

# OPCOES DE REFEICOES
# Vai ser usado como index para saber onde vai escrever o CSV

refeicao_index = {
    CAFE_DA_MANHA : 0,
    LANCHE_MANHA : 1,
    ALMOCO : 2,
    LANCHE_TARDE : 3,
    JANTAR : 4,
    LANCHE_NOITE : 5
}

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
        smart_str(u"Dia"),
        smart_str(u"Café da manhã"),
        smart_str(u"Lanche da manhã"),
        smart_str(u"Almoço"),
        smart_str(u"Lanche da tarde"),
        smart_str(u"Jantar"),
        smart_str(u"Lanche da noite"),
    ])

    # Usado para a conversao do datetime
    local_tz = pytz.timezone("America/Recife")

    # Fazendo a query para pegar as informacoes da refeicao do participante
    participante = Participante.objects.get(nome=participanteName)
    refeicoes = Log_Refeicao.objects.filter(participante=participante)
    for log in refeicoes:

        # Pegando o tipo de refeicao para ver em que coluna ele vai escrever a refeicao
        refeicao_nome = log.refeicao_nome

        # Convertando de datetime UTC para local
        local_dt = local_tz.normalize(log.data.astimezone(local_tz))

        row = []
        row.append(local_dt.strftime("%d/%m/%Y %H:%M:%S"))
        for i in range(0, 6):
            if refeicao_index[refeicao_nome] == i:
                row.append(log.descricao_refeicao)
            else:
                row.append("")

        writer.writerow(row)
        # writer.writerow([
        #     smart_str(local_dt.strftime("%d/%m/%Y %H:%M:%S")),
        #     smart_str(log.descricao_refeicao),
        #     smart_str(local_dt.strftime("%d/%m/%Y %H:%M:%S")),
        # ])
    return response

# def export_csv_refeicao_todos(request):

# 	for participante in Participante.objects.all():
# 		participanteName = participante.nome

# 		# Pegando


def getfiles(request):
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    filenames = ["/tmp/file1.txt", "/tmp/file2.txt"]

    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_subdir = "somefiles"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

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
