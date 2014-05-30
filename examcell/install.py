from django.contrib.auth.models import User, Group
from department.models import Subject, Department
from student.models import Student


def install_groups():
    exam = Group()
    exam.name='ExamCell'
    exam.save()

    student = Group()
    student.name='Student'
    student.save()
    
    dept = Group()
    dept.name='Department'
    dept.save()
    


def install_admin(name):
    admin = User()
    admin.username = name
    admin.set_password(name)
    admin.is_staff=True
    admin.is_active=True
    admin.is_superuser=True
    
    g = Group.objects.get(name='ExamCell')
    admin.save()
    g.user_set.add(admin)
    g.save()


def add_department(title):
    dept = Department()
    dept.title = title
    
    deptUser = User()
    deptUser.username = title
    deptUser.set_password(title)
    deptUser.is_staff=True
    deptUser.is_active=True
    
    dept_group = Group.objects.get(name='Department')
    deptUser.save()
    dept.user = deptUser
    dept.save()
    dept_group.user_set.add(deptUser)

    

    
def install_departments():
    departments = [
                   "MCA",
                   "MBA",
                   "IT",
                   "CSE",
                   "ECE",
                   "EIE",
                   "CE",
                   "ME"
                   ]

    for i in departments:
        add_department(i)

def install_sample_data():
    subjects = [
                {'code':'MCA1001','title':'Programming In C','tol':'T','o':False},
                {'code':'MCA1002','title':'Computer Organization','tol':'T','o':False},
                {'code':'MCA1003','title':'Discreet Mathemetics','tol':'T','o':False},
                {'code':'MCA1004','title':'Probability and Statistics','tol':'T','o':False},
                {'code':'MCA1005','title':'English','tol':'T','o':False},
                {'code':'MCA1051','title':'C Lab','tol':'L','o':False},
                {'code':'MCA1052','title':'CO Lab','tol':'L','o':False}
                ]
    mca = Department.objects.get(title='MCA')
    for i in subjects:
        s = Subject()
        s.code = i['code']
        s.title = i['title']
        s.department = mca
        s.theoryOrLab = i['tol']
        s.optional = i['o']
        s.semester = 1 
        s.save()

def add_student(name):
    student = User()
    student.username = name
    student.set_password(name)
    student.is_staff=False
    student.is_active=True
    student.detained = False
    student.condonation = 0
    student.save()
    student_group = Group.objects.get(name='Student')
    student_group.user_set.add(student)

    

def install_sample_students():
    numbers = ['118w1f'+str(i).zfill(4) for i in range(1,61)]
    for i in numbers:
        add_student(i)

def install_all():
    print "installing groups [",
    install_groups()
    print "done]"
    print "installing admin [",
    install_admin('ratanraj')
    print "done]"
    print "installing departments [",
    install_departments()
    print "done]"
    print "installing sample data [",
    install_sample_data()
    print "done]"
    print "installing students [",
    install_sample_students()
    print "done]"