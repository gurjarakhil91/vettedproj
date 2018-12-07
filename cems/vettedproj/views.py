from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.template import Template, Context
from django.template.loader import get_template
from django.db import transaction
import json

from .forms import RegisterationForm, EmployeeRegisterationForm
from .models import Company, Employee
from .decorators import user_is_employee, user_is_admin

@user_is_employee
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class Register(View):

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('view_profile')
		return HttpResponse(render(request, 'register.html'))

	def post(self, request, *args, **kwargs):
		form = RegisterationForm(request.POST)
		if form.is_valid():
			try:
				with transaction.atomic():
					form.save()
			except:
				return HttpResponse('Some error occured')
			else:
				username = form.cleaned_data.get('email')
				raw_password = form.cleaned_data.get('password')
				user = authenticate(username=username, password=raw_password)
				login(request, user)
				return HttpResponse("Company registered")
		else:
			return HttpResponse(json.dumps(form.errors))


class Login(View):

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('view_profile')
		return HttpResponse(render(request, 'login.html'))

	def post(self, request, *args, **kwargs):
		username = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			return redirect('view_profile')
		else:
			return HttpResponse('Invalid Credentials')


class CompanyView(View):

	@method_decorator(login_required(login_url='login'))
	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def get(self, request, *args, **kwargs):
		#return HttpResponse(render(request, 'list.html'))
		filter = request.GET.get('filter', None)
		if filter == 'active':
			coms = Company.objects.filter(is_active=True)
		elif filter == 'inactive':
			coms = Company.objects.filter(is_active=False)
		else:
			coms = Company.objects.all()
		data = {}
		for com in coms:
			data[com.id] = {'id': com.id, 'name': com.name, 'is_active': com.is_active}

		return HttpResponse(json.dumps(data))

	@method_decorator(login_required(login_url='login'))
	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def post(self, request, *args, **kwargs):
		com_id = request.POST.get('id')
		action = request.POST.get('action')

		try:
			company = Company.objects.get(id=com_id)
		except Company.DoesNotExist:
			return HttpResponse('Company not found')
		else:
			if action == 'approve':
				company.activate()
				return HttpResponse('Company approved')
			elif action == 'remove':
				company.deactivate()
				return HttpResponse('Company removed')


class EmployeeView(View):

	@method_decorator(login_required(login_url='login'))
	@method_decorator(user_is_admin)
	def get(self, request, *args, **kwargs):
		filter = request.GET.get('filter', None)
		if filter == 'active':
			emps = request.user.employee.company.employees.filter(is_active=True)
		elif filter == 'inactive':
			emps = request.user.employee.company.employees.filter(is_active=False)
		else:
			emps = request.user.employee.company.employees.all()

		data = {}
		for emp in emps:
			data[emp.id] = {'id': emp.id, 'name': emp.first_name, 'is_active': emp.is_active}

		return HttpResponse(json.dumps(data))
		
		return HttpResponse(render(request, 'list.html'))
		return HttpResponse(render(request, 'employee_register.html'))

	@method_decorator(login_required(login_url='login'))
	@method_decorator(user_is_admin)
	def post(self, request, *args, **kwargs):
		emp_id = request.POST.get('id', None)
		if emp_id:
			action = request.POST.get('action')

			employee = Employee.objects.filter(id=emp_id, company=request.user.employee.company).last()

			if employee:
				if action == 'approve':
					employee.activate()
					return HttpResponse('Employee approved')
				elif action == 'remove':
					employee.deactivate()
					return HttpResponse('Employee removed')
			else:
				HttpResponse('Employee not found')
		else:
			form = EmployeeRegisterationForm(request.POST)
			if form.is_valid():
				try:
					with transaction.atomic():
						form.save(request.user.employee.company)
				except:
					return HttpResponse('Some error occured')
				else:
					return HttpResponse("Employee registered")
			else:
				return HttpResponse(json.dumps(form.errors))

	def put(self, request, *args, **kwargs):
		emp_id = request.POST.get('id', None)
		action = request.POST.get('action')

		employee = Employee.objects.filter(id=com_id, company=request.user.employee.company).last()

		if employee:
			if action == 'approve':
				company.activate()
				return HttpResponse('Company approved')
			elif action == 'remove':
				company.deactivate()
				return HttpResponse('Company removed')
		else:
			HttpResponse('Employee not found')


class ProfileView(View):

	@method_decorator(login_required(login_url='login'))
	@method_decorator(user_is_employee)
	def get(self, request, *args, **kwargs):
		return HttpResponse(request.user.employee.to_json())


class Logout(View):

	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponse('User logged out')

