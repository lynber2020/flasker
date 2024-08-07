from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash



# Create Flask
app = Flask(__name__)
# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:LynBer01@localhost/our_users'


#secret key
app.config['SECRET_KEY'] = " my little secret"
#initialize database
db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, db)



#create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    favorite_color = db.Column(db.String(120))
    email =  db.Column(db.String(120),  unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #do some password !!
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Deleted na")
        
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", 
        form=form,
        name=name,
        our_users=our_users)
        
    except:
        flash("Shockking! My problema!")
        return render_template("add_user.html", 
        form=form, name=name, our_users=our_users)
    


#create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password must Match!!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

#update Database Records
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:    
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
        except: 
            flash("OoOpppss Error!")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template("update.html",
                                form=form,
                                name_to_update=name_to_update,
                                id = id)
        
class PasswordForm(FlaskForm):
    email = StringField("Your Email", validators=[DataRequired()])
    password_hash = StringField("Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create Route


#def index():
 #   return "<h1>Hello World!</h1>"
 
@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #hash password
            hashed_pw = generate_password_hash(form.password_hash.data, "8")
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=form.password_hash.data)    
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash("User added!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
        form=form,
        name=name,
        our_users=our_users)
    

@app.route('/')

def index():
    first_name = "LynBer"
    stuff = "This is bold text"
    
    return render_template("index.html", first_name=first_name)



@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#add tax dec INFORMATION
@app.route('/addTD')
def addTD():
     return render_template("addTD.html")
 
@app.route('/faas')
def faas():
     return render_template("faas.html")
 
 
#Create Password test page
@app.route('/test_pw', methods=['GET','POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    #validate
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        #clear the form
        #form.email.data = ''
        #form.password_hash.data =''
        
       # flash("Successfully Submitted")
        
    return render_template("test_pw.html",
                           email = email,                           
                           password = password,
                           form = form)


#Create name page

@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    #validate
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        
        flash("Successfully Submitted")
        
    return render_template("name.html",
                           name = name,                           
                           form = form)

