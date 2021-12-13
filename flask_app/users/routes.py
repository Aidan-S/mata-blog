from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import TagSearch, NameSearch, RegistrationForm, LoginForm
from ..models import User, Post

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("posts.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("posts.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users.friends"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("posts.index"))


@users.route("/friends", methods=["GET", "POST"])
@login_required
def friends():
    posts = []
    for f in current_user.friends:
        fposts = Post.objects(userStr=f)
        posts.extend(fposts)
            

    tagForm = TagSearch()
    nameForm = NameSearch()


    if tagForm.validate_on_submit():
        tagPosts = Post.objects(tag=tagForm.search_query)
        return render_template("tags.html", tagPosts = tagPosts)


    if nameForm.validate_on_submit():
        lst = current_user.friends
        newFriend = User.objects(username=nameForm.search_query).first()
        lst.append(newFriend)
        current_user.modify(friends=lst)

        return redirect(url_for("posts.index"))


    return render_template("friends.html", posts = posts, tagForm = tagForm, nameForm = nameForm)
