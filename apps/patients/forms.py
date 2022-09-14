from django import forms
from .models import Patient
import datetime
from .models import DiagnosisProc, IndProc, AnnotOpt, Procedures

GENDER_CHOICES = [
        ('','Seleccionar'),
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Indefinido','Indefinido')
    ]


ETHNIC_CHOICES = [
        ('Sin pertenencia étnica', 'Sin pertenencia étnica'),
        ('Afrocolombiano', 'Afrocolombiano'),
        ('Indígena','Indígena'),
        ('Raizal','Raizal'),
        ('Palenquero','Palenquero'),
        ('Gitano','Gitano'),
        ('Caucasico','Caucasico'),
    ]

ID_CHOICES = [
        ('CC', 'CC'),
        ('TI', 'TI'),
        ('CE', 'CE')
    ]


EXAMS_CHOICES = [
        ('TAC', 'TAC'),
        ('RMN', 'RMN'),
        ('Laparoscopia', 'Laparoscopia'),
        ('Colangioresonancia','Colangioresonancia')
    ]

AFF_CHOICES=[
    ('Si','Si'),
    ('No','No')
]


class PatientForm(forms.ModelForm):
    type_id       = forms.ChoiceField(label='Tipo de Identificación', required=True, widget=forms.Select(attrs={'class':'dropdown-item','name': 'typeid_select', 'id': 'typeid_select', 'style':'padding-right: 0; width: 100%; padding-top:8pt; padding_bottom:8pt;'}), choices=ID_CHOICES, initial='CC')
  
    active_flg_patient       = forms.ChoiceField(required=False)
    idd       = forms.CharField(label='Número de Identificación', required=True,
                    widget=forms.TextInput(attrs={"placeholder": "Número",
                                            "class": "form-control",
                                            "id":"idd_input",
                                            "name":"idd_input",
                                }))
    age       = forms.CharField(label='Edad', required=True,
                    widget=forms.TextInput(attrs={"placeholder": "Edad",
                                            "class": "form-control", "id":"age_input", "name":"age_input"
                                }))
    name       =  forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Nombre", "class": "form-control","id":"name_input","name":"name_input"}))
    lastname       =  forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Apellido", "class": "form-control","id":"lname_input","name":"lname_input"}))
    phone       =  forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Teléfono","class": "form-control","id":"phone_input","name":"phone_input"}))
    gender       = forms.ChoiceField(label='Genero', widget=forms.Select(attrs={'class':'dropdown-item','name': 'gender_select', 'id': 'gender_select',}), choices=GENDER_CHOICES, required=True)
    ethnic       = forms.ChoiceField(label='Etnia', widget=forms.Select(attrs={'class':'dropdown-item','name': 'etnic_select', 'id': 'etnic_select',}), choices=ETHNIC_CHOICES, required=True)



    day = forms.DateField(label='Fecha', initial=datetime.date.today, widget=forms.DateInput(attrs={'class':'form-control', "value":datetime.date.today}))

    
    
    
    class Meta:
        model= Patient
        fields= [
            'type_id',
            'active_flg_patient',
            'idd',
            'age',
            'name',
            'lastname',
            'phone',
            'gender',
            'user_edit',
            'ethnic',
            'day',
        ]
 
class DiagnosisProcForm(forms.ModelForm):
    class Meta:
        model = DiagnosisProc
        fields = ('idd',
                'name',
                'proced')

class IndProcForm(forms.ModelForm):
    class Meta:
        model = IndProc
        fields = ('idd',
                'name',
                'proced')
   
class ProceduresForm(forms.ModelForm):
    class Meta:
        model = Procedures
        fields = ('idd',
                'name',
                'flg_stat',
                'flg_anot')
   

class AnnotOptForm(forms.ModelForm):
    class Meta:
        model = AnnotOpt
        fields = ('idd',
                'name',
                'proced')
   
 
 