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

discord = Blueprint("discord", __name__)

@discord.route("/callback", methods=["GET"])
def call_back():
    return ("Success!")