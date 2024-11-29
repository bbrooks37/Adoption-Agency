from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, URL, Optional, AnyOf, NumberRange
from flask_debugtoolbar import DebugToolbarExtension
import os
from werkzeug.utils import secure_filename

if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopt.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['UPLOAD_FOLDER'] = './static/uploads'
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    db.init_app(app)
    toolbar.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

db = SQLAlchemy()
toolbar = DebugToolbarExtension()

app = create_app()

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(30), nullable=False)
    photo_url = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)

class AddPetForm(FlaskForm):
    name = StringField('Pet Name', validators=[InputRequired()])
    species = StringField('Species', validators=[InputRequired(), AnyOf(['cat', 'dog', 'porcupine'])])
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30)])
    notes = StringField('Notes', validators=[Optional()])
    available = BooleanField('Available', default=True)

class EditPetForm(FlaskForm):
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    notes = StringField('Notes', validators=[Optional()])
    available = BooleanField('Available', default=True)

# Route to display all pets
@app.route('/')
def home():
    available_pets = Pet.query.filter_by(available=True).all()
    unavailable_pets = Pet.query.filter_by(available=False).all()
    return render_template('home.html', available_pets=available_pets, unavailable_pets=unavailable_pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        new_pet = Pet(**form.data)
        db.session.add(new_pet)
        db.session.commit()
        flash('Pet added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_pet.html', form=form)


@app.route('/list_pets')
def list_pets():
    pets = Pet.query.all()
    for pet in pets:
        print(f'{pet.name} - {pet.species} - {pet.available}')
    return "Check your terminal for the pet list"

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def show_edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash('Pet updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('pet_detail.html', pet=pet, form=form)

if __name__ == '__main__':
    app.run(debug=True)
