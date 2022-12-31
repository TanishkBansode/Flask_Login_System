from flask_login import current_user
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# Set up the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Set up the database
db = SQLAlchemy(app)


# Define the user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)


# Define the login form with validation rules
class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class SignUpForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


# Define the logout route
@app.route("/logout")
@login_required
def logout():
    if current_user is not None:
        logout_user()
        flash("You have been logged out")
        return redirect(url_for("login"))
    else:
        flash("Login first!")


# Define the starting route
@app.route("/")
def start():
    return """
<html>
  <head>
    <title>Index</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.css">
      <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.js"></script>  
  </head>
  <body style="text-align: center">
  <div style="margin-top: 50px;" class="ui container">
    <h1 class="ui center aligned header">Welcome to Login System</h1>
    <a class="ui center aligned blue button" href="http://127.0.0.1:5000/signup">Signup</a>
    <a class="ui center aligned blue button" href="http://127.0.0.1:5000/login">Login</a>
  </div>
  </body>
</html>
    """


# Define the login route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the user exists in the database
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            # Log in the user and redirect to the protected page
            login_user(user)
            flash(f"Welcome, {user.username}!")
            return redirect(url_for("main_page"))
        else:
            return """
<html>
  <head>
    <title>Try again</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.css">
      <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.js"></script>  
  </head>
  <body style="text-align: center">
  <div style="margin-top: 50px;" class="ui container">
    <h2 class="ui red block header">Maybe password or username is incorrect.Please try again...</h2>
    <a class="ui green button" href="http://127.0.0.1:5000/signup">Signup</a>
    <a class="ui green button" href="http://127.0.0.1:5000/login">Login</a>
    </div>
  </body>
</html>


    """
    return render_template("login.html", form=form)


# Define the login route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form2 = SignUpForm()
    if form2.validate_on_submit():
        # Check if the user exists in the database
        user = User.query.filter_by(username=form2.username.data).first()
        if user is not None and user.password == form2.password.data:
            # Log in the user and redirect to the protected page
            login_user(user)
            flash(f"Welcome, {user.username}!")
            return redirect(url_for("main_page"))
        elif user is not None and user.password != form2.password.data:
            return """
<html>
  <head>
    <title>Try again</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.css">
      <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.js"></script>  
  </head>
  <body style="text-align: center">
  <div style="margin-top: 50px;" class="ui container">
    <h1 class="ui red block header">There's already an account. Try another one...</h1>
    <a class="ui green button" href="http://127.0.0.1:5000/signup">Signup</a>
    <a class="ui green button" href="http://127.0.0.1:5000/login">Login</a>
    </div>
  </body>
</html>


    """
        else:
            with app.app_context():
                db.create_all()
                db.session.add(
                    User(
                        username=str(form2.username.data),
                        password=str(form2.password.data),
                    )
                )
                db.session.commit()
            # Log in the user and redirect to the protected page
            return redirect(url_for("login"))
    return render_template("signup.html", form=form2)


# The user_loader callback is a function that is called to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Define the protected route
@app.route("/main_page")
@login_required
def main_page():
    if current_user.is_authenticated:
        pass
    else:
        print("Don't do that")
        redirect(url_for("login"))
    return """
<html>
<head>
    <title>Main Page</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.css">
      <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.js"></script>  
    <script>
        const confirmAction = () => {
            const response = confirm("Are you sure you want to logout?");

            if (response) {
                window.location.replace("http://127.0.0.1:5000/logout");
            } else {
                alert("OK");
            }
        }
    </script>
    <style>
     button{
     position: relative;
     bottom: 90px;
     left: 95px     
          }
     h1{
     position:relative;
     bottom: 16px;
          }
    </style>
</head>
<body style="text-align: center">
  <div style="margin-top: 50px;" class="ui container">
    <h1 class="ui center aligned block header">
    You are logged in!</h1>
    <button class="negative ui right floated button" onclick="confirmAction()">
        Logout?
    </button>
    </div>
</body>
</html>


    """


with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    # App runs
    app.run()
