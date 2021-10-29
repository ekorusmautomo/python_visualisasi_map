from flask import Flask, render_template, request, url_for, redirect
import sqlite3 as lite
import time
from peewee import *

app = Flask(__name__)


@app.route("/") #tergantung permintaan user
def index(): #backend
	return render_template ('index.html') #backend


@app.route('/crimelist')
def crimelist():
    con=lite.connect("myskripsi.db")
    con.row_factory = lite.Row

    cur = con.cursor()
    cur.execute("select * from crime")

    rows = cur.fetchall();
    con.close()
    return render_template("crimelist.html", rows = rows)



@app.route('/insertcrime')
def insertcrime():
    return render_template ("input_crime.html")

@app.route('/savecrime', methods=['GET', 'POST'])
def savecrime():
    if request.method == 'POST':
        id_form = request.form['id']
        alamat_form =request.form['alamat']
        deskripsi_form = request.form['deskripsi']
        lat = request.form['latitude']
        longi = request.form['longitude']
        now = time.time()
        saiki = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))



        con = lite.connect('myskripsi.db')

        with con:
            cur=con.cursor()
            cur.execute("INSERT INTO crime (id,date,alamat,deskripsi,latitude,longitude) Values (?,?,?,?,?,?)", (id_form,saiki,alamat_form,deskripsi_form,lat,longi))
            con.commit()

        return redirect(url_for('crimelist'))


@app.route('/showmap')
def showmap():
    con=lite.connect("myskripsi.db")
    con.row_factory = lite.Row

    cur = con.cursor()
    cur.execute("select * from crime")

    rows = cur.fetchall();
    con.close()
    return render_template("peta.html", rows = rows)


app.secret_key = 'baksosolo'
if __name__ == "__main__":
    app.run(debug="True")