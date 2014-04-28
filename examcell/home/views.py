from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from student.models import Student, Applications
from django.http.response import HttpResponseRedirect, HttpResponse
from django.forms.models import ModelForm
from django.contrib.auth.models import Group, User
from django import forms
from home.models import Notification
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def home(request):
	group = request.user.groups.values_list('name')[0][0]
	if group == 'Student':
		return render_to_response("StudentHome.html",{'user':request.user,'group':group})
	elif group == 'Department':
		return HttpResponseRedirect("/department/")
	elif group == 'ExamCell':
		return HttpResponseRedirect('/notify/')
	else:
		return HttpResponse('Invalid User')



@csrf_exempt
@login_required
def verification(request):
	if request.method=='GET':
		app = Applications.objects.filter(verified=False)
		return render_to_response('verification.html',{'user':request.user,'applications':app})
	elif request.method=='POST':
		obj = json.loads(request.POST.get('data'))
		
		def verify(id):
			a = Applications.objects.get(id=id)
			a.verified = True
			a.save()
		count=0
		for i in obj:
			verify(i)
			count+=1
		return HttpResponse("Verified "+str(count)+" records")


@login_required
def notify(request):
	group = request.user.groups.values_list('name')[0][0]
	department_users = User.objects.filter(groups=Group.objects.get(name='Department'))
	departments = [i.department for i in department_users]
	
	notifications = Notification.objects.all()
	c={'user':request.user,'departments':departments,'notifications':notifications}
	c.update(csrf(request))
	if request.method == 'POST':
		class NotificationForm(ModelForm):
			class Meta:
				model = Notification
		
		form = NotificationForm(request.POST)
		if form.is_valid():
			form.save()
			print "done"
		
		c.update({'group':group})
		c.update({'departments':departments})
		c.update({'errors':form.errors})
		c.update(csrf(request))
		Notification.objects.filter(lastdate__lt=datetime.utcnow().date()).delete()
		return render_to_response("ExamCellHome.html",c)
	else:
		Notification.objects.filter(lastdate__lt=datetime.utcnow().date()).delete()
		return render_to_response("ExamCellHome.html",c)