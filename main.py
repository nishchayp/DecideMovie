from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

class MovieDetails(object):
	def __init__(self, infoJson, genreInfoJson):
		if infoJson is None and genreInfoJson is None:
			self.id = 0
			self.vote_average = 0
			self.title = ""
			self.poster_path = ""
			self.overview = ""
			self.genres = ""
			self.count = 0
		else:
			self.id = infoJson["results"][0]["id"]
			self.vote_average = infoJson["results"][0]["vote_average"]
			self.title = infoJson["results"][0]["title"]
			self.poster_path = "https://image.tmdb.org/t/p/w500" + infoJson["results"][0]["poster_path"]
			self.overview = infoJson["results"][0]["overview"]
			self.genres = genreInfoJson["genres"]
			self.count = 0

movies = []

result = MovieDetails(None, None)


@app.route("/", methods = ["GET", "POST"])
def home():
	if request.method == "GET":
		for movie in movies:
			movies.remove(movie)
		return render_template("home.html")
	elif request.method == "POST":
		movieName = request.form["movieName"]
		info = requests.get("https://api.themoviedb.org/3/search/movie?api_key=2f2fd8f55fe7eebdbb843d858023d883&language=en-US&query=" + movieName + "&page=1&include_adult=false")
		infoJson = info.json()
		genreInfo = requests.get("https://api.themoviedb.org/3/movie/" + str(infoJson["results"][0]["id"]) + "?api_key=2f2fd8f55fe7eebdbb843d858023d883&language=en-US")
		genreInfoJson = genreInfo.json()
		movies.append(MovieDetails(infoJson, genreInfoJson))
		return render_template("home.html", movies = movies)

@app.route("/decide", methods = ["GET", "POST"])
def decide():
	if request.method == "GET":
		return render_template("decide.html", movies = movies)
	elif request.method == "POST":
		i = 0
		j = 0
		for movie in movies:
			i += 1
			j = 0
			for genre in movie.genres:
				j += 1
				if ((request.form["box-" + str(i) + "-" + str(j)]) == ("box-" + str(i) + "-" + str(j))):
					movie.count += 1


		result = MovieDetails(None, None)
		for movie in movies:
			if movie.count >= result.count:
				result = movie
			elif movie.count == result.count:
				if movie.vote_average >= result.vote_average:
					result = movie
		return render_template("result.html", result = result)

if __name__ == "__main__":
	app.run()