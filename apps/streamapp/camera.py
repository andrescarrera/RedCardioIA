import cv2
class VideoCamera(object):
	def __init__(self,name):
		self.video = cv2.VideoCapture(name)
		self.url= name
		
	def __del__(self):
		self.video.release()

	def tot_frames(self):
		tot=int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))	
		return tot
	
	def fr(self):
		fps = int(self.video.get(cv2.CAP_PROP_FPS))
		return fps
		

	def get_frame(self,count):
		self.video.set(1,count) 
		success, image = self.video.read()
		
		ret, png = cv2.imencode('.png', image)
		return png.tobytes(),image
