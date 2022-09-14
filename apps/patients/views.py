from django.http import  HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required

from .forms import PatientForm
from .models import Patient
from viewfiles.models import Fle
from patients.models import DiagnosisProc, IndProc, AnnotOpt, Procedures
import os
# Descomentar solo la primera vez que se corre}
# Procedimientos y banderas
Proced=["Vias Altas Digestivas",
            " ",
            " ",
            "Otro"]
Flgs_stat=[1, # bandera estaciones
        0,
        0,
        0]
Flgs_anot=[0, # bandera anotaciones
        0,
        1,
        0]
# Opciones Diagnósticos
DgGrl=[ "Sin Hallazgos", # Generales
        "Otro", 
        "Lesión"]         
DgEndo=["Esofagitis Erosiva grado A", # Vias digestivas altas
        "Esofagitis Erosiva grado B",
        "Esofagitis Erosiva grado C",
        "Esofagitis Erosiva grado D",
        "Esofagitis Infecciosa",
        "Esofago de Barrett - CM(abierta)",
        "Varices esofágicas",
        "Gastritis Eritematosa",
        "Gastritis Erosiva plana", 
        "Gastritis Erosiva elevada", 
        "Gastritis Atrófica", 
        "Gastritis Hemorrágica", 
        "Gastritis Hipertrófica", 
        "Gastritis Folicular", 
        "Úlceras - Forrest IA", 
        "Úlceras - Forrest IB", 
        "Úlceras - Forrest IIA", 
        "Úlceras - Forrest IIB", 
        "Úlceras - Forrest IIC", 
        "Úlceras - Forrest III",
        "Metaplasia Intestinal"]
DgCol=["Pólipos"] # Vias digestivas bajas
DgPanc=["Lesión Maligna",# Páncreas
        "Lesión Benigna",
        "Pancreatitis"] 

# Opciones Indicaciones
IndGrl=["Tamización", # Generales
        "Otro examen que muestre una lesión",
        "Dolor abdominal",
        "Pérdida de peso",
        "Otro"]
IndEndo=["Regurgitación", # Vias digestivas altas
        "Pirosis",
        "Disfagia",
        "Odinofagia",
        "Hematemesis - Melenas",
        "Ascitis",
        "Dispepsia",
        "Emesis",
        "Anemia",
        "Diarrea crónica"]
IndCol=["Sangrado rectal"]# Vias digestivas bajas
IndPanc=["Ictericia"] # Páncreas

# Opciones Anotaciones
AnnEndo=["Estación 1", # Vias digestivas altas
         "Estación 2",
         "Estación 3",
         "Estación 4",
         "Estación 5",
         "Estación 6",
         "Estación 7",
         "Estación 8",
         "Estación 9",
         "Estación 10",
         "Estación 11",
         "Estación 12",
         "Estación 13",
         "Estación 14",
         "Estación 15",
         "Estación 16",
         "Estación 17",
         "Estación 18",
         "Estación 19",
         "Estación 20",
         "Estación 21",
         "Estación 22"]
AnnCol=["Pólipo", # Vias digestivas bajas
        "Úlcera",
        "Indefinido",
        "Sin Hallazgos",
        "Otro"]
AnnPanc=["Benigno", # Páncreas
        "Maligno",
        "Pancreatitis",
        "Indefinido",
        "Sin Hallazgos",
        "Otro"]
# Hasta aqui

