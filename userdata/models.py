from django.db import models

class Account_Risk(models.Model):
	account_id = models.IntegerField(default=0)
	account_name = models.CharField(max_length=200)
	customer_name = models.CharField(max_length=200)
	account_risk = models.CharField(max_length=3000)

class Account(models.Model):
	account_id = models.IntegerField(default=0)
	account_child = models.IntegerField(default=0)
	potential = models.CharField(max_length=200)
	pipeline = models.CharField(max_length=200)
	stage = models.CharField(max_length=200)
