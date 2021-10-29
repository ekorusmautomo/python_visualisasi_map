import pandas as pd

data = pd.read_csv('data.csv')   
df = pd.DataFrame(data, columns= ['Tgl','Alamat','Deskripsi','Latitude','Longitude'])

print(df)