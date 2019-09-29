from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError




class Question(FlaskForm):
    question = TextAreaField("Votre Question", validators=[DataRequired(),Length(min=5)])
    submit = SubmitField("Similarité")


class Suggestion(FlaskForm):
	question = TextAreaField("Question", validators=[DataRequired(),Length(min=5)])
	reponse = TextAreaField("Réponse",validators=[DataRequired(),Length(min=10)])
	categorie = SelectField("Catégorie",choices=[('Offres mobiles',"Offres Mobile"),
		('Terminaux et applications',"Terminaux et applications"),
		('Internet et fixe','Internet et fixe'),('Internet mobile','Internet mobile'),
		('Orange Money','Orange Money'),('Entre nous','Entre nous'),
		('Tutoriel','Tutoriel'),('Bienvenue','Bienvenue'),("TV d'orange et contenus","TV d'orange et contenus"),('TVO','TVO')])
	submit = SubmitField("envoyer")
