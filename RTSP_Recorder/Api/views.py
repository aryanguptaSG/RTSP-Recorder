from .models import Camera,Recording
from .serializers import RecordingSerializer,CameraSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .recorder import startRecording
import threading
import datetime,os
from django.conf import settings

'''This is the path of dir where all the recordings will be saved'''
PATH = os.path.join(settings.BASE_DIR,"allRecordings")
PATH = PATH.replace("\\","/")


'''function for starting recording from given camera'''
@api_view(['PUT'])
def start(request):
    name=request.data.get('name',None)
    if name is not None:
        try:
            camera = Camera.objects.get(name=name)
        except:
            return Response("camera not found")
        check = CameraSerializer(camera)
        if check.data.get("status"):
            return Response({"Success":"Camera is already runnig"})
        serializer = CameraSerializer(camera,data ={"status":True},partial=True)
        if serializer.is_valid():
            serializer.save()
            date = str(str(datetime.datetime.now()).split()[0])
            Time = "Time_"+str(str(datetime.datetime.now().hour))+"_Date_"+date
            if addpath(name,Time):
                t = threading.Thread(target=startRecording,args=(name,check.data.get("url"),str(Time)))
                t.start()
                return Response("{name} is Started".format(name=name))
            else:
                return Response("{name} is not Started".format(name=name))
            return Response("{name} is Started".format(name=name))
        else:
            return Response({"error":serializer.errors})

    else:
        return Response("camera not found")


''' function for stopping recording from given camera'''
@api_view(['PUT'])
def stop(request):
    name=request.data.get('name',None)
    if name is not None:
        try:
            camera = Camera.objects.get(name=name)
        except:
            return Response("camera not found")
        serializer = CameraSerializer(camera,data ={"status":False},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("{name} is Stopped".format(name=name))
        else:
            return Response({"error":serializer.errors})

    else:
        return Response("camera not found!")


'''function for retriving status of all/given camera'''
@api_view()
def health_check(request,Name=None):
    if request.method =="GET":
        pythondata = request.data
        name = pythondata.get("name",None)
        if Name and name is None:
            name = Name
        if name is not None and name!="all":
            try:
                camera = Camera.objects.get(name=name)
                serializer = CameraSerializer(camera)
                return Response(serializer.data)
            except:
                return Response("invalid request")
        elif name=="all":
            camera = Camera.objects.all()
            serializer = CameraSerializer(camera,many=True)
            return Response(serializer.data)
        else:
            return Response("invalid request")

'''function to store a list of camera urls to database for recording'''
@csrf_exempt
@api_view(['POST'])
def store_urls(request):
    if request.method =="POST":
        pythondata = request.data
        urls = pythondata.get("urls",None)
        if urls is not None:
            for i in urls:
                try:
                    camera = Camera.objects.get(name=i.get('name'))
                    res = {"Error":"Camera url is allready Present can't insert again"}
                    break
                except:
                    serializer = CameraSerializer(data = i)
                    if serializer.is_valid():
                        serializer.save()
                        res = {"Success":"Camera urls are stored"}
                    else:
                        res = {"Error":serializer.errors}
        else:
            res = {"Error":"data not passed by you"}
        
        return Response(res)





'''retrive all recordings from database'''
@api_view(['GET'])
def getpath(request):
    if request.method =="GET":
        recording = Recording.objects.all()
        serializer = RecordingSerializer(recording,many=True)
        return Response(serializer.data)



'''function for getting Valid and corrupted videos in dictonary formate'''
@api_view(['GET'])
def corrupt_checker(request):
    if request.method =="GET":
        res = dict()
        recording = Recording.objects.filter(status="valid")
        serializer = RecordingSerializer(recording,many=True)
        res["Good Videos"] = serializer.data
        recording = Recording.objects.filter(status="corrupt")
        serializer = RecordingSerializer(recording,many=True)
        res["Corrupted Videos"] = serializer.data
        return Response(res)



'''this function is called only from start function . user can not call it direct'''
def addpath(name,Time):
    filename = name+"_"+str(Time)
    global PATH
    data = {"name":filename,"path":PATH+"/"+filename+".avi","status":"valid","datetime":Time}
    serializer = RecordingSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        res = {"Success":"recording Set"}
        print(res)
        return True
    else:
        res = {"Error":serializer.errors}
        return False

        






    
