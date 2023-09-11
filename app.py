from flask import Flask, render_template, request, jsonify
from recommendationFunctions import *


app = Flask(__name__)

movies = cleanData('movies_db.xlsx')

@app.route('/')
def hello_world():
    movie_list = movies['movie_title'].values
    return render_template('index.html', options=movie_list)

@app.route('/process_option', methods=['GET'])
def process_option():
    recommended_movie_names = []
    recommended_movie_posters = []
    movie = request.args.get('selected_option')
    for i in get_recommendations(movie, movies).values:
        recommended_movie_posters.append(fetch_poster(i[1]))
        recommended_movie_names.append(i[0])
    return jsonify({'list1': recommended_movie_names, 'list2': recommended_movie_posters})

if __name__ == "__main__":
    app.run(debug=True)
