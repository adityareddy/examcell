from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from student.models import Applications

# Create your views here.

@csrf_exempt
def home(request):
    params = {'user':request.user}
    if request.method=='POST':
        appid = request.POST.get('challan')
        app = Applications.objects.get(id=appid)
        print app.paid
        if app.paid:
            params.update({'paid':True})
        else:
            params.update({'application':app})
    return render_to_response("BankerHome.html",params)

@csrf_exempt
def paid(request):
    if request.method=='POST':
        appid=request.POST.get('challan')
        app = Applications.objects.get(id=appid)
        app.paid=True
        app.save()
    return HttpResponseRedirect("/bank/")