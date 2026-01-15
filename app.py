from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Episode(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')
    serialize_rules = ('-appearances.episode',)

class Guest(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')
    serialize_rules = ('-appearances.guest',)

class Appearance(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    serialize_rules = ('-episode.appearances', '-guest.appearances')

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Late Show API", "endpoints": ["/episodes", "/guests", "/appearances"]})

@app.route('/episodes')
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict(only=('id', 'date', 'number')) for e in episodes])

@app.route('/episodes/<int:id>')
def get_episode(id):
    episode = db.session.get(Episode, id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    return jsonify(episode.to_dict(only=('id', 'date', 'number', 'appearances')))

@app.route('/guests')
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict(only=('id', 'name', 'occupation')) for g in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    
    if not (1 <= data.get('rating', 0) <= 5):
        return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400
    
    appearance = Appearance(
        rating=data['rating'],
        episode_id=data['episode_id'],
        guest_id=data['guest_id']
    )
    
    db.session.add(appearance)
    db.session.commit()
    
    return jsonify(appearance.to_dict()), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)