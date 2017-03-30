from django.contrib import admin
from .models import (Log_Peso, Log_Refeicao, Participante)

# SENHA DO ADMIN SUPERUSER growboteleve

# Register your models here.
admin.site.register(Log_Refeicao)
admin.site.register(Log_Peso)
admin.site.register(Participante)
