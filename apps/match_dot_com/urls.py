from django.conf.urls import url, include
from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login$', login, name='login'),
    url(r'^register$', register, name='register'),
    url(r'^survey$', survey, name='survey'),
    url(r'^logout$', logout, name='logout'),
<<<<<<< HEAD
    url(r'^matchmsg$', messages, name='matchmsg'),
=======
    url(r'^messages$', matchmsg, name='messages'),
>>>>>>> 65b964c9a501c78e06eb7f6778183c29f2742419
    url(r'^messenger/(?P<id>\d+)$', messenger, name='messenger'),
    url(r'^user/(?P<id>\d+)$', user, name='user'),
]
