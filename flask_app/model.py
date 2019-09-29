from flask_app import db

class Chat(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	question = db.Column(db.Text,nullable=False)
	reponse = db.Column(db.Text,nullable=False)
	categorie = db.Column(db.String(20),nullable=False)