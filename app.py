from flask import Flask, render_template 
import requests 
import json 

app = Flask(__name__, template_folder='template') 
req = requests.get("https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/COVID19_Indonesia_per_Provinsi/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json")
data = json.loads(req.text) 
features = data['features']
data_covid = [] 
aww = [] 
listpositif = [] 
listmeninggal = [] 
listsembuh = [] 

for i in features:
    covid=dict()
    attributes = i['attributes']
    covid['provinsi'] = attributes['Provinsi']
    covid['positif'] = attributes['Kasus_Posi']
    covid['sembuh'] = attributes['Kasus_Semb']
    covid['meninggal'] = attributes['Kasus_Meni']
    data_covid.append(covid)
#loop data
for i in range(34):
    listpositif.append(data_covid[i]['positif'])
    listmeninggal.append(data_covid[i]['meninggal'])
    listsembuh.append(data_covid[i]['sembuh'])
#rumus untuk menghitung persen
persentasesembuh = list(map(lambda x, y: x / y * 100, listsembuh, listpositif))
persentasemeninggal = list(map(lambda x, y : x / y * 100, listmeninggal, listpositif))
percensembuh = [f'{i:.1f}%' for i in persentasesembuh]
percenmeninggal = [f'{i:.1f}%' for i in persentasemeninggal]

for i in range(34):
    data_covid[i]['persensembuh'] = percensembuh[i]
    data_covid[i]['persenmeninggal'] = percenmeninggal[i]

#rumus untuk memanggil library flask
@app.route('/')
def home():
    return render_template('index.html',covid=data_covid)
@app.route('/covid')
def profil():
    return render_template('indek.html',covid=data_covid)
@app.route('/sorted')
def urut():
    urutkan = sorted(data_covid, key=lambda x: x['provinsi'])
    return render_template('sorted.html', covid=urutkan)
@app.route('/filter')
def filterin():
    filtering = filter(lambda x: x < 10000, aww)
    return render_template('filter.html', covid=data_covid)
@app.route('/zonamerah')
def merah():
    filtering = filter(lambda x: x > 10000, aww)
    return render_template('zonamerah.html', covid=data_covid)
if __name__ == "__main__":
    app.run(debug=True) #debug=True untuk saat ada penggantian file tidak perlu run ulang