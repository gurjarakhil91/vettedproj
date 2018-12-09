from django.db import models
from django.contrib.auth.models import User, Permission

import json


class Company(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	is_active = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def activate(self):
		if not self.is_active:
			self.is_active = True
			self.save()

	def deactivate(self):
		if self.is_active:
			self.is_active = False
			self.save()

"""
We can use django mptt if we want to maintain heirarchy
"""
class Employee(models.Model):
	GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, related_name='employee', on_delete=models.CASCADE)
	company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	dob = models.DateTimeField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		permissions = (
            ('is_admin', 'Can add and remove employees'),
        )

	@property
	def is_admin(self):
		return True if self.get_admin() == self.user else False

	@property
	def first_name(self):
		return self.user.first_name

	@property
	def last_name(self):
		return self.user.last_name

	@property
	def email(self):
		return self.user.email

	@property
	def is_admin(self):
		perm = Permission.objects.get(codename='is_admin')
		return True if perm in self.user.user_permissions.all() else False

	def activate(self):
		if not self.is_active:
			self.is_active = True
			self.save()

	def deactivate(self):
		if self.is_active:
			self.is_active = False
			self.save()

	def to_dict(self):
		return {
			'id': self.id,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'email': self.email,
			'gender': 'male' if self.gender == 'm' else 'female',
			'dob': self.dob.strftime('%d-%m-%Y'),
			'company': self.company.name,
			'is_active': self.is_active
		}

	def to_json(self):
		return json.dumps(self.to_dict())

	def promote_to_admin(self):
		perm = Permission.objects.get(codename='is_admin')
		self.user.user_permissions.add(perm)
		return True
