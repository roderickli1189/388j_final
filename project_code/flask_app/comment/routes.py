import base64,io
from io import BytesIO
from flask_login import current_user
from flask import Blueprint, render_template, url_for, redirect, request, flash
from bson import ObjectId
from .. import movie_client
from ..forms import MovieReviewForm, SearchForm, CommentForm
from ..models import User, Review, SquirrelPost
from ..utils import current_time

@comment.route("/post/<post_id>", methods=["GET", "POST"])
def comment_page(post_id):
    # Convert the string representation of ObjectId to ObjectId
    post_id_obj = ObjectId(post_id)

    # Retrieve the SquirrelPost document with the given _id
    squirrel_post = SquirrelPost.objects.get(id=post_id_obj)

    form = CommentForm()

    return render_template("comment.html", squirrel_post=squirrel_post, form = form)