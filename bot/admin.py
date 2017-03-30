from django.contrib import admin
from .models import (Log_Peso, Log_Refeicao, Participante)
from simple_history.admin import SimpleHistoryAdmin

# SENHA DO ADMIN SUPERUSER growboteleve

# Register your models here.
admin.site.register(Log_Refeicao)
admin.site.register(Log_Peso, SimpleHistoryAdmin)
admin.site.register(Participante)
