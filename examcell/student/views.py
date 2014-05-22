from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from student.models import Student, Applications
from django.forms.models import ModelForm
from home.models import Notification
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from reportlab.pdfgen import canvas


@csrf_exempt
@login_required
def apply(request):
	if request.user.groups.values_list('name')[0][0] != 'Student':
		return HttpResponseRedirect("/")
	student = None
	if request.method=='GET':
		try:
			student = Student.objects.get(user=request.user)
			applications = Applications.objects.filter(student__user=request.user)
			notifications=Notification.objects.filter(dept=request.user.student.branch).exclude(applications=applications)
			c={'user':request.user,'notifications':notifications,'applications':applications}
			return render_to_response("apply.html",c)
		except:
			return HttpResponseRedirect("/student/fillprofile/")

	elif request.method=='POST':
		app = Applications()
		app.student = Student.objects.get(user=request.user)
		app.notification = Notification.objects.get(id=int(request.POST.get('notification')))
		app.verified=False
		app.save()
		return HttpResponse("")
		

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

@login_required
def hallticket(request):
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
	p = canvas.Canvas(response)
	p.rect(10, 10, 570, 810, stroke=1, fill=0)
	p.showPage()
	p.save()
	return response


@login_required
def challan(request):
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
	application = request.GET.get('application')
	app = Applications.objects.get(id=int(application))
	p = canvas.Canvas(response)
	p.rect(10, 10, 570, 810, stroke=1, fill=0)
	
	p.drawString(60,740,"Challan No:"+str(application))
	p.drawString(450,740,"Date:")
	
	p.setFont('Times-Bold',48)
	p.drawString(100, 780, "Syndicate Bank.")
	p.line(100, 775, 430, 775)
	
	p.setFont('Times-Bold',20)
	p.drawString(50,680,"Roll No:")
	p.drawString(135,682,request.user.username)
	p.line(130, 680, 300, 680)
	
	p.drawString(50,640,"Program:")
	p.line(135, 640, 300, 640)
	p.drawString(135,642,request.user.student.branch)
	
	p.drawString(50,600,"Branch:")
	p.line(125, 600, 300, 600)
	p.drawString(155,602,request.user.student.branch)
	
	p.drawString(50,560,"Year:")
	p.line(105, 560, 300, 560)
	p.drawString(135,562,"1")
	
	p.drawString(50,520,"Sem:")
	p.line(100, 520, 300, 520)
	p.drawString(130,522,str(request.user.student.semester))
	
	p.setFont('Times-BoldItalic',26)
	p.drawString(50,460,"Fees:")
	p.line(105, 460, 300, 460)
	p.drawString(125,460,str(app.notification.amount)+"/-")
	
	p.drawString(50,420,"Fine:")
	p.line(105, 420, 300, 420)
	p.drawString(125,420,str(request.GET.get('fine','0.0'))+"/-")

	p.setFont('Times-BoldItalic',26)
	p.drawString(50,100,"Signature")
	p.drawString(460,100,"Signature")
	p.setFont('Times-BoldItalic',16)
	p.drawString(60,120,"Clerk")
	p.drawString(480,120,"Student")
	
	p.showPage()
	p.save()
	return response