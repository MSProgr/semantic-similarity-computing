from flask import render_template,url_for,flash,redirect,request
from flask_app.form import Question,Suggestion
from flask_app.model import Chat
from flask_app.spacy_helper import nlp,nlp_question,rep,ques,cat
from flask_app import app,db

import numpy as np

@app.route("/",methods=["GET","POST"])
def index():
    form = Question()
    suggestion = Suggestion()
    similarity_result = np.array([])
    if form.validate_on_submit():
        the_question = form.question.data
        if len(the_question.split(" ")) < 3:
            flash("Veuillez Formulez une question correcte","dark")
            return redirect(url_for('index'))
        
        for index,t in enumerate(nlp_question):
            sm = t.similarity(nlp(the_question.lower()))
            similarity_result = np.append(similarity_result,sm)

        best_score,best_index = similarity_result.max(), similarity_result.argmax()
        if best_score < 0.87:
            return redirect(url_for("suggest",question=the_question))

        suggestion.question.data = the_question
        return render_template('test.html',reponse=rep[best_index],ind=best_index,question=the_question, q_sim=ques[best_index],
            similarity=100*float("{0:.3f}".format(best_score)),
            suggestion=suggestion)        

    return render_template("index.html",form=form,legend='A Propos de Orange et moi')


@app.route("/suggest/<question>",methods=["GET","POST"])
def suggest(question):
    suggestion = Suggestion()
    suggestion.question.data = question
    if suggestion.validate_on_submit():
        rep_sugg = (suggestion.reponse.data).split(" ")
        if len(rep_sugg) <= 2:
            flash("Merci de suggérer une réponse correct","dark")
            return redirect(url_for('index'))
        chat = Chat(question=suggestion.question.data,reponse=suggestion.reponse.data,categorie=suggestion.categorie.data)
        db.session.add(chat)
        db.session.commit()
        ques.append(suggestion.question.data)
        rep.append(suggestion.reponse.data)
        cat.append(suggestion.categorie.data)
        nlp_question.append(nlp((suggestion.question.data).lower()))
        flash("Merci pour votre contribution !","primary")
        return redirect(url_for("index"))

    return render_template("suggestion.html",suggestion=suggestion)


@app.route("/new_suggest",methods=["POST"])
def new_suggest():
    suggestion = Suggestion()
    if suggestion.validate_on_submit():
        rep_sug = (suggestion.reponse.data).split(" ")
        if len(rep_sug) <= 2:
            flash("Merci de suggérer une réponse correct","dark")
            return redirect(url_for('index'))
        chat = Chat(question=suggestion.question.data,reponse=suggestion.reponse.data,categorie=suggestion.categorie.data)
        db.session.add(chat)
        db.session.commit()
        ques.append(suggestion.question.data)
        rep.append(suggestion.reponse.data)
        cat.append(suggestion.categorie.data)
        nlp_question.append(nlp(ques.lower()))
        flash("Merci pour votre contribution !","primary")
        return redirect(url_for("index"))
    else:
        flash("Merci de bien voloir suggérer une réponse correcte","dark")
        return redirect(url_for('index')) 

@app.route("/validate_question",methods=["GET"])
def validate_question():
    user_q = request.args.get("user_q")
    q_index = int(request.args.get("q_sim_index"))
    q = user_q
    r = rep[q_index]
    c = cat[q_index]
    ques.append(q)
    rep.append(r)
    cat.append(c)
    nlp_question.append(nlp(q.lower()))
    chat = Chat(question=q,reponse=r,categorie=c)
    db.session.add(chat)
    db.session.commit()
    return redirect(url_for('index'))

