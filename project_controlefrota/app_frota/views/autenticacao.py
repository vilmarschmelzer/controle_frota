# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext

def login(request):
    render_to_response("index.html", context_instance=RequestContext(request))
