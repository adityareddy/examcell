from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from student.models import Student
from django.http.response import HttpResponseRedirect
from django.forms.models import ModelForm

@login_required
def home(request):
	return render_to_response("home.html",{})

class StudentRegistrationForm(ModelForm):
	class Meta:
		model=Student


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
			return HttpResponseRedirect('/apply/')
		
	