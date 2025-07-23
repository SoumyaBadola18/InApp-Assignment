# app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from config import Config
from models import db, ma, Person, Title, PersonSchema, TitleSchema
from auth import auth_bp
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return 'API is running'

@app.route('/search/movie', methods=['GET'])
@jwt_required()
def search_movie():
    print('Searching Movie')
    start_time = time.time()
    query = Title.query
    year = request.args.get('year')
    genre = request.args.get('genre')
    ptype = request.args.get('type')

    if year:
        query = query.filter(Title.startYear == int(year))
    if genre:
        query = query.filter(Title.genres.contains(genre))
    if ptype:
        query = query.filter(Title.titleType.ilike(f'%{ptype}%'))

    results = query.limit(5).all()
    output = []

    for movie in results:
        associated_people = Person.query.filter(Person.knownForTitles.contains(movie.tconst)).all()
        people_schema = PersonSchema(many=True)
        output.append({
            "title": TitleSchema().dump(movie),
            "associated_people": people_schema.dump(associated_people)
        })

    end_time = time.time()
    print("Movie Search took {:.2f} seconds".format(end_time - start_time))
    return jsonify(output)

@app.route('/search/person', methods=['GET'])
@jwt_required()
def search_person():
    print('Searching Person')
    start_time = time.time()
    name = request.args.get('name', '').lower()
    title = request.args.get('title', '').lower()
    profession = request.args.get('profession', '').lower()

    query = Person.query

    if name:
        query = query.filter(Person.primaryName.ilike(f'%{name}%'))
    if profession:
        query = query.filter(Person.primaryProfession.ilike(f'%{profession}%'))
    if title:
        query = query.filter(Person.knownForTitles.ilike(f'%{title}%'))

    results = query.limit(20).all()
    output = []

    for person in results:
        known_titles = []
        for tid in person.knownForTitles.split(','):
            title_obj = db.session.get(Title, tid)
            if title_obj:
                known_titles.append(TitleSchema().dump(title_obj))
        person_data = PersonSchema().dump(person)
        person_data['knownForTitles'] = known_titles
        output.append(person_data)

    end_time = time.time()
    print("Person Search took {:.2f} seconds".format(end_time - start_time))
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
