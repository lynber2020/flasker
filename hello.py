from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



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


    #Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


#create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")

#update Database Records
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorit_color']
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
                                name_to_update=name_to_update)
            
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
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color)    
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
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

