from app import app, db , login_manager
from app.models import User, Post
from app.forms import PostForm , ChangeUsername
from flask import render_template, flash , redirect , url_for ,request
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter 
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
# from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.consumer import oauth_authorized
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm.exc import NoResultFound
import requests

twitter_blueprint = make_twitter_blueprint(api_key='JwqH7ZkVRf6ijx7mhBj2vHEGI', api_secret='Vkauv9IhKzqxhY9UPuDtcVYMFDQDepDggvIUGn0gEgDXXhJI5q')
github_blueprint = make_github_blueprint(client_id='da040506cead084d7f16', client_secret='bf759d2ea183fff315ce29ef72990b0ab3ebb151')
google_blueprint = make_google_blueprint(client_id="492844928396-3fncmg10ggsg9tfcp0iort43srnu18hj.apps.googleusercontent.com", client_secret="rapC0Iih0QO7znm8co1XKCqD", scope=["profile", "email"])

app.register_blueprint(github_blueprint, url_prefix="/github_login")
app.register_blueprint(google_blueprint, url_prefix="/google_login")
app.register_blueprint(twitter_blueprint, url_prefix="/twitter_login")
# app.register_blueprint(facebook_blueprint, url_prefix="/facebook_login")

@app.route('/', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    username_form = ChangeUsername()
    if username_form.validate_on_submit():
        l = []
        for i in User.query.order_by(User.username).all():
            l.append(i.username)
        if username_form.new_name.data not in l:
            current_user.username = username_form.new_name.data
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash("Username already exists", 'danger')
            return redirect(url_for('home'))

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("html/home.html", title='home', posts=posts, username_form=username_form)

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('html/user_posts.html', posts=posts, user=user)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have logged out", 'info')
    return redirect(url_for("home"))

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'info')
        return redirect(url_for('home'))
    return render_template("html/create_post.html", title = 'Create Post', form=form, legend='Create Post')

@app.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    print(post_id)
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'info')
    return redirect(url_for('home'))

# login routes
@app.route('/github')
def github_login():
    if (github.authorized == False) or (current_user.is_authenticated == False):
        return redirect(url_for("github.login"))
    resp = github.get("/user")

    if github.authorized == True:
        return "You are @{login} on GitHub".format(login=resp.json()["login"])

@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):

    account_info = blueprint.session.get("/user")

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json["login"]

        query = User.query.filter_by(username=username)

        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        login_user(user)




@app.route("/google")
def google_login():
    if (google.authorized == False) or (current_user.is_authenticated == False):
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    email=resp.json()["email"]
    username = email.split("@")[0]

    if google.authorized == True:
        return "You are {} on Google".format(email)

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):

    account_info = blueprint.session.get("/oauth2/v2/userinfo")

    if account_info.ok:
        account_info_json = account_info.json()
        email = account_info_json["email"]
        username = email.split("@")[0]

        query = User.query.filter_by(email=email)

        try:
            user = query.one()
        except NoResultFound:
            user = User(username = username, email=email)
            db.session.add(user)
            db.session.commit()

        login_user(user)



@app.route("/twitter")
def twitter_login():
    if (twitter.authorized == False) or (current_user.is_authenticated == False):
        return redirect(url_for('twitter.login'))

    account_info = twitter.get("account/settings.json")
    account_info_json = account_info.json()

    if twitter.authorized == True:
        return "You are @{} on Twitter".format(account_info_json["screen_name"])

@oauth_authorized.connect_via(twitter_blueprint)
def twitter_logged_in(blueprint, token):

    account_info = blueprint.session.get('account/settings.json')

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json['screen_name']

        query = User.query.filter_by(username=username)

        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        login_user(user)
