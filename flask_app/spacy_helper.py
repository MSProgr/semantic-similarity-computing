import spacy
import pickle
import os
import re

from flask_app.model import Chat

nlp = spacy.load('flask_app/static/content/word2vec.model/')

with open(os.path.join('flask_app/static',"reponse.pickle"),"rb") as f:
    rep = pickle.load(f)
    
with open(os.path.join('flask_app/static',"question.pickle"),"rb") as f:
    ques = pickle.load(f)

with open(os.path.join('flask_app/static',"tag.pickle"),"rb") as f:
    tag = pickle.load(f)

with open(os.path.join('flask_app/static',"categorie.pickle"),"rb") as f:
    cat = pickle.load(f)

chats = Chat.query.all()

for chat in chats : 
    ques.append(chat.question)
    rep.append(chat.reponse)
    cat.append(chat.categorie)
    #when using all the data for training a new model
    # with open("ques_new.pkl","wb") as file:
    # 	pickle.dump(ques,file)
    # with open("resp_new.pkl","wb") as file:
    # 	pickle.dump(rep,file)

nlp_question = [nlp(s.lower()) for s in ques]

