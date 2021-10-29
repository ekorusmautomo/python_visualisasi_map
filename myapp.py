from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3 as lite
import pandas as pd
import csv, time
from io import TextIOWrapper
import netifaces as ni
import folium

app = Flask(__name__)


@app.route('/')
def index():
	if 'username' in session:
		username_session = session['username']
		return render_template('twit.html', session_user_name=username_session)
	else:
		#return render_template ('index.html') #backend

		con=lite.connect("myskripsi.db")
		dt = pd.read_sql_query("SELECT * FROM tweet", con)
		df = pd.DataFrame(dt)

		df_lokasi = df[['latitude', 'longitude']]
		location_list = df_lokasi.values.tolist()
		    
		df_tgl = df['created_date']
		tgl_list = df_tgl.values.tolist()

		df_content = df['content']
		content_list = df_content.values.tolist()

		df_username = df['username']
		username_list = df_username.values.tolist()

		start_coords = (-7.446290537747875, 112.65134254198409)
		folium_map = folium.Map(location=start_coords, zoom_start=12)
		tooltip = "Click for detail"
		
		for point in range(0, len(location_list)):
			folium.Marker(location_list[point], popup=username_list[point], tooltip=tooltip).add_to(folium_map)

		folium_map.save('templates/map.html')
		#return folium_map._repr_html_()
		return render_template ('index.html')


@app.route('/logout')
def logout():
	ni.ifaddresses('wlp3s0')
	ip = ni.ifaddresses('wlp3s0')[2][0]['addr']
	now = time.time()
	saiki = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
	username = session['username']
	status = "logout"
	con = lite.connect('myskripsi.db')
	with con:
		cur=con.cursor()
		cur.execute("INSERT INTO login (username, ip, tgl, status) Values (?,?,?,?)", (username,ip,saiki,status))
		con.commit()
	session.pop('username', None)
	return redirect(url_for('index'))


@app.route('/showlogin')
def showlogin():
	return render_template("login.html")


@app.route('/gologin/', methods=['GET','POST'])
def gologin():
    error=""
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']

        con=lite.connect('myskripsi.db')
        cur=con.cursor()
        cur.execute("SELECT COUNT(1) FROM user WHERE username = (?)", [username_form])
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM user WHERE username =(?)", [username_form])
            for row in cur.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']

                    ni.ifaddresses('wlp3s0')
                    ip = ni.ifaddresses('wlp3s0')[2][0]['addr']
                    iduser = username = request.form['username']
                    now = time.time()
                    saiki = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
                    username = request.form['username']
                    status = "login"

                    con = lite.connect('myskripsi.db')

                    with con:
                        cur=con.cursor()
                        cur.execute("INSERT INTO login (username, ip, tgl, status) Values (?,?,?,?)", (username,ip,saiki,status))
                        con.commit()

                    return redirect(url_for('showtwit'))
                else:
                    error = "Invalid Credential - Error Password"
            else:
                error = "Invalid Credential - Error Username!!!"
    return render_template('login.html', error=error)


