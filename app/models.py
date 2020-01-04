from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin ,current_user
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage

from flask_dance.contrib.twitter import make_twitter_blueprint, twitter 
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,nullable=False)
    email = db.Column(db.String(64), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


twitter_blueprint = make_twitter_blueprint(api_key='JwqH7ZkVRf6ijx7mhBj2vHEGI', api_secret='Vkauv9IhKzqxhY9UPuDtcVYMFDQDepDggvIUGn0gEgDXXhJI5q')
github_blueprint = make_github_blueprint(client_id='da040506cead084d7f16', client_secret='bf759d2ea183fff315ce29ef72990b0ab3ebb151')
google_blueprint = make_google_blueprint(client_id="492844928396-3fncmg10ggsg9tfcp0iort43srnu18hj.apps.googleusercontent.com", client_secret="rapC0Iih0QO7znm8co1XKCqD", scope=["profile", "email"])


twitter_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)
google_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)
github_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)

