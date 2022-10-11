from flaskferrelli import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#model class from db instance
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    #set relationship between User and Rental
    rental = db.relationship('Rental', backref='user', uselist=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    makemodel = db.Column(db.String(70), nullable=False)
    startdate = db.Column(db.Integer, nullable=False)
    enddate = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self): 
        #return f"Rental('{self.year}', '{self.makemodel}', '{self.startdate}', '{self.enddate}')"
        return f"{self.year} {self.makemodel} From {self.startdate} To {self.enddate}"

#one-to-one User/Rental relationship (one user can only rent one car at a time)