from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku 
import os 

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Meme(db.Model):
    __tablename__ = "memes"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(150))
    image = db.Column(db.String(500))
    favorite = db.Column(db.Boolean)

    def __init__(self, text, image, favorite):
        self.text = text
        self.image = image
        self.favorite = favorite

class MemeSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "image", "favorite")

meme_schema = MemeSchema()
memes_schema = MemeSchema(many=True)

@app.route("/")
def greeting():
    return"<h1>Hello</h1>"

@app.route('/add-meme', methods = ["POST"])
def add_meme():
    text = request.json['text']
    image = request.json['image']
    favorite = request.json['favorite']

    new_meme = Meme(text, image, favorite)

    db.session.add(new_meme)
    db.session.commit()


    meme = Meme.query.get(new_meme.id)
    return meme_schema.jsonify(meme)


if __name__ == '__main__':
    app.run(debug=True)