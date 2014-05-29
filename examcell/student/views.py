from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from student.models import Student, Applications
from django.forms.models import ModelForm
from home.models import Notification
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from _ast import With
from department.models import Subject, Department


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
		amount = int(float(request.POST.get('amount',None)))
		print amount
		app = Applications()
		app.student = Student.objects.get(user=request.user)
		app.notification = Notification.objects.get(id=int(request.POST.get('notification')))
		app.verified=False
		app.paid=False
		if amount:
			app.amount=amount
		else:
			app.amount=app.notification.amount
		app.save()
		return HttpResponse("")
		

class StudentRegistrationForm(ModelForm):
	class Meta:
		model=Student


@csrf_exempt
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
			departments = Department.objects.all()
			c.update({'departments':departments})
			return render_to_response("fillprofile.html",c)
	
	if request.method=='POST':
		print request.user.id
		print request.POST
		form=StudentRegistrationForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/student/apply/')
		else:
			return HttpResponse(str(form.errors))


@csrf_exempt
def editprofile(request):
	if request.method=='GET':
			student = Student.objects.get(user=request.user)
			c={}
			c.update(csrf(request))
			c.update({'form':StudentRegistrationForm()})
			c.update({'user':request.user})
			c.update({'student':student})
			return render_to_response("editprofile.html",c)
	
	if request.method=='POST':
		print request.user.id
		print request.POST
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
	p.setPageSize(landscape(A4))
	
	hallticket = request.GET.get('hallticket')
	app = Applications.objects.get(id=hallticket)
	
	p.drawImage(app.student.photo.file.name,20*mm,100*mm,45*mm,60*mm)
	p.drawImage(app.student.sign.file.name,20*mm,80*mm,45*mm,20*mm)
	
	p.setFont('Times-Bold',18)
	p.drawCentredString(148*mm, 190*mm, "VELAGAPUDI RAMAKRISHNA")
	p.drawCentredString(148*mm, 180*mm, "SIDDHARTHA ENGINEERING COLLEGE")
	
	p.setFont('Times-Bold',14)
	p.drawString(80*mm,146*mm,"Name: "+app.student.first_name+' '+app.student.last_name)
	p.drawString(80*mm,136*mm,"Reg.No.: "+app.student.reg_id)
	p.drawString(80*mm,126*mm,"Name: "+app.student.branch)
	
	#Subject.objects.filter()
	
	dept = Department.objects.get(title=app.student.branch)
	
	subjects = Subject.objects.filter(semester=app.student.semester,department=dept)
	x=80
	p.drawString(80*mm,110*mm,"Subjects:")
	for i in subjects:
		p.rect(x*mm,85*mm,25*mm,10*mm,stroke=1,fill=0)
		p.rect(x*mm,95*mm,25*mm,10*mm,stroke=1,fill=0)
		p.drawString(x*mm,100*mm,i.code)
		x+=25
	
	p.drawImage("/home/ratanraj/Downloads/sign.jpg",200*mm,40*mm,40*mm,15*mm)
	p.drawCentredString(222*mm, 30*mm, "Signature of the Candidate")
	p.showPage()
	p.save()
	return response

def drawBox(p,x,owner,name,branch,rollno,amount,id):
	p.rect(x*mm,10*mm,85*mm,190*mm,stroke=1, fill=0)
	p.setFont('Times-Bold',13)
	p.drawCentredString((x+42)*mm,190*mm,"SYNDICATE BANK, VRSEC CAMPUS")
	p.setFont('Times-Bold',12)
	p.drawCentredString((x+42)*mm,180*mm,"KANURU, VIJAYAWADA - 520 007")
	p.drawCentredString((x+42)*mm,170*mm,owner+" COPY")
	p.drawCentredString((x+42)*mm,160*mm,"ORIGINAL")
	
	p.line(x*mm,158*mm,(x+85)*mm,158*mm)
	
	p.setFont('Times-Bold',8)
	p.drawCentredString((x+42)*mm,150*mm,"Paid to the credit of SB A/c.No.3367.220.20899")
	p.drawCentredString((x+42)*mm,145*mm,"of Principal, V.R. Siddhartha Engineering")
	p.drawCentredString((x+42)*mm,140*mm,"College, (Autonomous) VIJAYAWADA")
	
	p.line(x*mm,138*mm,(x+85)*mm,138*mm)
	
	p.setFont('Times-Bold',10)
	p.drawString((x+5)*mm,130*mm,"Name: "+name)
	p.drawString((x+5)*mm,125*mm,"Programme: "+branch)
	p.drawString((x+5)*mm,120*mm,"R.No: "+rollno)
	p.drawString((x+5)*mm,115*mm,"Challan Number: *** "+str(id)+" ***")
	
	p.line(x*mm,110*mm,(x+85)*mm,110*mm)
	
	p.setFont('Times-Bold',14)
	p.drawString((x+10)*mm,90*mm,"Amount: "+str(amount)+"/-")
	p.drawString((x+10)*mm,80*mm,"Late Fee: 0/-")
	p.drawString((x+10)*mm,70*mm,"Condonation Fee: 0/-")
	p.drawString((x+10)*mm,60*mm,"Total: "+(" "*20)+str(amount)+"/-")
	
	p.setFont('Times-Bold',10)
	p.drawCentredString((x+21)*mm,40*mm,"Cashier")
	p.drawCentredString((x+63)*mm,40*mm,"Cashier")

