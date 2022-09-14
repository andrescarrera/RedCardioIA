from django import forms

from .models import Annotation

class AnnotationForm(forms.ModelForm):
    label = forms.CharField(required=True, widget=forms.TextInput(attrs={"readonly":"true", 'class':'dropdown-item diagn_select','name': 'diagn_select', 'id': 'diagn_select'}))
    label_pk = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'dropdown-item','name': 'label_pk', 'id': 'label_pk'}))
        
    observ=forms.CharField(required=False, 
                    widget=forms.Textarea( 
                            attrs={
                                "rows": 2,
                                "class": "form-control",
                                'cols': 120
                            }))
    
    class Meta:
        model = Annotation
        fields = ('root_ann',
                'root_png',
                'coords',
                'name_video',
                'day_ann',
                'id_pateint',
                'frame',
                'id_file',
                'observ',
                'user_edit',
                'label',
                'label_pk',
                'procedure')

