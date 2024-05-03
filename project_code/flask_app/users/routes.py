from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm, SquirrelReviewForm
from ..models import User, SquirrelPost
from ..utils import current_time

users = Blueprint("users", __name__)

""" ************ User Management views ************ """

""" ************ Helper for pictures ************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

    
# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))

    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, extern_id=form.username.data, email=form.email.data, password=hashed_password)
            user.save()
            return redirect(url_for('users.login'))
    return render_template('register.html',form=form)

# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()

            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('users.account'))
            else:
                flash("Failed to log in!")
    return render_template('login.html', form=form)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('movies.index'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():

    squirrel_review_form = SquirrelReviewForm()
    
    if squirrel_review_form.validate_on_submit():
        
        image = squirrel_review_form.picture.data

        # Read the content of the file
        image_bytes = image.read()

        # Encode the bytes using base64
        image_base64 = base64.b64encode(image_bytes).decode()
        
        squirrel_post = SquirrelPost(
            commenter=current_user._get_current_object(),
            content=squirrel_review_form.text.data,
            date=current_time(),
            image=image_base64,
            location=squirrel_review_form.location.data
        )
        squirrel_post.save()

        return redirect(url_for('movies.index'))

    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            current_user.modify(username = update_username_form.username.data)
            current_user.save()

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            # TODO: handle update profile pic form submit
            image = update_profile_pic_form.picture.data
            filename = secure_filename(image.filename)
            content_type = f'images/{filename[-3:]}'

            if current_user.profile_pic.get() is None:
                # user doesn't have a profile picture => add one
                current_user.profile_pic.put(image.stream, content_type=content_type)
            else:
                # user has a profile picture => replace it
                current_user.profile_pic.replace(image.stream, content_type=content_type)
            current_user.save()
            return redirect(url_for('users.account'))
    
    
    # TODO: handle get requests
    
    image = None
    if current_user.profile_pic.get() is not None:
        image_bytes = BytesIO(current_user.profile_pic.read())
        image = base64.b64encode(image_bytes.getvalue()).decode()
    return render_template('account.html', squirrel_review_form = squirrel_review_form, update_username_form = update_username_form, update_profile_pic_form = update_profile_pic_form, image = image)


@users.route("/squirrel-post", methods=["GET", "POST"])
@login_required
def squirrel_post():
    upload_squirrel_form = UploadSquirrelPic()
    if request.method == "POST":
        if upload_squirrel_form.validate_on_submit():
            image = upload_squirrel_form.picture.data

            filename = secure_filename(image.filename)
            content_type = f'images/{filename[-3:]}'

            # Create a new SquirrelPost object and save it to db
            squirrel_post = SquirrelPost()
            squirrel_post.posted_images.put(image.stream, content_type=content_type)
            squirrel_post.save()

            return redirect(url_for('users.squirrel_post'))

    # Get all squirrel posts
    all_squirrel_posts = SquirrelPost.objects()

    return render_template('squirrel_post.html', upload_squirrel_form=upload_squirrel_form, all_squirrel_posts=all_squirrel_posts)
