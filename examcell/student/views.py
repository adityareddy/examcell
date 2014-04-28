from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from student.models import Student
from django.core.context_processors import csrf
from django.forms.models import ModelForm

@login_required
def apply(request):
	if request.user.groups.values_list('name')[0][0] != 'Student':
		return HttpResponseRedirect("/")
	student = None
	if request.method=='GET':
		try:
			student = Student.objects.get(user=request.user)
			return render_to_response("apply.html",{'user':request.user})
		except:
			return HttpResponseRedirect("/student/fillprofile/")
	elif request.method=='POST':
		pass

class StudentRegistrationForm(ModelForm):
	class Meta:
		model=Student


def fillprofile(request):
	if request.method=='GET':
		try:
			student = Student.objects.get(user=request.user)
			return HttpResponseRedirect("/student/apply/")
		except:			
			c={}
			c.update(csrf(request))
			c.update({'form':StudentRegistrationForm()})
			c.update({'user':request.user})
			return render_to_response("fillprofile.html",c)
	
	if request.method=='POST':
		form=StudentRegistrationForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/student/apply/')
		else:
			return HttpResponse(str(form.errors))