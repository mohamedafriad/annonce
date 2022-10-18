from django.db import models

class Message(models.Model):
	nom = models.CharField("Nom", max_length=500)
	email = models.EmailField("Email")
	message = models.CharField("Message", max_length=5000)

	def __str__(self):
		return self.nom