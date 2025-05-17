from flask import Flask, render_template, url_for, redirect
from extensions import db
from models.users import User
from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy

#flask forms
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField  # etc.
from wtforms.validators import Email, InputRequired, Length, ValidationError  # etc.
#flask forms

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '$ECRET_key'

# db = SQLAlchemy(app)
###########################################################################################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
#Flask Form Definition
class RegisterForm(FlaskForm):
    username = StringField(
        validators=[
            Email(message="Enter a valid email"),
            InputRequired(message="Email cannot be empty"),
            Length(min=4, max=100)
        ],
        render_kw={"placeholder": "Email"}
    )

    password = PasswordField(
        validators=[
            InputRequired(message="Password cannot be empty"),
            Length(min=4, max=37)
        ],
        render_kw={"placeholder": "Password"}
    )

    submit = SubmitField("REGISTER")
    
    #Validate username uniqueness
    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("Username / Email already Registered : Sign In")

# Now Login Form
class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            Email(message="Enter a valid email"),
            InputRequired(message="Email cannot be empty"),
            Length(min=4, max=100)
        ],
        render_kw={"placeholder": "Email"}
    )

    password = PasswordField(
        validators=[
            InputRequired(message="Password cannot be empty"),
            Length(min=4, max=37)
        ],
        render_kw={"placeholder": "Password"}
    )

    submit = SubmitField("LOGIN")





###########################################################################################
# Landing page : '/'
@app.route('/')
def home():
    return render_template('home.html')

# Register page : '/register'
@app.route('/register', methods=['GET','POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)

#Login page : '/login'
@app.route('/login', methods=['GET','POST'])
def login_user():
    form = LoginForm()
    return render_template('login.html', form=form)


db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)