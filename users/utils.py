# helper functions
import requests
import cloudinary
import cloudinary.uploader
from tenacity import *
import random
# import retry
import os
from rest_framework_simplejwt.tokens import AccessToken
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

JWT_authenticator = JWTAuthentication()

cloudinary.config(
  cloud_name = "codenames",
  api_key = "672829769414271",
  api_secret = "dRTgF4eKnD6Bwak81dITpcSPYjI"
)



@retry(wait=wait_fixed(5) , stop=stop_after_attempt(3))
def upload_profile_picture(username):
    background_colors = ["b6e3f4", "c0aede" , "d1d4f9", "ffd5dc" , "ffdfbf"]
    try:
        response = requests.get(f"https://api.dicebear.com/5.x/adventurer/png?seed={username}&backgroundColor={background_colors[random.randint(0,4)]}")
        if response.status_code == 200:
            with open('image.png', "wb") as f:
                f.write(response.content)
        response = cloudinary.uploader.upload("image.png")
        if response["url"] == None:
            raise Exception("maximum number of retries")
        if os.path.exists("image.png"):
            os.remove("image.png")
        return response["url"]
    except Exception as ex:
        print("something went wrong") 

    

def get_user_from_request(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        user , token = response
        user = User.objects.get(id=token["user_id"])
        return user
    else:
        raise Exception("no token is provided in the header or the header is missing")
    

