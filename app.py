import os
from flask import Flask,render_template,url_for,request, flash, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user,login_required


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://noxhshxfmwjrvf:c7fd0458f613a81920db1679bd7c9d8833d7bc0c69460c71d6bac3758d05d20a@ec2-34-250-102-242.eu-west-1.compute.amazonaws.com:5432/df7spnhmsrkmu2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_PRE_PING'] = True
##


db = SQLAlchemy(app)

migrate = Migrate(app,db)



from flask_login import LoginManager
###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "/login"




########################################

class Vendor(db.Model):

	__tablename__ = 'vendors'

	id = db.Column(db.Integer,primary_key=True)
	name= db.Column(db.Text)
	food= db.Column(db.Text)
	price= db.Column(db.Integer)
	location = db.Column(db.Text)

	def __init__(self,name,food,price,location):
		self.name = name
		self.food = food
		self.price = price
		self.location = location


	def __repr__(self):
		return f"{self.name} is selling {self.food} for {self.price} eur. Location: {self.location}"





from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.Text,nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.
    posts = db.relationship('BlogPost', backref='author', lazy=True)
    comments = db.relationship('Comment',backref='user',lazy=True)
    likes = db.relationship('Like',backref='user',lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"

class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    # Setup the relationship to the User table
    users = db.relationship(User, backref='blogpost',uselist=False)

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text,nullable=False)
    text = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text)
    contact = db.Column(db.Text)

    comments = db.relationship('Comment', backref='blogpost', lazy='dynamic')
    likes = db.relationship('Like',backref='blogpost',lazy=True)

    

    def __init__(self, title, text, location, user_id,picture,contact):
        self.title = title
        self.text = text
        self.location =location
        self.user_id =user_id
        self.picture =picture
        self.contact =contact

    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    author = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('blog_post.id'))


    def __repr__(self):
        return f"comment id: {self.id}"


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    author  = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('blog_post.id'))





# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)
admin.add_view(ModelView(Vendor, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Like, db.session))


@app.route("/", methods = ['GET','POST'])
def home():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=9)


    return render_template('home.html',blog_posts=blog_posts)






from flask_wtf.file import FileField, FileAllowed

class BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    picture = FileField('Add images', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    contact = StringField('Contact No:', validators=[DataRequired()])
    
    submit = SubmitField('BlogPost')




@app.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_blog_pic(form.picture.data,username,form.title.data)

            new_number = "+353" + form.contact.data[1:]
            print(new_number)

            blog_post = BlogPost(title=form.title.data,
                                 text=form.text.data,
                                 location=form.location.data,
                                 user_id=current_user.id,
                                 picture= pic,
                                 contact=new_number
                                 )

            db.session.add(blog_post)
            db.session.commit()
            flash("Blog Post Created!")
            return redirect(url_for('home'))
        else:
            flash("Must upload a picture!")


    return render_template('create_post.html',form=form)






class AddComment(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    text = TextAreaField('Add new comment:', validators=[DataRequired()])
    submit = SubmitField('Comment')



# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@app.route('/<int:blog_post_id>',methods=['GET','POST'])
def blog_post(blog_post_id):

    page = request.args.get('page', 1, type=int)

    form = AddComment()
    if form.validate_on_submit():

        if current_user.is_anonymous:
            comment = Comment(text=form.text.data,
                              post_id=blog_post_id)
            db.session.add(comment)
            db.session.commit()

        else:
            comment = Comment(text=form.text.data,
                              post_id=blog_post_id,
                              author=current_user.id)
            db.session.add(comment)
            db.session.commit()            

        return redirect(url_for('blog_post',blog_post_id=blog_post_id))

    # grab the requested blog post by id number or return 404
    all_comments = Comment.query.order_by(Comment.id.desc()).paginate(page=page, per_page=3)
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',name=blog_post.author,post=blog_post, form=form,all_comments=all_comments)



@app.route("/<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():


        if form.picture.data:
            username = current_user.username
            pic = add_blog_pic(form.picture.data,username,form.title.data)

            blog_post.picture = pic
            blog_post.title = form.title.data
            blog_post.text = form.text.data
            blog_post.location = form.location.data
            db.session.commit()
            flash('Post Updated!')
            return redirect(url_for('blog_post', blog_post_id=blog_post.id))


        else:
            blog_post.title = form.title.data
            blog_post.text = form.text.data
            blog_post.location = form.location.data

            db.session.commit()
            flash('Post Updated!')
            return redirect(url_for('blog_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        form.location.data = blog_post.location
        form.contact.data = blog_post.contact


    return render_template('create_post.html', title='Update',
                           form=form)


@app.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    delete_blob("pasarmalamdublin","blog_pics/"+blog_post.picture)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted!')
    return redirect(url_for('home'))




@app.route("/like-post/<post_id>" , methods = ['POST'])
@login_required
def like(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)

    elif like:
        db.session.delete(like)
        db.session.commit()

    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})



















# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')



def SendEmail(newuser,newusername):
    import smtplib
    smtp_object = smtplib.SMTP('smtp.gmail.com',587)
    smtp_object.ehlo()
    smtp_object.starttls()

    email = "pasarmalamdublin@gmail.com"
    password = "rpacdvvjbgqqpubh"
    smtp_object.login(email,password)


    from_address = email
    to_address = newuser
    subject = "New User Registration"
    message = "Hi "+newusername + ",\n \n Welcome to Pasar Malam Dublin. \n Your account has been created. Thank you for registering. \n \n Admin Pasar Malam"

    msg = "Subject: " +subject+'\n'+message
    smtp_object.sendmail(from_address,to_address,msg)
    smtp_object.quit()
    print("email sent successfully!")




from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()


    if form.validate_on_submit():

        if " " in form.username.data:
            flash("Username must not have space.")

        else:    
            try:
                form.check_username(form.username)
                form.check_email(form.email)

                user = User(email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)

                db.session.add(user)
                db.session.commit()

                SendEmail(form.email.data,form.username.data)

                flash('Thanks for registering! Now you can login!')
                return redirect(url_for('login'))
            
            except ValidationError as e:
                flash("Sorry, username or email has been registered already!")


    return render_template('register.html', form=form)





@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(username=form.username.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not



        if user is None:
            flash("username does not exist!")

        elif user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully!')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('home')

            return redirect(next)

        else:
        	flash("incorrect password!")

    return render_template('login.html', form=form)






@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@app.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)


from PIL import Image,ImageOps

from flask import url_for, current_app

def add_profile_pic(pic_upload,username):

    filename = pic_upload.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    storage_filename = str(username) + '.' +ext_type
    
    filepath = os.path.join(current_app.root_path, 'static/profile_pics', storage_filename)

    # Play Around with this size.
    output_size = (200, 200)

    # Open the picture and save it
    pic = Image.open(pic_upload)

    fixed_image = ImageOps.exif_transpose(pic)

    fixed_image.thumbnail(output_size)
    fixed_image.save(filepath)

    upload_blob("pasarmalamdublin",filepath,"profile_pics/"+storage_filename)

    return storage_filename


def add_blog_pic(pic_upload,username,title):


    try:
        filename = pic_upload.filename
        # Grab extension type .jpg or .png
        ext_type = filename.split('.')[-1]
        storage_filename = str(username)+'-' +str(title[:10]) + '.png'
        
        filepath = os.path.join(current_app.root_path, 'static/blog_pics', storage_filename)

        # Play Around with this size.
        output_size = (600, 600)

        # Open the picture and save it
        pic = Image.open(pic_upload)
        fixed_image = ImageOps.exif_transpose(pic)


        fixed_image.thumbnail(output_size)
        fixed_image.save(filepath)

        upload_blob("pasarmalamdublin",filepath,"blog_pics/"+storage_filename)


        return storage_filename


    except Exception as e:
        print(e)














os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =basedir+'/pasarmalamdublin-4b5c383a9704.json'
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)


    # Upload the new object
    blob = bucket.blob(destination_blob_name)
    
    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0


    try:
        delete_blob(bucket_name,destination_blob_name)
    
    except Exception as e:
        print(e)
        pass


    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )




def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    generation_match_precondition = None

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to delete is aborted if the object's
    # generation number does not match your precondition.
    blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
    generation_match_precondition = blob.generation

    blob.delete(if_generation_match=generation_match_precondition)

    print(f"Blob {blob_name} deleted.")


























@app.route("/maps", methods = ['GET','POST'])
def maps():
	return render_template('maps.html')



@app.route("/snakegame", methods = ['GET','POST'])
def snakegame():
	return render_template('snakegame.html')


@app.route("/stackgame", methods = ['GET','POST'])
def stackgame():
    return render_template('stackgame.html')


@app.route("/flappybird", methods = ['GET','POST'])
def flappybird():
    return render_template('flappybird.html')



@app.route("/millionringgit", methods = ['GET','POST'])
def millionringgit():
    return render_template('millionringgit.html')







@app.errorhandler(404)
def error_404(error):
    '''
    Error for pages not found.
    '''
    # Notice how we return a tuple!
    return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(error):
    '''
    Error for trying to access something which is forbidden.
    Such as trying to update someone else's blog post.
    '''
    # Notice how we return a tuple!
    return render_template('403.html'), 403


if __name__ == '__main__':
	app.run(debug = True)








