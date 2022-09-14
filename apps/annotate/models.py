from django.db import models


class Annotation(models.Model):
    root_ann = models.TextField(null=True,blank=True)
    root_png= models.TextField(null=True,blank=True)
    name_video = models.TextField(null=True,blank=True)
    frame = models.CharField(max_length=255,null=True,blank=True) 
    
    day_ann = models.DateField(null=True,blank=True)
    
    id_pateint = models.CharField(max_length=255,null=True,blank=True)    
    id_file = models.CharField(max_length=255,null=True,blank=True)
    coords = models.TextField(null=True,blank=True)
    observ = models.TextField(null=True,blank=True)
    label = models.CharField(max_length=255,null=True,blank=True)
    label_pk = models.CharField(max_length=255,null=True,blank=True)

    user_edit = models.TextField(null=True,blank=True)
    procedure = models.TextField(null=True,blank=True)
    
    

    
    

    