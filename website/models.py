from . import db
from flask_login import UserMixin

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    tweets = db.relationship('Tweet')
    following = db.relationship('Follow', foreign_keys=[Follow.follower_id])
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id])


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    date_created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    image = db.Column(db.String(300))
    comments = db.relationship('Comment')
    likes = db.relationship('Like')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(300))
    date_created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
    user = db.relationship('User')


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))



    