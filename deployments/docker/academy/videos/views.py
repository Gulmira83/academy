from django.shortcuts import render
from videos.vimeo import Vimeo
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from videos.models import Video, VideoTopic
from main.models import Feature
from django.contrib.auth.models import User

@login_required
def index(request):

    user = User.objects.get(username=request.user.username)
    feature = Feature.objects.filter(user=user.id).first()

    access = "False"
    if feature.feature_type == "Basic":
        access = "False"
        return render(request, 'videos.html', {'access':access})

    else:
        access = "True"
        result = Video.objects.all()
        return render(request, 'videos.html', {'videos': result, 'access':access})
    


@login_required
def topics(request, topic=None):

    user = User.objects.get(username=request.user.username)
    feature = Feature.objects.filter(user=user.id).first()

    access = "False"

    if feature.feature_type == "Basic":
        access = "False"
        return render(request, 'topics.html', {'access':access})
    
    else:
        access = "True"
    

        topics = VideoTopic.objects.all()

        if topic is not None:
            
            videos = Video.objects.filter(topic__id=topic)
            if not Video.objects.filter(topic__id=topic).exists():

                if Video.objects.filter(id=topic).exists():
                    single_video = Video.objects.get(id=topic)
                    return render(request, 'one-video.html', {'video': single_video})
                
            return render(request, 'topics.html', {'table_data': videos,'access':access})
    
    

    return render(request, 'topics.html', {'table_data': topics,'access':access})
