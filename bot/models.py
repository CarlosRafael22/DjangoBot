from django.db import models

# Create your models here.
# class Participante(models.Model):
# 	telegram_id 
class Log_Peso(models.Model):
	peso = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	data = models.DateTimeField()
	# participante = models.OneToOneField(Paciente)
	# history = HistoricalRecords()


	# for log in log1.history.all():
	# 	type(log.history_date)
	# 	print(log.history_date - timedelta(hours=3) )
	#  TEM QUE SUBTRAIR 3 HORAS PARA DAR A HORA DAQUI JA QUE ELE PEGA A HORA DE GREENWICH

	def __str__(self):
		# peso_mais_recente = str(self.history.most_recent().peso)
		# response = self.participante.perfil.user.username + " " + peso_mais_recente
		response = str(self.peso)
		return response

	# def save(self, *args, **kwargs):
	# 	if not self.id:
	# 		self.data = timezone.localtime(timezone.now())

	# 	# Salvando o peso mais recente no Paciente
	# 	# import pdb;
	# 	# pdb.set_trace();
	# 	# partic = Paciente.objects.get(id=self.participante.id)
	# 	# partic.peso = self.history.most_recent().peso
	# 	# partic.save()

	# 	return super(Log_Peso, self).save(*args, **kwargs)