from flask import Flask, render_template

# Create Flask
app = Flask(__name__)

# Create Route
@app.route('/')

#def index():
 #   return "<h1>Hello World!</h1>"

def index():
    first_name = "LynBer"
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