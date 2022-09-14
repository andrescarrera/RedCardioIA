from django.shortcuts import render, redirect
from django.shortcuts import  get_object_or_404,render, redirect
from django.contrib.auth.decorators import login_required

from streamapp.camera import VideoCamera
from viewfiles.models import Fle
from patients.models import Procedures

import base64


@login_required(login_url="/login/")
def index(request,pk,count):
	f = get_object_or_404(Fle, pk=pk)
	id=f.id_pateint
	
	procedure = Procedures.objects.filter(idd=f.procedure)
	procedure=procedure[0]
	if procedure.flg_stat=='1':
		flg_stations=1
	else:		
		flg_stations=0
		

	name_video=f.fle.url
	name_video=name_video[1:]
	vid=VideoCamera(name_video)
	frame_rate=vid.fr()   


	fles = Fle.objects.filter(id_pateint=id,active_flg_file=True).order_by('pk')
	flg=True
	i=0
	tot=len(fles)
	while flg:
		fl=fles[i]
		if pk==fl.pk:
			if i-1<0:
				bef=False
				bef1=0
			else:
				bef=fles[i-1].pk
				bef1=bef
			if i+1> len(fles)-1:
				nex=False
				nex1=0
			else:
				nex=fles[i+1].pk
				nex1=nex
			flg=False
		i=i+1



	context= {'pk': pk,
			'id_patient':id,
			'url_video':f.root_fle,
			'frame_rate':frame_rate,
			'flg_stations':flg_stations,
			'num_anot':f.num_anot,
			'count':count,
			'bef':bef,
			'bef1':bef1,
			'nex':nex,
			'nex1':nex1,
			'tot':tot,
			'cfile':i}

	if request.method == "POST":
		count=request.POST['currentFrame']
		kwargs = {"pk": pk, "count":count}
		return redirect('paint', **kwargs)

	else:		
		return render(request, 'streamapp/runvideo.html',context)		
			