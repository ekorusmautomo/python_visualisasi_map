import sqlite3 as lite
username = "benibeni"
con=lite.connect("myskripsi.db")
cur = con.cursor()
curr = con.cursor()
cur.execute("select * from tweet where username=(?)", [username])
curr.execute("select count(*) from tweet")
user = cur.fetchall()
v = user.count("benibeni")
a = curr.fetchone()

b = user.count(3)
print (user)
print (b)
