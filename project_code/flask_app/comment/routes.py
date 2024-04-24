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

comment = Blueprint("comment", __name__)

@comment.route("/post/<post_id>", methods=["GET", "POST"])
def comment_page(post_id):
    # Convert the string representation of ObjectId to ObjectId
    post_id_obj = ObjectId(post_id)

    # Retrieve the SquirrelPost document with the given _id
    squirrel_post = SquirrelPost.objects.get(id=post_id_obj)

    form = CommentForm()
    if form.validate_on_submit():

        cmter = current_user._get_current_object()
        image = cmter.profile_pic
        image_base64 = None

        if image:
            # Read the content of the file
            image_bytes = image.read()
            # Encode the bytes using base64
            image_base64 = base64.b64encode(image_bytes).decode()

        comment = Comment(
            commenter=current_user._get_current_object(),
            commenter_profile_pic = image_base64,
            content=form.text.data,
            date=current_time()
        )
        comment.save()

        # Append the newly created comment to the comments list of squirrel_post
        squirrel_post.comments.append(comment)
        squirrel_post.save()
        
    return render_template("comment.html", squirrel_post=squirrel_post, form = form)