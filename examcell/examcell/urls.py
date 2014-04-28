from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'examcell.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', 'home.views.home', name='home'),
    url(r'^student/apply/$', 'student.views.apply', name='apply'),
    url(r'^student/fillprofile/$', 'student.views.fillprofile', name='fillprofile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page':'/accounts/login/'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page':'/accounts/login/'}),
    url(r'^accounts/register/$','home.views.register',name='register'),
    url(r'^department/$','department.views.home',name='department.home'),
    url(r'^department/subjects/$','department.views.subjects',name='department.subjects'),
    url(r'^department/subjects/list/$','department.views.subjectslist',name='department.subjects.list'),
    url(r'^department/detained/$','department.views.detained',name='department.detained'),
    url(r'^department/condonation/$','department.views.condonation',name='department.condonation'),
)
