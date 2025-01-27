from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
heroku = Heroku(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://xxbkpfltxlaxeu:6c92bb396d604406d958a6f8bd270715f6950ae2d4ea6128c1d54775ce04ce4e@ec2-23-23-92-204.compute-1.amazonaws.com:5432/dc7ulvj7si5s6l"
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo(db.Model):
  __tablename__ = "todos"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  done = db.Column(db.Boolean)
  def __init__(self, title, done):
    self.title = title
    self.done = done
    
class Review(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), unique=False)
   content = db.Column(db.String(144), unique=False)
   def __init__(self, title, content):
       self.title = title
       self.content = content
class ReviewSchema(ma.Schema):
   class Meta:
       fields = ('title', 'content')
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
#Endpoint to create a new review
@app.route('/review', methods=["POST"])
def add_review():
   title = request.json['title']
   content = request.json['content']
   new_review = Review(title, content)
   db.session.add(new_review)
   db.session.commit()
   review = Review.query.get(new_review.id)
   return review_schema.jsonify(review)
# Endpoint to query all reviews
@app.route("/reviews", methods=["GET"])
def get_reviews():
   all_reviews = Review.query.all()
   result = reviews_schema.dump(all_reviews)
   return jsonify(result)
# Endpoint for querying a single review
@app.route("/review/<id>", methods=["GET"])
def get_review(id):
   review = Review.query.get(id)
   return review_schema.jsonify(review)
# Endpoint for updating a review
@app.route("/review/<id>", methods=["PUT"])
def review_update(id):
   review = Review.query.get(id)
   title = request.json['title']
   content = request.json['content']
   review.title = title
   review.content = content
   db.session.commit()
   return review_schema.jsonify(review)
# Endpoint for deleting a record
@app.route("/review/<id>", methods=["DELETE"])
def review_delete(id):
   review = Review.query.get(id)
   db.session.delete(review)
   db.session.commit()
   return "Review was successfully deleted"
if __name__ == '__main__':
   app.run(debug=True)