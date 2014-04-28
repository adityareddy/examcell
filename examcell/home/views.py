from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from student.models import Student
from django.http.response import HttpResponseRedirect, HttpResponse
from django.forms.models import ModelForm
from django.contrib.auth.models import Group, User

@login_required
def home(request):
	group = request.user.groups.values_list('name')[0][0]
	if group == 'Student':
		return render_to_response("StudentHome.html",{'user':request.user,'group':group})
	elif group == 'Department':
		return HttpResponseRedirect("/department/")
	elif group == 'ExamCell':
		department_users = User.objects.filter(groups=Group.objects.get(name='Department'))
		departments = [i.department for i in department_users]
		return render_to_response("ExamCellHome.html",{'user':request.user,'group':group,'departments':departments})
	else:
		return HttpResponse('Invalid User')



def register(request):
	if request.method=='GET':
		c={}
		c.update(csrf(request))
		c.update({'form':StudentRegistrationForm()})
		return render_to_response("registration/register.html",c)
	
	if request.method=='POST':
		form=StudentRegistrationForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/student/apply/')
		
	