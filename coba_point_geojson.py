import json
from geojson import Point, Feature
import sqlite3 as lite
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)


titik_lokasi = [
    {"lat": -7.3508394822, "long": 112.7246348756, "name": "waru", 'type': 'Point'},
    {"lat": -7.3524568595, "long": 112.6892726319, "name": "sedati", 'type': 'Point'},
    {"lat": -7.3851861995, "long": 112.6115100282, "name": "kota", 'type': 'Point'}
]


@app.route('/getpoint')
def getpoint():
	con=lite.connect("myskripsi.db")
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("select * from tweet")
	rows = cur.fetchall()
	lt = rows[0][3]
	lg = rows[0][4]
	rows_to_geojson = (rows, filename='data.geojson', lat='lt', lag='lg')
	Point((lt,lg))
	print (lt,lg)
	print (rows_to_geojson)
	return render_template("getpoint.html",rows = rows, lt=lt, lg=lg)


def create_point():
    lokasi = []
    for lokasi in titik_lokasi:
        point = Point([lokasi['long'], lokasi['lat']])
        properties = {
            'title': location['name'],
            'icon': 'campsite',
            'marker-color': '#3bb2d0',
            'marker-symbol': len(stop_locations) + 1
        }
        feature = Feature(geometry = point, properties = properties)
        stop_locations.append(feature)

        lokasi.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": address['coordinates']
            }
        })
    return stop_locations



app.secret_key = 'baksosolo'

if __name__ == "__main__":
    app.run(debug="True")