from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from models.users import User

#flask forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField  # etc.
from wtforms.validators import Email, InputRequired, Length, ValidationError  # etc.
#flask forms

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '$ECRET_key'

db = SQLAlchemy(app)
###########################################################################################

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
    def validate_username(self, field):
        existing_user = User.query.filter_by(username=field.data).first()
        if existing_user:
            raise ValidationError("Username / Email already Registered : Sign In")







###########################################################################################

# Landing page : '/'
@app.route('/')
def home():
    return render_template('home.html')

# Register page : '/register'
@app.route('/register')
def register_user():
    return render_template('register.html')

#Login page : '/login'
@app.route('/login')
def login_user():
    return render_template('login.html')

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)