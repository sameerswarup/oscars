#!/usr/bin/env python3
'''
    webapp.py
'''
import flask
from flask import Flask, flash, redirect, render_template, request, url_for
import backend.datasource
import json
import sys


app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    ds = backend.datasource.DataSource()

    user = 'kuritar'
    password = 'lamp977python'
    connection = ds.connect(user, password)
    winners = []
    key = request.form['key']
    length = len(key)
    if length == 4:
        year = int(key)
        categories = ["picture","actor","actress","director"]

        if year < 1927 or year > 2018:
            title =  'The year ' + str(year) + ' is out of range. Please go back and type in again.'
            return render_template('result.html', winners=[], year=year, title=title)
        else:
            for category in categories:
                result = ds.get_winner(connection, year, category)
                film = result[0][0]
                if category != "picture":
                    person = result[0][1]
                else:
                    person = ""
                winners.append({"award":category, "film":film, "person":person})

                title = year + ' Oscar Winners'

    return render_template('result.html',
                                winners=winners,
                                title=title)


@app.route('/pictures')
def pictures():
    ds = backend.datasource.DataSource()
    user = 'kuritar'
    password = 'lamp977python'
    connection = ds.connect(user, password)


    year = 0
    category = "picture"
    pictures = ds.get_winner(connection, year, category)
    return render_template('pictures.html', pictures=pictures)

@app.route('/actors')
def actors():
    ds = backend.datasource.DataSource()
    user = 'kuritar'
    password = 'lamp977python'
    connection = ds.connect(user, password)


    year = 0
    category = "actor"
    actors = ds.get_winner(connection, year, category)

    return render_template('actors.html', actors=actors)

@app.route('/actresses')
def actresses():
    ds = backend.datasource.DataSource()
    user = 'kuritar'
    password = 'lamp977python'
    connection = ds.connect(user, password)


    year = 0
    category = "actress"
    actresses = ds.get_winner(connection, year, category)

    return render_template('actresses.html', actresses=actresses)

@app.route('/directors')
def directors():
    ds = backend.datasource.DataSource()
    user = 'kuritar'
    password = 'lamp977python'
    connection = ds.connect(user, password)


    year = 0
    category = "director"
    directors = ds.get_winner(connection, year, category)
    return render_template('directors.html', directors=directors)


@app.route('/trends_by_decade/<decade>')
def trends_by_decade(decade):
    ds = backend.datasource.DataSource()
    user = 'kuritar'
    password = 'lamp977python'
    connection = ds.connect(user, password)

    if int(decade) == 2010:
        start = 2010
        end = 2018
    elif int(decade) == 1910:
        start = 1927
        end = 1929
    else:
        start = int(decade)
        end = int(decade)+9
    pictures = ds.get_pictures(connection, start, end)
    genres = ds.get_genre(connection, pictures)
    counts = ds.count_genre(connection, genres)

    return render_template('trends-by-decade.html', start=start, end=end, counts=counts)


@app.route('/trends')
def trends():
    return render_template('trends.html')


@app.route('/about_oscars')
def about_oscars():
    return render_template('about-oscars.html')

@app.route('/winners2020')
def winners2020():
    return render_template('winners2020.html')

@app.route('/about_data')
def about_data():
    return render_template('about-data.html')

@app.route('/terms_of_use')
def terms_of_use():
    return render_template('terms.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact.html')





if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
