from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from department.models import Department, Subject
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import ModelForm
import json
from home.models import Notification
from student.models import Student,Applications
from django.contrib.auth.models import User


@login_required
def home(request):
    notifications=Notification.objects.filter(dept='MCA')
    return render_to_response('DepartmentHome.html',{'user':request.user,'notifications':notifications,'department':request.user.username})

@csrf_exempt
@login_required
def subjects(request):
    class SubjectForm(ModelForm):
        class Meta:
            model=Subject

    if request.method=="GET":
        sem = request.GET.get('sem',False)
        dept = request.GET.get('dept',False)
        print sem,dept
        if sem and dept:
            subjects=Subject.objects.filter(semester=sem,department=dept)
            s=''
            for subject in subjects:
                s=s+"<input type='checkbox' name='supply-subj' class='supply-subjects'><label>"+subject.code+"</label>"
            return HttpResponse(s)
		
        department = Department.objects.get(user=request.user)
        subjects = Subject.objects.filter(department=department.id)
        return render_to_response('subjects.html',{'department':department,'subjects':subjects})
    else:
        form = SubjectForm(request.POST)
        if form.is_valid():
            print form.save()
        else:
            print form.errors
            print "invalid"
            
    return HttpResponse("Test")


def subjectslist(request):
    l=[]
    department = Department.objects.get(user=request.user)
    for subject in Subject.objects.filter(department=department.id):
        l.append({
                  'code':subject.code,
                  'semester':subject.semester,
                  'title':subject.title,
                  'theoryOrLab':subject.theoryOrLab,
                  'optional':subject.optional
                  })

    return HttpResponse(json.dumps(l))


@csrf_exempt
@login_required
def detained(request):
    if request.method=='POST':
        x=request.POST.get('id',None)
        print x
        student = Student.objects.get(reg_id=x)
        if request.POST.get('remove',False):
            student.detained = False
            student.save()
            return HttpResponse('Removed')
        student.detained=True
        student.save()
        print student.first_name
        return HttpResponse(str(x)+" Detained!")
    department = Department.objects.get(user=request.user)
    students = Student.objects.filter(branch=department.title,detained=False)
    detainedstudents = Student.objects.filter(branch=department.title,detained=True)
    print students
    #students = User.objects.filter(username__istartswith='118')
    return render_to_response('detained.html',{'students':students,'detainedstudents':detainedstudents})

@csrf_exempt
@login_required
def condonation(request):
    if request.method == 'POST':
        x=request.POST.get('id',None)
        amt = request.POST.get('amount',0)
        student = Student.objects.get(reg_id=x)
        student.condonation=int(amt)
        student.save()
        return HttpResponse('Condonation of '+amt+' for '+str(x)+' is imposed!')
        
    department = Department.objects.get(user=request.user)
    students = Student.objects.filter(branch=department.title,condonation=0)
    condonationstudents = Student.objects.filter(branch=department.title,condonation__gt=0)
    return render_to_response('condonation.html',{'students':students,'condonationstudents':condonationstudents})

