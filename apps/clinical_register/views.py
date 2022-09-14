from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect


@login_required(login_url="/login/")
def clinical_register_view(request):
    return render(request, "clinical_register/image-classification.html")