@login_required
def challan(request):
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
	application = request.GET.get('application')
	app = Applications.objects.get(id=int(application))
	p = canvas.Canvas(response)
	p.setPageSize(landscape(A4))

	#p.rect(10*mm,10*mm,85*mm,190*mm,stroke=1, fill=0)
	#p.rect(105*mm,10*mm,85*mm,190*mm,stroke=1, fill=0)
	#p.rect(200*mm,10*mm,85*mm,190*mm,stroke=1, fill=0)
	drawBox(p,10,"BANKER'S",app.student.first_name+' '+app.student.last_name,app.student.branch,app.student.reg_id,app.amount,app.id)
	drawBox(p,105,"COLLEGE",app.student.first_name+' '+app.student.last_name,app.student.branch,app.student.reg_id,app.amount,app.id)
	drawBox(p,200,"STUDENT'S",app.student.first_name+' '+app.student.last_name,app.student.branch,app.student.reg_id,app.amount,app.id)

	p.showPage()
	p.save()
	return response

# @login_required
# def challan_old(request):
# 	response = HttpResponse(content_type='application/pdf')
# 	response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
# 	application = request.GET.get('application')
# 	app = Applications.objects.get(id=int(application))
# 	p = canvas.Canvas(response)
# 	p.setPageSize(landscape(A4))
# 	p.rect(10, 10, 570, 810, stroke=1, fill=0)
# 	
# 	p.drawString(60,740,"Challan No:"+str(application))
# 	p.drawString(450,740,"Date:")
# 	
# 	p.setFont('Times-Bold',48)
# 	p.drawString(100, 780, "Syndicate Bank.")
# 	p.line(100, 775, 430, 775)
# 	
# 	p.setFont('Times-Bold',20)
# 	p.drawString(50,680,"Roll No:")
# 	p.drawString(135,682,request.user.username)
# 	p.line(130, 680, 300, 680)
# 	
# 	p.drawString(50,640,"Program:")
# 	p.line(135, 640, 300, 640)
# 	p.drawString(135,642,request.user.student.branch)
# 	
# 	p.drawString(50,600,"Branch:")
# 	p.line(125, 600, 300, 600)
# 	p.drawString(155,602,request.user.student.branch)
# 	
# 	p.drawString(50,560,"Year:")
# 	p.line(105, 560, 300, 560)
# 	p.drawString(135,562,"1")
# 	
# 	p.drawString(50,520,"Sem:")
# 	p.line(100, 520, 300, 520)
# 	p.drawString(130,522,str(request.user.student.semester))
# 	
# 	p.setFont('Times-BoldItalic',26)
# 	p.drawString(50,460,"Fees:")
# 	p.line(105, 460, 300, 460)
# 	p.drawString(125,460,str(app.notification.amount)+"/-")
# 	
# 	p.drawString(50,420,"Fine:")
# 	p.line(105, 420, 300, 420)
# 	p.drawString(125,420,str(request.GET.get('fine','0.0'))+"/-")
# 
# 	p.setFont('Times-BoldItalic',26)
# 	p.drawString(50,100,"Signature")
# 	p.drawString(460,100,"Signature")
# 	p.setFont('Times-BoldItalic',16)
# 	p.drawString(60,120,"Clerk")
# 	p.drawString(480,120,"Student")
# 	
# 	p.showPage()
# 	p.save()
# 	return response
