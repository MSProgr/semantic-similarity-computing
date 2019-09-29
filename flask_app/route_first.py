from flask import render_template,url_for,flash,redirect,request
from flask_app.form import Question,Suggestion
from flask_app.model import Chat
from flask_app.spacy_helper import nlp,nlp_question,rep,ques,cat,find_maxs,tag,get_all_question
from flask_app import app,db

import numpy as np

@app.route("/",methods=["GET","POST"])
def index():
    form = Question()
    suggestion = Suggestion()
    better_index = []
    similarity_result = []
    indexes = []
    if form.validate_on_submit():
        the_question = form.question.data
        if len(the_question.split(" ")) < 3:
            flash("Veuillez Formulez une question correcte","dark")
            return redirect(url_for('index'))
        
        for index,t in enumerate(nlp_question):
            sm = t.similarity(nlp(the_question.lower()))
            if sm >= 0.87:
                similarity_result.append(sm)
                indexes.append(index)
        scores = np.array(similarity_result)
        if scores.size == 0:
            return redirect(url_for("suggest",question=the_question))
        elif scores.size < 3:
            better_index,with_scores = find_maxs(scores,indexes,scores.size)
        else:
            better_index,with_scores = find_maxs(scores,indexes,3)

        all_data = [(rep[i],ques[i],100*float("{0:.3f}".format(j))) for i,j in zip(better_index,with_scores)]

        suggestion.question.data = the_question
        return render_template('test.html',all_data=all_data,the_question=the_question,suggestion=suggestion)        

    return render_template("index.html",form=form,legend='A Propos de Orange et moi')


@app.route("/suggest/<question>",methods=["GET","POST"])
def suggest(question):
    suggestion = Suggestion()
    suggestion.question.data = question
    if suggestion.validate_on_submit():
        rep = (suggestion.reponse.data).split(" ")
        if len(rep) <= 2:
            flash("Merci de suggérer une réponse correct","dark")
            return redirect(url_for('index'))
        chat = Chat(question=suggestion.question.data,reponse=suggestion.reponse.data,categorie=suggestion.categorie.data)
        db.session.add(chat)
        db.session.commit()
        flash("Merci pour votre contribution !","primary")
        return redirect(url_for("index"))

    return render_template("suggestion.html",suggestion=suggestion)


@app.route("/new_suggest",methods=["POST"])
def new_suggest():
    suggestion = Suggestion()
    if suggestion.validate_on_submit():
        rep = (suggestion.reponse.data).split(" ")
        if len(rep) <= 2:
            flash("Merci de suggérer une réponse correct","dark")
            return redirect(url_for('index'))
        chat = Chat(question=suggestion.question.data,reponse=suggestion.reponse.data,categorie=suggestion.categorie.data)
        db.session.add(chat)
        db.session.commit()
        flash("Merci pour votre contribution !","primary")
        return redirect(url_for("index"))
    else:
        flash("Merci de bien voloir suggérer une réponse correcte","dark")
        return redirect(url_for('index')) 
