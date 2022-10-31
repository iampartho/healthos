from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class Company(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class User(AbstractUser):
	PLANS_TYPE = (
		('Bronze', 'Globalnet Bronze - 500 BDT // month, 12 months'),
		('Silver', 'Globalnet Silver - 750 BDT / month, 12 months'),
		('Gold', 'Globalnet Gold - 1500 BDT / month, no contract - You can cancel at any time')
		)
	name = models.CharField(max_length=200)
	email = models.EmailField(null=True, blank=True)
	plan = models.CharField(
		max_length=200, choices=PLANS_TYPE, null=True, blank=True)
	company = models.ForeignKey(
		Company, on_delete=models.CASCADE, null=True)
	primary_phone_number = models.CharField(max_length=15, unique=True)
	secondary_number_field = models.TextField(null=True, blank=True)
	payment_done = models.BooleanField(default=False)
	available_balance = models.BigIntegerField(default=2000)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	USERNAME_FIELD = 'primary_phone_number'
	REQUIRED_FIELDS = ['name', 'email', 'username']

	@property
	def paiduser(self):
		if self.payment_done and now().month == self.updated.month:
			return True
		else:
			return False

	def __str__(self):
		return self.name
