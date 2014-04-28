from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from department.models import Department, Subject
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import ModelForm
import json
@login_required
def home(request):
    return render_to_response('DepartmentHome.html',{'user':request.user})


@csrf_exempt
@login_required
def subjects(request):
    class SubjectForm(ModelForm):
        class Meta:
            model=Subject

    if request.method=="GET":
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


@login_required
def detained(request):
    return render_to_response('detained.html',{})

@login_required
def condonation(request):
    return render_to_response('condonation.html',{})

