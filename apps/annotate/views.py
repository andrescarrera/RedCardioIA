from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import  get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from viewfiles.models import Fle
from patients.models import Procedures

from patients.models import AnnotOpt

from streamapp.camera import VideoCamera
from.forms import AnnotationForm
from.models import Annotation

import base64
import os
import datetime
import cv2
import numpy as np
from PIL import Image, ImageDraw

import pickle

@login_required(login_url="/login/")
def paint(request,pk,count):
    actual_user=request.user.username
    f = get_object_or_404(Fle, pk=pk)
    id=f.id_pateint
    name_video=f.fle.url
    name_video=name_video[1:]
    labels = AnnotOpt.objects.filter(proced=f.procedure)
    
    procedure = Procedures.objects.filter(idd=f.procedure)
    procedure=procedure[0]
    if procedure.flg_stat=='1':
        flg_stations=1
    else:
        flg_stations=0

    if procedure.flg_anot=='1':
        flg_annotations=1
    else:
        flg_annotations=0


    if request.method=='POST' and request.POST['ans']!='':
        ans= request.POST['ans']
        if ans=='Si':
            pk_actual=request.POST['pk_actual']
            pk_new=request.POST['pk_new']

            actual = get_object_or_404(Annotation,pk=pk_actual)
            name_actual=actual.root_ann
            os.remove(name_actual)
            if name_actual.find('png') < 0:
                os.remove(actual.root_png)
            
            new = get_object_or_404(Annotation,pk=pk_new)
            new_usr=new.user_edit
            actual_usr=actual.user_edit
            if actual_usr.find(new_usr) < 0:
                new.user_edit=new_usr+actual_usr
                new.save()
            
            Annotation.objects.filter(pk=pk_actual).delete()
            
            kwargs = {"pk": pk, "count":count}
            return redirect('VideoStreaming', **kwargs)
            
        else:
            pk_new=request.POST['pk_new']
            new = get_object_or_404(Annotation,pk=pk_new)
            new_name=new.root_ann
            os.remove(new_name)
            if new_name.find('png') < 0:
                new_name_temp=new.root_png
                os.remove(new_name_temp)

            Annotation.objects.filter(pk=pk_new).delete()

            form= AnnotationForm(request.POST)
            camera=VideoCamera(name_video)
            image,img = camera.get_frame(count)            
            
            encoded_img = base64.b64encode(image).decode('ascii')
            img_uri = 'data:%s;base64,%s' % ('image/png', encoded_img)      
            
            context = {
                'form':form,
                'img_uri': img_uri,
                'pk': pk,
                'count':count,
                'flg_stations':flg_stations,
                'flg_annotations':flg_annotations,
                'id_patient':f.id_pateint,
                'num_anot':f.num_anot,
                'labels':labels,
                'id_video':pk,
                'error':''
            }    
            return render(request, 'annotate/paint.html',context)
    else:
        name_video= f.fle.url
        name_video=name_video[1:]

        form= AnnotationForm(request.POST)
        
        camera=VideoCamera(name_video)
        tot=camera.tot_frames()
        if tot<count:
            count=tot-1
        image,img = camera.get_frame(count)
        
        encoded_img = base64.b64encode(image).decode('ascii')
        img_uri = 'data:%s;base64,%s' % ('image/png', encoded_img)       

        

        if request.method == 'POST':  
            if form.is_valid():
                coords=[]
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)

                if flg_annotations==1: # si el procedimiento se anota
                    form.save()
                    x=request.POST['pencil_x']
                    y=request.POST['pencil_y']
                    r=request.POST['rectangle']

                    p = Annotation.objects.last()            
                    
                    s=img.size
                    w=s[0]
                    h=s[1]
                    
                    dimentions=[]
                    geometry=[]            
                    if len(x)>2:
                        x=x.replace("[[","")
                        y=y.replace("[[","")
                        x=x.replace("]]","")
                        y=y.replace("]]","")


                        x=x.split('],[')
                        y=y.split('],[')

                        for i in range(len(x)):
                            x1=x[i]
                            y1=y[i]
                            
                            x1=x1.split(',')
                            y1=y1.split(',')

                            w1=float(x1[0])
                            h1=float(x1[1])
                            
                            scale=w/w1
                            xy = [
                            (xp,
                            yp)
                            for xp,yp in zip([float(x1[j])*scale for j in range(1,len(x1))],[float(y1[j])*scale for j in range(1,len(x1))])
                            ]  

                            coords.append(xy)
                            dimentions.append([w, h, w1, h1, scale])
                            geometry.append(0)
                    
                    if len(r)>2:
                        r=r.replace("[[","")
                        r=r.replace("]]","")
                        r=r.split('],[')
                        for i in range(len(r)):
                            r1=r[i]
                            
                            r1=r1.split(',')
                            
                            w1=float(r1[0])
                            h1=float(r1[1])

                            scale=w/w1
                            
                            x1=float(r1[2])*scale
                            y1=float(r1[3])*scale
                            x2=float(r1[4])*scale
                            y2=float(r1[5])*scale


                            shape = [(x1, y1), (x2, y2)]

                            coords.append(shape)
                            dimentions.append([w, h, w1, h1, scale])
                            geometry.append(1)
                            
                    name_coords='media/patients/'+str(id)+'/'+str(f.pk)+'/'+str(p.pk)+'_xy_coords.pkl'
                    name_annotation='media/patients/'+str(id)+'/'+str(f.pk)+'/'+str(p.pk)+'_'+request.POST['label']+'.png'

                    p.day_ann=datetime.date.today()
                    p.id_pateint=str(f.id_pateint)
                    p.root_ann=name_annotation
                    p.root_png=name_annotation
                    p.id_file=str(pk)
                    p.name_video=name_video
                    p.frame=count 
                    p.procedure=f.procedure 
                    p.user_edit=actual_user+';'
                    
                else:
                    label_fle=request.POST['label']
                    pk_label_fle=request.POST['pk_label']
                    
                    procedure = Procedures.objects.filter(idd=f.procedure)
                    procedure=procedure[0]
                    if procedure.flg_stat=='1':
                        annotation = Annotation.objects.filter(id_pateint=f.id_pateint,id_file=pk,label=label_fle,procedure=f.procedure)     
                        
                        form.save()  
                        p = Annotation.objects.last()                         
                        name= "media/patients/"+str(id)+'/'+str(f.pk)+'/'+str(p.pk)+'_'+pk_label_fle+'.png'                
                        name_video= f.fle.url
                        name_video=name_video[1:]

                        p.day_ann=datetime.date.today()
                        p.root_ann=name
                        p.root_png=name
                        p.id_pateint=str(f.id_pateint)
                        p.id_file=str(pk)
                        p.name_video=name_video
                        p.frame=count 
                        p.procedure=f.procedure     
                        p.user_edit=actual_user+';'
                        p.save()
                        annot=annotation[0]
                        if annot.pk != p.pk:                          
                            img.save(name)

                            context = {
                                'id_patient':id,
                                'pk':pk,
                                'actual_anot':annot,
                                'new_anot':p,
                                'station': label_fle,
                            }
                            return render(request, "annotate/confirm_delete.html", context)
                    else:
                        form.save()

                    
                    p = Annotation.objects.last()
                    
                    name_annotation='media/patients/'+str(id)+'/'+str(f.pk)+'/'+str(p.pk)+'_'+pk_label_fle+'.png'
                    name_coords='media/patients/'+str(id)+'/'+str(f.pk)+'/'+str(p.pk)+'_xy_coords.pkl'
                    
                    p.day_ann=datetime.date.today()
                    p.root_ann=name_annotation
                    p.root_png=name_annotation
                    p.id_pateint=str(f.id_pateint)
                    p.id_file=str(pk)
                    p.name_video=name_video
                    p.label=label_fle
                    p.label_pk=pk_label_fle
                    p.procedure=f.procedure
                    p.frame=count           
                    p.user_edit=actual_user+';'

                img.save(name_annotation)

                if len(coords)>0:
                    with open(name_coords, 'wb') as folder:
                        pickle.dump([coords,dimentions,geometry],folder)
                    p.coords=name_coords
                
                p.save()

                form = AnnotationForm()

                annotation = Annotation.objects.filter(id_pateint=f.id_pateint,id_file=pk)  
                fle = Fle.objects.filter(id=pk)
                fle=fle[0]
                fle.num_anot=int(annotation.count())
                fle.save() 
            
                kwargs = {"pk": pk, "count":count}
                return redirect('VideoStreaming', **kwargs)
            else:
                form= AnnotationForm(request.POST)
                camera=VideoCamera(name_video)
                tot= camera.tot_frames
                image,img = camera.get_frame(count)
                
                encoded_img = base64.b64encode(image).decode('ascii')
                img_uri = 'data:%s;base64,%s' % ('image/png', encoded_img)       

                
                context = {
                    'form':form,
                    'img_uri': img_uri,
                    'pk': pk,
                    'count':count,
                    'flg_stations':flg_stations,
                    'flg_annotations':flg_annotations,
                    'id_patient':f.id_pateint,
                    'num_anot':f.num_anot,
                    'labels':labels,
                    'id_video':pk,
                    'error':'Seleccione una etiqueta para la imagen'
                }    
                return render(request, 'annotate/paint.html',context)
        else:
            context = {
                'form':form,
                'img_uri': img_uri,
                'pk': pk,
                'count':count,
                'flg_stations':flg_stations,
                'flg_annotations':flg_annotations,
                'id_patient':f.id_pateint,                
                'num_anot':f.num_anot,
                'labels':labels,
                'id_video':pk,
                'error':''
            }    
            return render(request, 'annotate/paint.html',context)
                
