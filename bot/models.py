from django.db import models
from simple_history.models import HistoricalRecords
from django.utils import timezone

# Create your models here.
class Participante(models.Model):
	telegram_chat_id = models.CharField(max_length=50)
	nome = models.CharField(max_length=50)

	def __str__(self):
		return self.nome

class Log_Peso(models.Model):
	peso = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	data = models.DateTimeField()
	participante = models.ForeignKey(Participante)

	def __str__(self):
		response = self.participante.nome + " " + str(self.peso)
		return response

	def save(self, *args, **kwargs):
		if not self.id:
			self.data = timezone.localtime(timezone.now())

		return super(Log_Peso, self).save(*args, **kwargs)

# class Log_Peso(models.Model):
# 	peso = models.DecimalField(max_digits=5, decimal_places=2, null=True)
# 	data = models.DateTimeField()
# 	participante = models.ForeignKey(Participante)
# 	history = HistoricalRecords()


# 	# for log in log1.history.all():
# 	# 	type(log.history_date)
# 	# 	print(log.history_date - timedelta(hours=3) )
# 	#  TEM QUE SUBTRAIR 3 HORAS PARA DAR A HORA DAQUI JA QUE ELE PEGA A HORA DE GREENWICH

# 	def __str__(self):
# 		peso_mais_recente = str(self.history.most_recent().peso)
# 		response = self.participante.nome + " " + peso_mais_recente
# 		return response

# 	def save(self, *args, **kwargs):
# 		if not self.id:
# 			self.data = timezone.localtime(timezone.now())

# 		return super(Log_Peso, self).save(*args, **kwargs)

class Log_Refeicao(models.Model):
	refeicao_nome = models.CharField(max_length=100, null = True)
	descricao_refeicao = models.CharField(max_length=500)
	data = models.DateTimeField()
	participante = models.ForeignKey(Participante)
	# person = models.ForeignKey(Person, related_name='logs_meal')

	def __str__(self):
		return self.descricao_refeicao