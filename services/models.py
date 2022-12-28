from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


##### Init class #####
db = SQLAlchemy()

##models###rr
class meAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), nullable=False  , unique = True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self,username,password ):
        self.username=username
        self.password = password




    @classmethod
    def check_username(self, username):
        x = self.query.filter_by(username=username).first()
        return x
        


class messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=True)
    message = db.Column(db.String(80), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    def __init__(self,name,subject,email , message ):
        self.name = name
        self.subject=subject
        self.email = email
        self.message = message


    @classmethod
    def delete(self, id):
        query = self.query.get(id)
        db.session.delete(query)
        db.session.commit()

  