@login_required(login_url="/login/")
def insert_annot(name,count,name_coords):
    camera=VideoCamera(name)
    tot= camera.tot_frames
    image,img = camera.get_frame(count)
    
    if not (name_coords == ''):
        img = Image.fromarray(img)
        with open(name_coords, 'rb') as folder:
            coords,_,geometry=pickle.load(folder)
        
        geometry=list(geometry)
        coords=list(coords)

        for i in range(len(geometry)):
            xy=coords[i]
            if geometry[i]==0:
                img1 = ImageDraw.Draw(img)  
                img1.line(xy, width=5, fill ="red")
            else:
                img1 = ImageDraw.Draw(img)  
                img1.rectangle(xy, outline ="red",width=5)

        img=np.asarray(img) 
        _,image=cv2.imencode('.png', img)

    encoded_img = base64.b64encode(image).decode('ascii')
    img_uri = 'data:%s;base64,%s' % ('image/png', encoded_img)     

    return img_uri  

@login_required(login_url="/login/")
def list_anot(request,pk,id):    
    actual_user=request.user.username
    f = get_object_or_404(Fle, pk=pk)

    if request.method=='POST' and request.POST['ans']!='':
        ans= request.POST['ans']
        if ans=='Si':
            pk_actual=request.POST['pk_actual']
            pk_new=request.POST['pk_new']

            actual = get_object_or_404(Annotation,pk=pk_actual)
            name_actual=actual.root_ann
            os.remove(name_actual)
            if name_actual.find('png') < 0:
                os.remove(actual.root_png)
            
            new = get_object_or_404(Annotation,pk=pk_new)
            new_usr=new.user_edit
            actual_usr=actual.user_edit
            if actual_usr.find(new_usr) < 0:
                new.user_edit=new_usr+actual_usr
                new.save()
            
            Annotation.objects.filter(pk=pk_actual).delete()
            
        else:
            pk_new=request.POST['pk_new']
            new = get_object_or_404(Annotation,pk=pk_new)
            new_name=new.root_ann
            os.remove(new_name)
            if new_name.find('png') < 0:
                new_name_temp=new.root_png
                os.remove(new_name_temp)

            Annotation.objects.filter(pk=pk_new).delete()

    
        stations=[]
        roots=[]

        stations0=[]
        flg_stat0=[]
        roots0=[]
        roots0_png=[]
        for i in range(1,12):
            station="Estación "+str(i)
            annotation = Annotation.objects.filter(id_pateint=id,id_file=pk,label=station,procedure=f.procedure)       
            stations.append(i)
            stations0.append(i)
            if annotation.count()>0:
                annotation=annotation[0]
                flg_stat0.append(True)

                name_coords=annotation.coords  
                if name_coords != "":
                    name=annotation.name_video
                    count=int(annotation.frame)
                        
                    img_uri=insert_annot(name,count,name_coords)
                    roots.append(img_uri)
                    roots0.append(img_uri)
                    roots0_png.append(img_uri)
                else:
                    roots.append('/'+str(annotation.root_png))
                    roots0.append('/'+str(annotation.root_png))
                    roots0_png.append('/'+str(annotation.root_ann))


                
            else:
                roots.append(False)
                roots0.append(False)
                roots0_png.append(False)                
                flg_stat0.append(False)

        stations1=[]
        flg_stat1=[]
        roots1=[]
        roots1_png=[]
        for i in range(12,23):
            station="Estación "+str(i)
            annotation = Annotation.objects.filter(id_pateint=id,id_file=pk,label=station,procedure=f.procedure)       
            stations.append(i)
            stations1.append(i)
            if annotation.count()>0:
                annotation=annotation[0]
                flg_stat1.append(True)

                name_coords=annotation.coords  
                if name_coords != "":
                    name=annotation.name_video
                    count=int(annotation.frame)
                        
                    img_uri=insert_annot(name,count,name_coords)
                    roots.append(img_uri)
                    roots1.append(img_uri)
                    roots1_png.append(img_uri)
                else:
                    roots.append('/'+str(annotation.root_png))
                    roots1.append('/'+str(annotation.root_png))
                    roots1_png.append('/'+str(annotation.root_png))

                
            else:
                roots.append(False)                
                roots1.append(False)                
                roots1_png.append(False)
                flg_stat1.append(False)

        
        lista1=zip(stations0,flg_stat0,roots0,roots0_png)
        lista2=zip(stations1,flg_stat1,roots1,roots1_png)

        form = AnnotationForm(initial={'label': "1"})
        context = {
            'lista1':lista1,
            'lista2':lista2,
            'form':form,
            'stations':stations,
            'roots':roots,
            'id_patient':id,
            'id_video':pk,
        }
        return render(request, "annotate/list_stations.html", context)
    else:
        procedure = Procedures.objects.filter(idd=f.procedure)
        procedure=procedure[0]
        if procedure.flg_stat!='1':  
            annotations = Annotation.objects.filter(id_pateint=id,id_file=pk,procedure=f.procedure)       
            num=annotations.count()
            if num>1:
                flg_b=True    
                flg_n=True    
                if request.method == "POST":
                    if request.POST['action_val'] == 'next':
                        global indx
                        indx=indx+1

                        if indx==num-1:
                            flg_n=False    
                        else:
                            flg_n=True

                        if indx>num-1:
                            indx=num-1    
                    elif request.POST['action_val'] == 'before':
                        indx=indx-1
                        if indx==0:
                            flg_b=False
                        else:
                            flg_b=True   
                            
                        if indx<0:
                            indx=0
                        
                else:
                    indx=0
                    flg_b=False    
                    flg_n=True   
            else:
                flg_b=False
                flg_n=False
                indx=0

            anot=annotations[indx]
            name=anot.name_video
            count=int(anot.frame)
            name_coords=anot.coords        
            img_uri=insert_annot(name,count,name_coords)
            
            context = {
                        'img_uri': img_uri,      
                        'flg_b':flg_b,
                        'flg_n':flg_n,
                        'indx':indx+1,
                        'len':num,
                        'id_patient':id,
                        'label': anot.label,
                        'obs': anot.observ,
                        'id_video':pk,
                    }
            return render(request, "annotate/list_annot.html", context)

        else:
            if request.method == 'POST' and request.FILES['myfile']:
                label=str(request.POST['station'])                
                station="Estación "+str(request.POST['station'])
                annotation = Annotation.objects.filter(id_pateint=id,id_file=pk,label=station,procedure=f.procedure)     
                fs = FileSystemStorage()

                form= AnnotationForm(request.POST)
                form.save()
                p = Annotation.objects.last()
                name= 'patients/'+str(id)+'/'+str(f.pk)+'/'+str(p.pk)+'_'+label+'.png' 
                name_video= f.fle.url
                name_video=name_video[1:]

                myfile = request.FILES['myfile'] 
                #default_storage.save(name_orig, ContentFile(myfile.read()))
                image = cv2.imdecode(np.frombuffer(myfile.read() , np.uint8), cv2.IMREAD_UNCHANGED)
                url_file=myfile.name
                extention=url_file.split('.')
                extention=extention[-1]
                name_orig= 'patients/'+str(id)+'/'+str(f.pk)+'/'+str(p.pk)+'_'+label+'.'+extention


                p.day_ann=datetime.date.today()
                p.root_ann="media/"+name_orig
                p.root_png="media/"+name
                p.id_pateint=str(id)
                p.id_file=str(pk)
                p.name_video=name_video
                p.label=station
                p.label_pk=label
                p.procedure=f.procedure
                p.coords=""                 
                p.user_edit=actual_user+';'
                p.save() 
                
                fs.save(name_orig,myfile)
                
                cv2.imwrite("media/"+name,image)

                annot=annotation[0]
                if annot.pk != p.pk:  
                    annot=annotation[0]
                    actual_name=annot.root_ann

                    context = {
                        'id_patient':id,
                        'pk':pk,
                        'actual_anot':annot,
                        'new_anot':p,
                        'station':station
                    }
                    return render(request, "annotate/confirm_delete.html", context)
                    
                else:
                    annotation = Annotation.objects.filter(id_pateint=id,id_file=pk)       
                    fle = Fle.objects.filter(id=pk)
                    fle=fle[0]
                    fle.num_anot=int(annotation.count())
                    fle.save()  

            stations=[]
            roots=[]

            stations0=[]
            flg_stat0=[]
            roots0=[]
            roots0_png=[]
            for i in range(1,12):
                station="Estación "+str(i)
                annotation = Annotation.objects.filter(id_pateint=id,id_file=pk,label=station,procedure=f.procedure)       
                stations.append(i)
                stations0.append(i)
                if annotation.count()>0:
                    annotation=annotation[0]
                    flg_stat0.append(True)

                    name_coords=annotation.coords  
                    if name_coords != "":
                        name=annotation.name_video
                        count=int(annotation.frame)
                            
                        img_uri=insert_annot(name,count,name_coords)
                        roots.append(img_uri)
                        roots0.append(img_uri)
                        roots0_png.append(img_uri)
                    else:
                        roots.append('/'+str(annotation.root_png))
                        roots0.append('/'+str(annotation.root_png))
                        roots0_png.append('/'+str(annotation.root_ann))


                    
                else:
                    roots.append(False)
                    roots0.append(False)
                    roots0_png.append(False)                
                    flg_stat0.append(False)

            stations1=[]
            flg_stat1=[]
            roots1=[]
            roots1_png=[]
            for i in range(12,23):
                station="Estación "+str(i)
                annotation = Annotation.objects.filter(id_pateint=id,id_file=pk,label=station,procedure=f.procedure)       
                stations.append(i)
                stations1.append(i)
                if annotation.count()>0:
                    annotation=annotation[0]
                    flg_stat1.append(True)

                    name_coords=annotation.coords  
                    if name_coords != "":
                        name=annotation.name_video
                        count=int(annotation.frame)
                            
                        img_uri=insert_annot(name,count,name_coords)
                        roots.append(img_uri)
                        roots1.append(img_uri)
                        roots1_png.append(img_uri)
                    else:
                        roots.append('/'+str(annotation.root_png))
                        roots1.append('/'+str(annotation.root_png))
                        roots1_png.append('/'+str(annotation.root_png))

                    
                else:
                    roots.append(False)                
                    roots1.append(False)                
                    roots1_png.append(False)
                    flg_stat1.append(False)

            
            lista1=zip(stations0,flg_stat0,roots0,roots0_png)
            lista2=zip(stations1,flg_stat1,roots1,roots1_png)

            form = AnnotationForm(initial={'label': "1"})
            context = {
                'lista1':lista1,
                'lista2':lista2,
                'form':form,
                'stations':stations,
                'roots':roots,
                'id_patient':id,
                'id_video':pk,
            }
            return render(request, "annotate/list_stations.html", context)


