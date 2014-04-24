from django.shortcuts import render_to_response

def apply(request):
	if request.method=='GET':
		return render_to_response("apply.html",{})
	elif request.method=='POST':
		pass
