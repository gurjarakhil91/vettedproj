from django.contrib.auth.models import User
from slugify import slugify

from .models import Company, Employee

def create_company(name, is_active=False):
	slug = slugify(name)
	company = Company.objects.create(
					name = name,
					slug = slug,
					is_active=is_active
				)

	return company


def create_employee(user, company, gender, dob):
	try:
		employee = Employee.objects.get(user=user)
	except Employee.DoesNotExist:
		employee = Employee.objects.create(
						user = user,
						company = company,
						gender = gender,
						dob=dob
					)
	else:
		employee.company = company
		employee.gender = gender
		employee.dob = dob
	return employee
