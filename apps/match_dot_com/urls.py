from django.conf.urls import url, include
from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login$', login, name='login'),
    url(r'^register$', register, name='register'),
    url(r'^survey$', survey, name='survey'),
    url(r'^survey_seeking$', survey_seeking, name='survey_seeking'),
    url(r'^seeking_entry$', seeking_entry, name='seeking_entry'),
    url(r'^logout$', logout, name='logout'),
    url(r'^messages$', matchmsg, name='messages'),
    url(r'^messenger/(?P<id>\d+)$', messenger, name='messenger'),
    url(r'^user/(?P<id>\d+)$', user, name='user'),
    url(r'^upload$', upload_pic, name='upload_pic'),
    url(r'^user/(?P<id>\d+)/edit$', editprofile, name='profileeditor'),
    url(r'^user/(?P<id>\d+)/seeking$', editseeking, name='editseeking'),
    url(r'^matchsort$', matchsort, name='matchsort'),
    url(r'^wink/(?P<id>\d+)$', wink, name='wink'),
    url(r'^winks$', winks, name='winks'),
    url(r'^regional$', regional, name='regional'),
    url(r'^gallery$', upload_gallery, name='gallery'),
    url(r'^user/(?P<id>\d+)/gallery', gallery, name='galleryviewer'),
    url(r'^user/(?P<id>\d+)/delete$', delete, name='delete'),
]
