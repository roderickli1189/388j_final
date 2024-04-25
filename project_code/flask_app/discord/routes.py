import base64,io
from io import BytesIO
from flask_login import current_user
from flask import Blueprint, render_template, url_for, redirect, request, flash
from bson import ObjectId
from .. import movie_client
from ..forms import MovieReviewForm, SearchForm, CommentForm
from ..models import User, Review, SquirrelPost, Comment
from ..utils import current_time
from flask_login import current_user, login_required, login_user, logout_user
import os, requests

discord = Blueprint("discord", __name__)

API_ENDPOINT = 'https://discord.com/api/v10'

@discord.route("/callback", methods=["GET"])
def call_back():
    #got the code back from user allowing the authorization
    code = request.args['code']
    data = {
        'client_id': '1232516161783074857',
        'client_secret': "shee3vVoWnrFsKuhgpJufmM11sTYKGxG",
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:8000/callback'
        #'http://127.0.0.1:8000/callback'
        #'https://388j-final.vercel.app/callback'
    }
    
    #now sending that data back to discord to get access token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    resp = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    json = resp.json()
    access_token = json['access_token']
    
    #now with access_token we are going to access user data
    new_headers = {"Authorization": f"Bearer {access_token}"}
    resp2 = requests.get("https://discord.com/api/oauth2/@me", headers=new_headers)
    
    if resp2.status_code == 200:
        user_info = resp2.json()
        username = user_info['user']['username']
        discord_user_id = user_info['user']['id']

        user = User.objects(discord_id=discord_user_id).first()
        if not user:
            user = User(username=username, discord_id=discord_user_id)
            user.save()
        
        login_user(user)
        return redirect(url_for("users.account"))
    else:
        return render_template("404.html")