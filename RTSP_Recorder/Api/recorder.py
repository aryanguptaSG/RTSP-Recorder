import numpy as np
import cv2,os
import threading
from .models import Camera,Recording
from .serializers import RecordingSerializer,CameraSerializer
from django.conf import settings
import datetime


'''#########  This is main function which is responsible for capturing video from given camera'''
def startRecording(file,path,time):
    print("from recorder ",time)
    try:
        ''' here i am changing the type of path for case of webcam capturing'''
        path = int(path)
    except:
        '''if path can not be changed into integer that's means path is a url of either IP_Camera or any video file'''
        pass

    ''' filename is the variable where video will be saved'''
    filename = os.path.join(settings.BASE_DIR,"allRecordings/")+file+"_"+str(time)+".avi"
    filename = filename.replace("\\","/")
    try:
        isnew = True
        camera = Camera.objects.get(name=file)
        serializer = CameraSerializer(camera)
        end_hours = int((serializer.data.get("active_hours")).split("to")[-1][:-2])
        zone = str((serializer.data.get("active_hours")).split("to")[-1][-2:])
        now = int(datetime.datetime.now().hour)
        if zone =="PM" and end_hours!=12:
            end_hours+=12
        elif zone=="AM" and end_hours==12:
            end_hours=0

        anyway = False
        if now>=end_hours:
            anyway=True
        ''' making a instance of videocapture for given path'''
        cap = cv2.VideoCapture(path)

        '''Type of Video'''
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        ''' Here actual capturing will be started '''
        while now<end_hours or anyway:
            now = int(datetime.datetime.now().hour)
            if cap.isOpened():
                ret, frame = cap.read()
                if isnew:
                    h,w,_=frame.shape
                    out = cv2.VideoWriter(filename, fourcc, 25,(w,h))
                    print("Recording Started")
                    isnew=False

                if ret:
                    # frame=cv2.flip(frame,1)
                    out.write(frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    camera = Camera.objects.get(name=file)
                    serializer = CameraSerializer(camera)
                    if not serializer.data.get("status"):
                        break
            else:
                recording = Recording.objects.get(name=file+"_"+time)
                serializer = RecordingSerializer(recording,data ={"status":"corrupt"},partial=True)
                if serializer.is_valid():
                    serializer.save()
                camera = Camera.objects.get(name=file)
                serializer = CameraSerializer(camera)
                serializer = CameraSerializer(camera,data ={"status":False},partial=True)
                if serializer.is_valid():
                    serializer.save()
                print("Wrong path")
                break
        
        ''' Release all   '''
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    except:
        ''' if making a instance of videocapture for given path is falid then video will be corrupted '''
        recording = Recording.objects.get(name=file+"_"+time)
        serializer = RecordingSerializer(recording,data ={"status":"corrupt"},partial=True)
        if serializer.is_valid():
            serializer.save()
        print("Wrong path")

    ''' Here Camera status will be changed to False '''
    camera = Camera.objects.get(name=file)
    serializer = CameraSerializer(camera)
    serializer = CameraSerializer(camera,data ={"status":False},partial=True)
    if serializer.is_valid():
        serializer.save()








