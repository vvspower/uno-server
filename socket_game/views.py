from django.shortcuts import render
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from users.models import User
from .models import Room
import socketio
from .serializers import UserSerializer
import time
from .utils import *


all_users = []


sio = socketio.Server(cors_allowed_origins="*")

def get_user_from_access_token(token):
    access_token_obj = AccessToken(token)
    user_id=access_token_obj['user_id']
    user=User.objects.get(id=user_id)
    return user

@sio.event
def connect(sid, environ):
    print('connect', sid)

@sio.event
def disconnect(sid):
    print('disconnect', sid)
    user = User.objects.get(username=sio.get_session(sid)["username"])
    rooms = Room.objects.filter(participants__username=user.username)
    for room in rooms:
        room.participants.remove(user)
        users_in_room = room.participants.all()
        serializer = UserSerializer(users_in_room, many=True)
        sio.emit("room_updates", serializer.data , room=room.room)
    all_users.remove(user)
    serializer = UserSerializer(all_users, many=True)
    sio.emit("all_users_connected", {"all_users" : serializer.data})
    

@sio.event
def enter_home(sid, data):
    return data["username"] + "is online"

@sio.event
def initialize(sid , data):
    try:
        user = get_user_from_access_token(data["token"])
        sio.save_session(sid, {'username' : str(user.username)})
        if user in all_users:
            return
        else:
            user = User.objects.get(username=sio.get_session(sid)["username"])
            all_users.append(user)
        serializer = UserSerializer(all_users, many=True)
        sio.emit("all_users_connected", {"all_users" : serializer.data})
        return "authenticated"
    except TokenError:
        return "token error"
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

@sio.event
def create_room(sid, data):
    session = sio.get_session(sid)
    user = User.objects.get(username=session["username"])
    sio.enter_room(sid, data["room"])
    room = Room.objects.create(room=data["room"])
    room.participants.add(user)
    room.save()
    print("here 1")
    return data["room"]

    

@sio.event
def join_room(sid, data):
    users = []
    try:
        session = sio.get_session(sid)
        user = User.objects.get(username=session["username"])
        room = Room.objects.get(room=data["room"])
        participants = room.participants.all()
        for participant in participants:
            if participant.username == session["username"]:
                sio.enter_room(sid, data["room"])
                users = list(participants)
                serializer = UserSerializer(users, many=True)
                sio.emit("room_updates", serializer.data , room=data["room"])
                break
            else:
                sio.enter_room(sid, data["room"])
                room.participants.add(user)
                users = list(Room.objects.get(room=data["room"]).participants.all())
                serializer = UserSerializer(users, many=True)
                sio.emit("room_updates", serializer.data , room=data["room"])
                break
    except Exception as ex:
        print(ex)

@sio.event
def leave_room(sid, data):
    try:
        session = sio.get_session(sid)
        user = User.objects.get(username=session["username"])
        room = Room.objects.get(room=data["room"])
        sio.leave_room(sid, data['room'])
        room.participants.remove(user)
        users = list(Room.objects.get(room=data["room"]).participants.all())
        if len(users) == 0:
            room.delete()
            return 'success'
        else:
            serializer = UserSerializer(users, many=True)
            sio.emit("room_updates", serializer.data , room=data["room"])
        return 'success'
    except Exception as ex:
        print('ex')
        return 'failed'        



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# start game

@sio.event
def start_game(sid, data):
    try:
        room = Room.objects.get(room=data["room"])
        sio.emit('start_game', {"time" : "starting" }, room=data["room"])
        time.sleep(3)
        room.game_active = True
        sio.emit('start_game', {"time" : "started" }, room=data["room"])
    except Exception as ex:
        pass


@sio.event(namespace="/game")
def assign_cards(sid, data):
    deck = shuffle_deck()
    player_names = []
    for user in data["users"]:
        print(user)
        player_names.append(user["username"])
    print(player_names)
    deck = deal_cards(deck , player_names)
    return deck






