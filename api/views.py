from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def get_csrf_token(request):
    token = get_token(request)
    return Response({'csrfToken': token})

@csrf_exempt
@api_view(['POST'])
def signup(request):
    try:
        username = request.data.get('username')
        color = request.data.get('color')
        user = CustomUser.objects.filter(username=username).first()
        if user:
            login(request, user)
            return Response({'data': [], 'code': 200, 'message': "Already exists!" })
        else:
            user = CustomUser.objects.create(username=username, color=color)
            user.room = None
            user.save()
            login(request, user)
            return Response({'data': [], 'code': 200, 'message': "User created!" })
    except Exception as e:
        return Response({'data': [], 'code': 500, 'message': "Internal Server Error" })

@api_view(['POST'])
def create_room(request):
    try:
        #create room
        name = request.data.get('name')
        capacity = request.data.get('capacity')
        public = request.data.get('public')
        room = Room.objects.create(name=name, max_capacity=int(capacity), public=public)
        room.save()
        user = request.user
        user.room = room
        user.host = True
        user.joined_at = timezone.now()
        user.save()
        # delete empty rooms
        rooms = Room.objects.all()
        empty_rooms = []
        for room in rooms:
            joined = CustomUser.objects.filter(room=room)
            if not joined:
                empty_rooms.append(room)
        
        for i in empty_rooms:
            i.delete()
        return Response({'data':{'name':name,'host':user.username,'capacity':capacity, 'public':public}, 'code':200, 'message':"Room created!" })
    except:
        return Response({'data':[], 'code':500, 'message':"Internal Server Error" })

@api_view(['GET'])
def join_room(request):
    try:
        user = request.user
        code = str(request.GET.get('code')).upper()
        room = Room.objects.filter(code=code).first()
        if room:
            user.room = room  
            user.joined_at = timezone.now()
            user.save()
            return Response({'data':[], 'code':200, 'message':"Joined the Room successfully" })   
        else:    
            return Response({'data':[], 'code':200, 'message':"Incorrect Room Code" })
    except:
        return Response({'data':[], 'code':500, 'message':"Internal Server Error" })

@api_view(['GET'])
def leave_room(request):
    try:
        user = request.user
        room = user.room
        user.host = False
        user.room = None
        user.save()
        remaining_people = CustomUser.objects.filter(room = room).order_by('joined_at')
        new_host = remaining_people[0]
        new_host.host = True
        new_host.save()
        return Response({'data':[], 'code':200, 'message':"Left the Room successfully" })
    except:
        return Response({'data':[], 'code':500, 'message':"Internal Server Error" })

@api_view(['GET'])
def get_rooms(request):
    try:
        rooms = Room.objects.filter(public=True)
        data = []
        for room in rooms:
            joined = CustomUser.objects.filter(room = room)
            data.append({'name':room.name,'joined':len(joined),'max_capacity':room.max_capacity})
        
        return Response({'data':data, 'code':200, 'message':"Rooms Fetched Successfully" })
    except:
        return Response({'data':[], 'code':500, 'message':"Internal Server Error" })
    