@login_required(login_url="/login/")
def patients_list_view(request):    
    actual_user=request.user.username
    try:
        myfile = request.FILES['myfile']
    except:
        myfile = False

    if request.method == 'POST' and (myfile!=False):
        myfile = request.FILES['myfile']
        folder='patients/'+request.POST['id']+'/'+request.POST['pk']+'/'
            
        url=myfile.name        
        ext=url.split('.')
        ext=ext[-1]

        name= folder+request.POST['pk']+'_inform_cons.'+ext
        
        fs = FileSystemStorage()
        if os.path.isfile("media/"+name):
            fs.delete(name)  

        fs.save(name, myfile)

        obj = get_object_or_404(Fle,pk=request.POST['pk'])
        actual_user_edit=obj.user_edit             
            
        if actual_user_edit.find(actual_user+';') < 0:
            obj.user_edit=actual_user_edit+actual_user+';'
        else:
            obj.user_edit=actual_user_edit

        obj.root_inf_cons=name
        obj.flg_inf_cons=True
        obj.save()
    
    # Descomentar solo la primera vez que se corre
    DiagnosisProc.objects.all().delete()
    for x in range(len(DgEndo)):
        dgn=DiagnosisProc(idd=x, name=DgEndo[x], proced='1')
        dgn.save()
    for x in range(len(DgCol)):
        dgn=DiagnosisProc(idd=x, name=DgCol[x], proced='2')
        dgn.save()
    for x in range(len(DgPanc)):
        dgn=DiagnosisProc(idd=x, name=DgPanc[x], proced='3')
        dgn.save()
    for x in range(len(DgGrl)):
        dgn=DiagnosisProc(idd=x, name=DgGrl[x], proced='0')
        dgn.save()

    IndProc.objects.all().delete()
    for x in range(len(IndEndo)):
        dgn=IndProc(idd=x, name=IndEndo[x], proced='1')
        dgn.save()
    for x in range(len(IndCol)):
        dgn=IndProc(idd=x, name=IndCol[x], proced='2')
        dgn.save()
    for x in range(len(IndPanc)):
        dgn=IndProc(idd=x, name=IndPanc[x], proced='3')
        dgn.save()
    for x in range(len(IndGrl)):
        dgn=IndProc(idd=x, name=IndGrl[x], proced='0')
        dgn.save()

    AnnotOpt.objects.all().delete()
    for x in range(len(AnnEndo)):
        dgn=AnnotOpt(idd=x+1, name=AnnEndo[x], proced='1')
        dgn.save()
    for x in range(len(AnnCol)):
        dgn=AnnotOpt(idd=x+1, name=AnnCol[x], proced='2')
        dgn.save()
    for x in range(len(AnnPanc)):
        dgn=AnnotOpt(idd=x+1, name=AnnPanc[x], proced='3')
        dgn.save()

    
    Procedures.objects.all().delete()
    for x in range(len(Proced)):
        dgn=Procedures(idd=x+1, name=Proced[x], flg_stat=Flgs_stat[x],flg_anot=Flgs_anot[x])
        dgn.save()
    # Hasta aqui

    queryset = Patient.objects.filter(active_flg_patient=True).order_by('-day','-id')
    listas=[]
    for j in range(queryset.count()):
        id=queryset[j].id
        fles = Fle.objects.filter(id_pateint=id,active_flg_file=True)
        files=[]
        flg_cons=[]
        roots=[]
        dates=[]
        procedures=[]

        for i in range(fles.count()):
            f=fles[i]
            
            files.append(f.pk)
            roots.append(f.root_inf_cons)           
            flg_cons.append(f.flg_inf_cons)
            dates.append(f.day_procedure)    
            proc = Procedures.objects.filter(idd=f.procedure)      
            proc=proc[0]  
            procedures.append(proc.name)
        
        if len(files)==0:
            lista=False
        else:
            lista=zip(files,flg_cons,roots,dates,procedures) 
        listas.append(lista)

    outputs=zip(queryset,listas)  
    try: 
        idp=request.POST['idp']
    except:
        idp=''
    if idp != '': #editar        
        obj = get_object_or_404(Patient, id=idp)
        initial_date=obj.day
        active_flg_patient=obj.active_flg_patient    
        actual_user_edit=obj.user_edit    
        form = PatientForm(request.POST or None, instance=obj)
        if form.is_valid():
            obj.day=initial_date
            obj.active_flg_patient=active_flg_patient
            
            if actual_user_edit.find(actual_user+';') < 0:
                obj.user_edit=actual_user_edit+actual_user+';'
            else:
                obj.user_edit=actual_user_edit

            obj.save()
            form.save()
            form = PatientForm()        
            return redirect('patientsListView')    
    else: # Nuevo paciente
        form= PatientForm(request.POST or None)
        if form.is_valid():
            form.save()
            
            p = Patient.objects.last()
            p.active_flg_patient=True            
            p.user_edit=actual_user+';'
            p.save()

            form = PatientForm()
            return redirect('filesView',id=p.id)

    context = {
        "object_list": queryset,
        'form':form,
        'outputs':outputs,
    }

    return render(request, "patients/list.html",context)


@login_required(login_url="/login/")
def patient_inactivate_view(request, id):
    actual_user=request.user.username
    obj = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        obj.active_flg_patient =False
        actual_user_edit=obj.user_edit
        if actual_user_edit.find(actual_user+';') < 0:
            obj.user_edit=actual_user_edit+actual_user+';'
        else:
            obj.user_edit=actual_user_edit
        obj.save()   
        return redirect('../../')
    context = {
        "object": obj
    }
    return render(request, "patients/patient_delete.html", context)
