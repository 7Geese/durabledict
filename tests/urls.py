from __future__ import absolute_import, division, print_function

from django.conf.urls.defaults import *


def dummy_view(request):
    from django.http import HttpResponse
    return HttpResponse()

urlpatterns = patterns('',
    url(r'^$', dummy_view, name='durabledict-home'),
)
