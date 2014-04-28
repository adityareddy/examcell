from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from student.models import Student, Applications
from django.forms.models import ModelForm
from home.models import Notification
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def apply(request):
	if request.user.groups.values_list('name')[0][0] != 'Student':
		return HttpResponseRedirect("/")
	student = None
	if request.method=='GET':
		#try:
			student = Student.objects.get(user=request.user)
			applications = Applications.objects.filter(student__user=request.user)
			notifications=Notification.objects.filter(dept=request.user.student.branch).exclude(applications=applications)
			c={'user':request.user,'notifications':notifications}
			return render_to_response("apply.html",c)
		#except:
		#	return HttpResponseRedirect("/student/fillprofile/")

	elif request.method=='POST':
		app = Applications()
		app.student = Student.objects.get(user=request.user)
		app.notification = Notification.objects.get(id=int(request.POST.get('notification')))
		app.verified=False
		app.save()
		return HttpResponse("applied")
		

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