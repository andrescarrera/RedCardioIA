from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.conf import settings
from .forms import FleForm
from .models import Fle
from patients.models import DiagnosisProc, IndProc, Procedures
from patients.models import Patient
import os
import cv2

from patients.forms import PatientForm
#def convert_avi_to_mp4(avi_file_path, output_name):
 #   os.popen("ffmpeg  -y -i '{input}' -vcodec libx264 -acodec aac '{output}'".format(input = avi_file_path, output = output_name)) 
  #  return True


def convert_lr_video(input_name, output_name,f):
    vcap = cv2.VideoCapture(input_name)
    width  = vcap.get(3)  # float `width`
    height = vcap.get(4)  # float `height

    new_height=720
    new_width=int(new_height*width/height)

    # no ejecutar en paralelo
    #os.system("ffmpeg  -y -i '{input}' -r 15 -s {w}x{h} -an '{output}'".format(input = input_name,w=new_width,h=new_height,output = output_name))
    # ejecutar en paralelo
    os.popen("ffmpeg  -y -i '{input}' -r 15 -s {w}x{h} -an '{output}'".format(input = input_name,w=new_width,h=new_height,output = output_name))
    
    # -an -> remove audio chanel
    # -vcodec copy -> straight copy and not do any processing/encoding 
    # -r 30 -s 112x112 -c -> fps y resolucion

    
    return True

@login_required(login_url="/login/")
def delete_file(request, pk, id):
    actual_user=request.user.username
    if request.method == 'POST':
        obj = get_object_or_404(Fle, pk=pk)
        obj.active_flg_file =False
        actual_user_edit=obj.user_edit
        if actual_user_edit.find(actual_user+';') < 0:
            obj.user_edit=actual_user_edit+actual_user+';'
        else:
            obj.user_edit=actual_user_edit
        obj.save()      
        
    return redirect('filesView',id=id)

