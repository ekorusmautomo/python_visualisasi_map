import csv

with open('data.csv') as file_csv:
    r = csv.reader(file_csv, delimiter=',')
    line = 0
    for row in r:
        if line == 0:
            hasil = (str(row[0]),"|",str(row[1]),"|",str(row[2]),"|",str(row[3]),str(row[4]))
            print (hasil)
            line += 1
        else:
            hasil2 = (str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]))
            print (hasil2)
            line += 1


    
