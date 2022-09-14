# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models

ID_CHOICES = [
        ('CC', 'CC'),
        ('TI', 'TI'),
        ('CE', 'CE')
    ]

# Create your models here.
class Patient(models.Model):
    id= models.AutoField(primary_key=True)
    active_flg_patient=models.BooleanField(null=True,blank=True)    
    type_id = models.CharField(max_length=6, choices=ID_CHOICES, default='CC')
    idd = models.CharField(max_length=120,blank=True)
    age=models.CharField(max_length=6,blank=True)    
    name=models.TextField(null=True,blank=True)
    lastname=models.TextField(null=True,blank=True)
    phone=models.TextField(null=True,blank=True)
    gender=models.CharField(max_length=255,blank=True)    
    ethnic=models.CharField(max_length=255,blank=True)
    user_edit = models.TextField(null=True,blank=True)
    day = models.DateField()



   
class DiagnosisProc(models.Model):
  idd = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  proced = models.CharField(max_length=255)

class IndProc(models.Model):
  idd = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  proced = models.CharField(max_length=255)

class Procedures(models.Model):
  idd = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  flg_stat= models.CharField(max_length=255)
  flg_anot= models.CharField(max_length=255)

class AnnotOpt(models.Model):
  idd = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  proced = models.CharField(max_length=255)