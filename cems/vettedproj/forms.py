from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from slugify import slugify

from .services import create_company, create_employee
from .models import Company, Employee

alphabets_only = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabets are allowed.')


class RegisterationForm(forms.Form):
	first_name = forms.CharField(max_length=50, required=True, validators=[alphabets_only], help_text='First name')
	last_name = forms.CharField(max_length=50, required=True, validators=[alphabets_only], help_text='Last name')
	company_name = forms.CharField(max_length=50, required=True, help_text='Company Name')
	gender = forms.CharField(max_length=1, required=True, help_text='gender of user')
	email = forms.EmailField(max_length=254, required=True)
	dob = forms.DateField(required=True, help_text='Required. Format: YYYY-MM-DD')
	password = forms.CharField(max_length=30, required=True, help_text='password')

	def clean_company_name(self):
		name = self.cleaned_data['company_name']
		slug = slugify(name)
		try:
			company = Company.objects.get(slug=slug)
		except Company.DoesNotExist:
			company = None

		if company:
			raise ValidationError("Company with this name already exist.")
		else:
			return name

	def clean_gender(self):
		gender = self.cleaned_data['gender'].lower()
		if gender in ['m', 'f']:
			return gender
		else:
			raise ValidationError("Invalid gender.")

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		else:
			raise ValidationError('user email already exist')


	def save(self):
		user = User.objects.create(
					username = self.cleaned_data.get('email'),
					first_name = self.cleaned_data.get('first_name'),
					last_name = self.cleaned_data.get('last_name'),
					email = self.cleaned_data.get('email'),
				)

		user.set_password(self.cleaned_data.get('password'))
		user.save()

		company = create_company(name = self.cleaned_data.get('company_name'))
		employee = create_employee(
						user = user,
						company=company,
						gender = self.cleaned_data.get('gender'),
						dob = self.cleaned_data.get('dob')
					)
		employee.promote_to_admin()

		return employee


class EmployeeRegisterationForm(forms.Form):
	first_name = forms.CharField(max_length=50, required=True, validators=[alphabets_only], help_text='First name')
	last_name = forms.CharField(max_length=50, required=True, validators=[alphabets_only], help_text='Last name')
	gender = forms.CharField(max_length=1, required=True, help_text='gender of user')
	email = forms.EmailField(max_length=254, required=True)
	dob = forms.DateField(required=True, help_text='Required. Format: YYYY-MM-DD')
	password = forms.CharField(max_length=30, required=True, help_text='password')

	def clean_company_name(self):
		name = self.cleaned_data['company_name']
		slug = slugify(name)
		try:
			company = Company.objects.get(slug=slug)
		except Company.DoesNotExist:
			company = None

		if company:
			raise ValidationError("Company with this name already exist.")
		else:
			return name

	def clean_gender(self):
		gender = self.cleaned_data['gender'].lower()
		if gender in ['m', 'f']:
			return gender
		else:
			raise ValidationError("Invalid gender.")

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		else:
			raise ValidationError('user email already exist')


	def save(self, company):
		user = User.objects.create(
					username = self.cleaned_data.get('email'),
					first_name = self.cleaned_data.get('first_name'),
					last_name = self.cleaned_data.get('last_name'),
					email = self.cleaned_data.get('email'),
				)

		user.set_password(self.cleaned_data.get('password'))
		user.save()

		employee = create_employee(
						user = user,
						company=company,
						gender = self.cleaned_data.get('gender'),
						dob = self.cleaned_data.get('dob')
					)

		return employee

