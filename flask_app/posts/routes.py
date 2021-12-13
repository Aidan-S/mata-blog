from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from flask_mail import Mail, Message

from ..forms import PostForm, TagSearch, NameSearch
from ..models import User, Post
from ..utils import current_time
from .. import mail

posts = Blueprint('posts', __name__)

@posts.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()

    posts = []
    for f in current_user.friends:
        fposts = Post.objects(userStr=f)
        posts.extend(fposts)
            

    if form.validate_on_submit():
        post = Post(
            poster=current_user._get_current_object(),
            userStr = current_user.username,
            content=form.text.data,
            tag=form.tag.data
        )

        sendMsg = current_user.username + " sent: " + form.text.data
        for friends in current_user.friends:
            print(friends)
            msg = Message(sendMsg, recipients=[User.objects(username=friends).first()])
            mail.send(msg)
        
        
        # v = Post.objects.first()
        # v.delete()
        post.save()
        return render_template("index.html", form = form)

    return render_template("index.html", form = form, posts = posts)