@app.route('/showregister')
def showregister():
	return render_template("register.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		nama_form = request.form['nama']
		email_form = request.form['email']
		username_form = request.form['username']
		password_form = request.form['password']
		now = time.time()
		saiki = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
		con = lite.connect("myskripsi.db")
		con.row_factory = lite.Row
		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO user (name, email, created_date, username, password) VALUES (?,?,?,?,?)", (nama_form, email_form, saiki, username_form, password_form))
			con.commit()
			cur.close()
			return redirect(url_for('showlogin'))


@app.route('/showtwit')
def showtwit():
	username_session = session['username']
	con=lite.connect("myskripsi.db")
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("select * from tweet ORDER BY tweet_id DESC")
	rows = cur.fetchall()

	curr = con.cursor()
	curr.execute("select COUNT(*) from tweet")
	item = curr.fetchall()
	return render_template("twit.html",rows = rows, session_user_name=username_session, item=item)


@app.route('/add_twit', methods=['GET', 'POST'])
def add_twit():
	username_session = session['username']
	con=lite.connect("myskripsi.db")
	cur = con.cursor()
	cur.execute("select * from user where username=(?)", [username_session])
	user = cur.fetchall()
	user_id = user[0][0]

	if request.method == 'POST':
		tweet_form = request.form['tweet']
		latitude_form = request.form['latitude']
		longitude_form = request.form['longitude']
		now = time.time()
		saiki = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
		con = lite.connect("myskripsi.db")
		con.row_factory = lite.Row
		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO tweet (content, created_date, latitude, longitude, user_id, username) VALUES (?,?,?,?,?,?)", (tweet_form, saiki, latitude_form, longitude_form, user_id, username_session))
			con.commit()
			cur.close()
			return redirect(url_for('showtwit'))


@app.route('/showmytwit')
def showmytwit():
	username_session = session['username']
	con=lite.connect("myskripsi.db")
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("select * from tweet where username=(?)", [username_session])
	rows = cur.fetchall()

	return render_template("mytwit.html",rows = rows, session_user_name=username_session)


@app.route('/showupdatetwit/<string:record_id>')
def showupdatetwit(record_id):
	username_session = session['username']
	con=lite.connect("myskripsi.db")
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("select * from tweet where tweet_id=(?)", [record_id])
	rows = cur.fetchall()
	return render_template("edittwit.html", session_user_name=username_session, rows=rows)


@app.route('/edittwit/<string:record_id>', methods=['GET', 'POST'])
def edittwit(record_id):
	if request.method == 'POST':
		con=lite.connect("myskripsi.db")
		con.row_factory = lite.Row
		content_form = request.form['content']
		latitude_form = request.form['latitude']
		longitude_form = request.form['longitude']
		now = time.time()
		saiki = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
		cur = con.cursor()
		with con:
			cur.execute("UPDATE tweet SET content=?, created_date=?, latitude=?, longitude=? WHERE tweet_id=?", (content_form, saiki, latitude_form, longitude_form, record_id))
			con.commit()
			cur.close()
		return redirect(url_for('showmytwit'))
	return render_template('edittwit.html')


@app.route('/showdeletetwit/<string:record_id>')
def showdeletetwit(record_id):
	username_session = session['username']
	con=lite.connect("myskripsi.db")
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("select * from tweet where tweet_id=(?)", [record_id])
	rows = cur.fetchall()
	return render_template("deletetwit.html", session_user_name=username_session, rows=rows)


@app.route('/deletetwit/<string:record_id>', methods=['GET', 'POST'])
def deletetwit(record_id):
	if request.method == 'POST':
		con=lite.connect("myskripsi.db")
		con.row_factory = lite.Row
		cur = con.cursor()
		with con:
			cur.execute("DELETE FROM tweet WHERE tweet_id=(?)",[record_id])
			con.commit()
			cur.close()
		return redirect(url_for('showmytwit'))
	return render_template('deletetwit.html')


@app.route('/showmap')
def showmap():
	con=lite.connect("myskripsi.db")
	dt = pd.read_sql_query("SELECT * FROM tweet", con)
	df = pd.DataFrame(dt)

	df_lokasi = df[['latitude', 'longitude']]
	location_list = df_lokasi.values.tolist()
	    
	df_tgl = df['created_date']
	tgl_list = df_tgl.values.tolist()

	df_content = df['content']
	content_list = df_content.values.tolist()

	df_username = df['username']
	username_list = df_username.values.tolist()

	start_coords = (-7.446290537747875, 112.65134254198409)
	folium_map = folium.Map(location=start_coords, zoom_start=12)
	tooltip = "Click for detail"
	
	for point in range(0, len(location_list)):
		folium.Marker(location_list[point], popup=username_list[point], tooltip=tooltip).add_to(folium_map)

	return folium_map._repr_html_()


@app.route('/userlist')
def userlist():
	con=lite.connect("myskripsi.db")
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("select * from user")
	rows = cur.fetchall()
	con.close()
	return render_template("userlist.html", rows=rows)


# READ FILE CSV FROM FORM UPLOAD

@app.route('/showdata')
def showdata():
	con=lite.connect("myskripsi.db")
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("select * from data")
	rows = cur.fetchall()
	con.close()
	return render_template("listdata.html", rows=rows)


@app.route('/showupload')
def showupload():
	return render_template("uploadcsv.html")


@app.route('/bacacsv', methods=['GET', 'POST'])
def bacacsv():
	if request.method == 'POST':
		file_form = request.form['file']
		with open(file_form, mode='r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
					#print(f'Column names are {", ".join(row)}')
					line_count += 1
				#print("{row["datetime"]}  {row["alamat"]}  {row["deskripsi"]} {row["latitude"]} {row["longitude"]}
				hasil = row["datetime"], row["alamat"], row["deskripsi"], row["latitude"], row["longitude"]
				dt = row["datetime"]
				alamat = row["alamat"]
				desk = row["deskripsi"]
				lat = row["latitude"]
				lng = row["longitude"]
				print(hasil,dt,alamat,desk,lat,lng)
				line_count += 1
			print('Processed lines:',line_count)
		#print('Processed {line_count} lines.')
		return render_template('listdata.html', hasil=hasil, dt=dt)


@app.route('/simpancsv', methods=['GET', 'POST'])
def simpancsv():
	con = lite.connect("myskripsi.db")
	con.row_factory = lite.Row


	if request.method == 'POST':
		file_form = request.form['file']
		with open(file_form, mode='r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
					line_count += 1
				hasil = row["datetime"], row["alamat"], row["deskripsi"], row["latitude"], row["longitude"]
				dt = row["datetime"]
				alamat = row["alamat"]
				desk = row["deskripsi"]
				lat = row["latitude"]
				lng = row["longitude"]
				print(dt,alamat,desk,lat,lng)

				cur=con.cursor()
				cur.execute("INSERT INTO data (tgl,alamat,deskripsi,latitude,longitude) Values (?,?,?,?,?)", (dt,alamat,desk,lat,lng))
				con.commit()

				line_count += 1
			print('Processed lines:',line_count)

		return redirect(url_for('showdata'))
    
@app.route('/showmapfromcsv')
def showmapfromcsv():
	con=lite.connect("myskripsi.db")
	dt = pd.read_sql_query("SELECT * FROM data", con)
	df = pd.DataFrame(dt)

	df_lokasi = df[['latitude', 'longitude']]
	location_list = df_lokasi.values.tolist()
		    
	df_tgl = df['tgl']
	tgl_list = df_tgl.values.tolist()

	df_content = df['deskripsi']
	content_list = df_content.values.tolist()

	start_coords = (-7.446290537747875, 112.65134254198409)
	folium_map = folium.Map(location=start_coords, zoom_start=12)
	tooltip = "Click for detail"
		
	for point in range(0, len(location_list)):
		folium.Marker(location_list[point], popup=tgl_list[point], tooltip=tooltip).add_to(folium_map)

	folium_map.save('templates/maps.html')
	#return folium_map._repr_html_()
	return render_template ('showmapcsv.html')


app.secret_key = 'baksosolo'

if __name__ == "__main__":
    app.run(debug="True")