@login_required(login_url="/login/")
def files_view_indx(request,id=id): 
    actual_user=request.user.username
    datadiagn = DiagnosisProc.objects.all()
    dataind = IndProc.objects.all()
    procedures = Procedures.objects.all()

    file_url=''
    try:
        obj = get_object_or_404(Patient, id=id)
    except:
        obj=None
    
       
    fles = Fle.objects.filter(id_pateint=id,active_flg_file=True)
    
    if request.method == 'POST':
        form = FleForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            
            f = Fle.objects.last() # list of objects
            actual_user_edit=f.user_edit

            url_file=f.fle.url            
            extention=url_file.split('.')
            extention=extention[-1]
            
            try:
                url_report=f.report.url
                extention_report=url_report.split('.')
                extention_report=extention_report[-1]
            except:
                url_report=False

            fs = FileSystemStorage()
            
            if extention=='png' or extention=='jpg' or extention=='tif' or extention=='jpeg':
                f.type_file='Imagen'
                f.img_file=True
            elif extention=='mp4' or extention=='mpeg' or  extention=='avi':
                f.type_file='Video'
                f.img_file=False
            else:
                f.type_file='Error'

            filename=url_file            
            filename=filename.split('media/')
            filename=filename[-1]

            if url_report != False:
                filename_report=url_report           
                filename_report=filename_report.split('media/')
                filename_report=filename_report[-1]
            
            if f.type_file=='Error':
                fs.delete(filename)    
                if url_report != False:
                    fs.delete(filename_report)  
                file_url='Tipo de archivo no soportado'
            else:
                if url_report != False:
                    name_report='patients/'+str(id)+'/'+str(f.pk)+'/'+str(f.pk)+'_report.'+extention_report
                    file_report=request.FILES['report']
                    fs.save(name_report, file_report)
                    fs.delete(filename_report)
                    name_report='/'+name_report
                else:
                    name_report=''

                name='patients/'+str(id)+'/'+str(f.pk)+'/'+str(f.pk)+'.'+extention
                if not os.path.exists('media/'+'patients/'+str(id)+'/'+str(f.pk)):
                    os.makedirs('media/'+'patients/'+str(id)+'/'+str(f.pk))
                
                fs.save(name, f.fle)
                fs.delete(filename)

                output_name_lr='media/patients/'+str(id)+'/'+str(f.pk)+'/'+str(f.pk)+'_lr.mp4'
                convert_lr_video('media/'+name, output_name_lr,f)

                f.title=f.pk
                f.root_fle=output_name_lr
                f.id_pateint=id
                f.active_flg_file =True
                f.num_anot=0
                f.report=name_report
                f.fle='/'+name
                
                if actual_user_edit.find(actual_user+';') < 0:
                    f.user_edit=actual_user_edit+actual_user+';'
                else:
                    f.user_edit=actual_user_edit
                f.save()    
        else:
            file_url='Error'    
    else:
        form = FleForm()
    try:
        idp=request.POST['idp']
        obj = get_object_or_404(Patient, id=idp)
        actual_user_edit=obj.user_edit

        initial_date=obj.day
        active_flg_patient=obj.active_flg_patient        
        form1 = PatientForm(request.POST or None, instance=obj)
        if form1.is_valid():
            obj.day=initial_date
            obj.active_flg_patient=active_flg_patient
            
            if actual_user_edit.find(actual_user+';') < 0:
                obj.user_edit=actual_user_edit+actual_user+';'
            else:
                obj.user_edit=actual_user_edit
            obj.save()
            form1.save()
            form1 = PatientForm()        
            return redirect('filesView',id=obj.id)
    except:
        form1=PatientForm(request.POST)

    try:
        pk=request.POST['pk_edt']
        datadiagn = DiagnosisProc.objects.all()
        dataind = IndProc.objects.all()
        procedures = Procedures.objects.all()
        obj = get_object_or_404(Patient, id=id)

        f = get_object_or_404(Fle, pk=pk)
        pk=f.pk
        root_fle=f.root_fle
        title=f.title
        fle=f.fle
        type_file=f.type_file
        img_file=f.img_file
        id_pateint=f.id_pateint
        active_flg_file =f.active_flg_file
        num_anot=f.num_anot 
        report=f.report
        root_inf_cons=f.root_inf_cons        
        flg_inf_cons=f.flg_inf_cons
        actual_user_edit=f.user_edit
        if actual_user_edit.find(actual_user+';') < 0:
            user_edit=actual_user_edit+actual_user+';'
        else:
            user_edit=actual_user_edit

        
        form = FleForm(request.POST or None, instance=f)
        if form.is_valid():
            f.pk=pk
            f.title=title
            f.root_fle=root_fle
            f.active_flg_file=active_flg_file
            f.fle=fle
            f.type_file=type_file
            f.img_file=img_file
            f.id_pateint=id_pateint
            f.num_anot=num_anot
            f.root_inf_cons=root_inf_cons        
            f.flg_inf_cons=flg_inf_cons  
            f.user_edit=user_edit

            fs = FileSystemStorage()
            
            try:
                myfile = request.FILES['myfile']
                url_report = myfile.name
            except:
                url_report = False

            if url_report!= False:
                extention_report=url_report.split('.')
                extention_report=extention_report[-1]
                name_report='patients/'+str(id)+'/'+str(f.pk)+'/'+str(f.pk)+'_report.'+extention_report
                if os.path.isfile("media/"+name_report):
                    fs.delete(name_report)           
                
                fs.save(name_report, myfile)
                    
                name_report='/'+name_report
                f.report=name_report
            else:
                name_report=''
                f.report=report      


            if f.antecedent== "False":
                f.antecedent_desc=''
            
            if actual_user_edit.find(actual_user+';') < 0:
                f.user_edit=actual_user_edit+actual_user+';'
            else:
                f.user_edit=actual_user_edit
            f.save()

            form = FleForm()
            
            fles = Fle.objects.filter(id_pateint=id)
            file_url=''
            context = {
            'form': form,
            'obj':obj,
            'fles': fles,
            'file_url':file_url,
            'datadiagn':datadiagn,
            'dataind':dataind,    
            'procedures':procedures
            }
            return HttpResponseRedirect(reverse('filesView', kwargs = {'id':id}))
    except:
        context = {
            'object': obj,
            'form1': form,
            'form':form1,
            'fles': fles,
            'file_url':file_url,
            'datadiagn':datadiagn,
            'dataind':dataind,    
            'procedures':procedures
        }
        return render(request, 'viewfiles/file_list.html', context)

