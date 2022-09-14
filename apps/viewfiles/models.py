from django.db import models


class Fle(models.Model):
    root_fle = models.TextField(null=True,blank=True)
    title =models.TextField(null=True,blank=True)

    active_flg_file=models.BooleanField(null=True,blank=True)    
    
    fle = models.FileField(upload_to='')
    type_file = models.TextField(null=True,blank=True)
    img_file = models.BooleanField(null=True,blank=True)
    day_procedure = models.DateField(null=True,blank=True)
    day_uploaded = models.DateField(null=True,blank=True)
    
    id_pateint = models.TextField(null=True,blank=True)
    
    procedure = models.TextField(null=True,blank=True)
    procedure_other =models.TextField(null=True,blank=True)
    
    exam_diagnosis =models.TextField(null=True,blank=True)
    exam_diagnosis_explain= models.TextField(null=True,blank=True)

    biopsy = models.TextField(null=True,blank=True)
    biopsy_diagnosis = models.TextField(null=True,blank=True)
    biopsy_analysis = models.TextField(null=True,blank=True)    

    indication= models.TextField(null=True,blank=True)
    indication_desc= models.TextField(null=True,blank=True)

    antecedent= models.TextField(null=True,blank=True)
    antecedent_desc = models.TextField(null=True,blank=True)
    antecedent_helicob = models.TextField(null=True,blank=True)
    antecedent_ulcera = models.TextField(null=True,blank=True)
    antecedent_AINES = models.TextField(null=True,blank=True)
    antecedent_IBP = models.TextField(null=True,blank=True)
    antecedent_antib = models.TextField(null=True,blank=True)

    informed_cons= models.TextField(null=True,blank=True)

    num_anot= models.TextField(null=True,blank=True)

    report = models.FileField(upload_to='')    

    user_edit = models.TextField(null=True,blank=True)

    
    root_inf_cons=models.TextField(null=True,blank=True)
    flg_inf_cons=models.BooleanField(null=True,blank=True)
    
            




