from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
import os
from .models import User, Tweet, Comment, Like, Follow

urls = Blueprint('urls', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@urls.route('/')
@login_required
def home():
    # query order by date created
    tweets = Tweet.query.order_by(Tweet.date_created.desc()).all()
    likes = Like.query.all()
    liked = []
    comments = Comment.query.all()
    for like in likes:
        if like.user_id == current_user.id:
            liked.append(like.tweet_id)
    return render_template('home.html', tweets=tweets, liked=liked, comments=comments)


@urls.route('/post', methods=['POST', 'GET'])
@login_required
def post():
    if request.method == 'POST':
        text = request.form.get('text')
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        tweet = Tweet(text=text, user_id=current_user.id, image=filename, date_created=db.func.current_timestamp())
        db.session.add(tweet)
        db.session.commit()
        flash('Tweet posted!', category='success')
        return redirect(url_for('urls.post'))
    else:
        posts = Tweet.query.filter_by(user_id=current_user.id).order_by(Tweet.date_created.desc()).all()
        return render_template('post.html', posts=posts)
    

@urls.route('/profile/<int:id>', methods=['POST', 'GET'])
def profile(id):
    if request.method == 'POST':
        pass
    else:
        user = User.query.filter_by(id=id).first()
        followers = len(user.followers)
        following = len(user.following)
        username = user.username
        follower_id = []
        for follower in user.followers:
            follower_id.append(follower.follower_id)
        return render_template('profile.html', user=user, username=username, followers=followers, following=following, tweets=user.tweets, follower_id=follower_id)
    
@urls.route('/like/<int:id>', methods=['POST'])
def like(id):
    like = Like(user_id=current_user.id, tweet_id=id)
    db.session.add(like)
    db.session.commit()
    return redirect(url_for('urls.home'))

@urls.route('/unlike/<int:id>', methods=['POST'])
def unlike(id):
    like = Like.query.filter_by(user_id=current_user.id, tweet_id=id).first()
    db.session.delete(like)
    db.session.commit()
    return redirect(url_for('urls.home'))


@urls.route('/comment/<int:id>', methods=['POST'])
def comment(id):
    text = request.form.get('comment')
    comment = Comment(user_id=current_user.id, tweet_id=id, comment=text, date_created=db.func.current_timestamp())
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('urls.home'))


@urls.route('/follow/<int:id>', methods=['GET'])
def follow(id):
    follow = Follow(follower_id=current_user.id, followed_id=id)
    db.session.add(follow)
    db.session.commit()
    return redirect(url_for('urls.profile', id=id))

@urls.route('/unfollow/<int:id>', methods=['GET'])
def unfollow(id):
    follow = Follow.query.filter_by(follower_id=current_user.id, followed_id=id).first()
    db.session.delete(follow)
    db.session.commit()
    return redirect(url_for('urls.profile', id=id))