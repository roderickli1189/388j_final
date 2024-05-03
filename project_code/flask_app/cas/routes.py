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

cas = Blueprint("cas", __name__)

@cas.route("/cascallback")
def cascallback():
    
    ticket = request.args['ticket']
    resp = requests.get("https://shib.idm.umd.edu/shibboleth-idp/profile/cas/serviceValidate", params={"service":"https://388j-final.vercel.app/cascallback","ticket":ticket})
    r = xmltodict.parse(resp.content)

    
    if 'cas:authenticationSuccess' in r['cas:serviceResponse']:
        username = r['cas:serviceResponse']['cas:authenticationSuccess']['cas:user']
        extern_user_id = r['cas:serviceResponse']['cas:authenticationSuccess']['cas:user']
        return "success"
        
        '''user = User.objects(extern_id=extern_user_id).first()
        if not user:
            user = User(username=username, extern_id=extern_user_id)
            user.save()
        
        login_user(user)
        return redirect(url_for("users.account"))'''
    else:
        return "faliure"

'''@cas.route("/caslogout")
@login_required
def caslogout():
    logout_user()
    return redirect("https://shib.idm.umd.edu/shibboleth-idp/profile/cas/logout?service=https%3A%2F%2Fhttps://388j-final.vercel.app/%2F")'''