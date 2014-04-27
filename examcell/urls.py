from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'examcell.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'home.views.home', name='home'),
    url(r'^apply$', 'student.views.apply', name='apply'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', 'home.views.profile',name='profile'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page':'/'}),
)
