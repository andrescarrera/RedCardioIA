from django import forms
from django.forms.widgets import CheckboxInput, RadioSelect

from .models import Fle

import datetime

from django.utils.safestring import mark_safe



procedure_CHOICES = [
        ('1','Vias Altas Digestivas'), 
        ('2',' '), 
        ('3',' '), 
        ('4','Otro')
]

AFF_CHOICES=[
        ('','Seleccionar'),
        ('1','Si'),
        ('0','No'),
        ]

Af_CHOICES=[
        ('1','Si'),
        ('0','No'),
        ]

class FleForm(forms.ModelForm):
    day_procedure       = forms.DateField(required=False,initial=datetime.date.today,
                    widget=forms.DateInput(attrs={"class": "form-control",'type':'date', 'id':'date_procedure'
                                }))

    day_uploaded = forms.DateField(initial=datetime.date.today, widget=forms.DateInput(attrs={'class':'form-control','id':'day_uploaded'}))             
    
    procedure = forms.ChoiceField(required=False,widget=forms.Select(attrs={'class':'dropdown-item','name': 'procedure_select', 'id': 'procedure_select',}), choices=procedure_CHOICES)    
    procedure_other = forms.CharField(required=False,widget=forms.TextInput(attrs={"class": "form-control","id":"procedure_other"}))
    
    exam_diagnosis= forms.CharField(required=False, 
                    widget=forms.Textarea(
                            attrs={
                                "rows": 3,
                                "class": "form-control",
                                'cols': 120,
                                'name': 'diagn_select',
                                'id': 'diagn_select',
                                "readonly":"true"
                            }))    
    exam_diagnosis_explain=forms.CharField(required=False, 
                    widget=forms.Textarea(
                            attrs={
                                "rows": 1,
                                "class": "form-control",
                                'cols': 120,
                                'id': 'diagn_other'
                            }))
    
    biopsy = forms.ChoiceField(required=False,widget=forms.Select(attrs={'class':'dropdown-item','name': 'biopsy_select', 'id': 'biopsy_select',}), choices=AFF_CHOICES)
    biopsy_diagnosis = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control",'id':'biopsy_diagnosis'}))
    biopsy_analysis = forms.CharField(required=False, 
                    widget=forms.Textarea(
                            attrs={
                                "rows": 2,
                                "class": "form-control",
                                'cols': 120,
                                'id':'biopsy_analysis'
                            }))

    indication= forms.CharField(required=False, 
                    widget=forms.Textarea(
                            attrs={
                                "rows": 3,
                                "class": "form-control",
                                'cols': 120,
                                'name': 'indication_select',
                                'id': 'indication_select',
                                "readonly":"true"
                            }))  
    indication_desc= forms.CharField(required=False, 
                    widget=forms.Textarea(
                            attrs={
                                "rows": 1,
                                "class": "form-control",
                                'cols': 120,
                                'id': 'indication_other'
                            }))
        

    antecedent = forms.CharField(required=False, widget=CheckboxInput(attrs={'class':'antecedent_select', 'name': 'antecedent_select', 'id': 'antecedent_select'}))
    antecedent_desc = forms.CharField(required=False, 
                    widget=forms.Textarea(
                            attrs={
                                "placeholder": "Especifique cuál",
                                "rows": 1,
                                "class": "form-control ant_desc",
                                'cols': 120,
                                'id': 'ant_desc',
                                "style": "padding:0; margin:0; display: none;"
                            }))
    antecedent_helicob = forms.CharField(required=False, widget=CheckboxInput(attrs={'class': 'antecedent_helicob_select','name': 'antecedent_helicob_select', 'id': 'antecedent_helicob_select'}))
    antecedent_ulcera = forms.CharField(required=False, widget=CheckboxInput(attrs={'class': 'antecedent_ulcera_select','name': 'antecedent_ulcera_select', 'id': 'antecedent_ulcera_select'}))
    antecedent_AINES = forms.CharField(required=False, widget=CheckboxInput(attrs={'class': 'antecedent_AINES_select','name': 'antecedent_AINES_select', 'id': 'antecedent_AINES_select'}))
    antecedent_IBP = forms.CharField(required=False, widget=CheckboxInput(attrs={'class': 'antecedent_IBP_select','name': 'antecedent_IBP_select', 'id': 'antecedent_IBP_select'}))
    antecedent_antib = forms.CharField(required=False, widget=CheckboxInput(attrs={'class': 'antecedent_antib_select','name': 'antecedent_antib_select', 'id': 'antecedent_antib_select'}))
    
    informed_cons= forms.ChoiceField( required=True, widget=RadioSelect(attrs={'id': 'informed_cons','class': 'form-check-inline informed_cons', 'type':'radio', 'style': 'display: inline-block; padding: 0; margin: 0; margin-left: 5px'}), choices=Af_CHOICES,initial='0')    
    

        
    class Meta:
        model = Fle
        fields = ('title',
                'root_fle',
                'active_flg_file',
                'fle',
                'type_file',
                'img_file',
                'day_procedure',
                'day_uploaded',
                'id_pateint',
                'procedure',
                'procedure_other',
                'exam_diagnosis',
                'exam_diagnosis_explain',
                'biopsy',
                'biopsy_diagnosis',
                'biopsy_analysis',
                'indication',
                'indication_desc',
                'informed_cons',
                'antecedent',
                'antecedent_desc',
                'antecedent_helicob',
                'antecedent_ulcera',
                'antecedent_AINES',
                'antecedent_IBP',
                'antecedent_antib',
                'num_anot',
                'report',
                'user_edit',
                'root_inf_cons',
                'flg_inf_cons')

    def __init__(self, *args, **kwargs):
        super(FleForm, self).__init__(*args, **kwargs)
        self.fields['report'].required = False



