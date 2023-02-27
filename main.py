from flask import Flask, render_template, redirect, flash, session
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from get_data import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secret-key"
bootstrap = Bootstrap(app)

class Search(FlaskForm):
    artist = StringField(label="Artist")
    song = StringField(label="Track name")
    submit = SubmitField(label="Search")


@app.route("/", methods=["POST", "GET"])
def home():
    form = Search()
    if form.validate_on_submit():
        song = form.song.data.lower()
        artist = form.artist.data

        try:
            session["result"] = find_result(song, artist)
            session["song"] = song
            session["artist"] = artist
            if session["result"] == None or session["result"] == []:
                flash("Invalid input, try again.")
                redirect("/")
            else:
                return redirect("/results")
        except IndexError:
            flash("Invalid input, try again.")
            return redirect("/")



    return render_template("index.html", form=form)

@app.route("/results", methods=["POST", "GET"])
def results():
    result = session["result"]
    song = session["song"]
    artist = session["artist"]
    return render_template("results.html", result=result, song=song, artist=artist)

if __name__ == "__main__":
    app.run(debug=True)