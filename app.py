from flask import Flask, render_template, request
import requests, math, folium, time

app = Flask(__name__)

@app.route('/coorde', methods=['POST'])
def coorde():
    formato = 'json'
    zipcode = request.form['zip']
    apiKey = '21451726-4fa5-4fe5-ac0a-64d1e9b30d2a'
    r = requests.get('https://geocode-maps.yandex.ru/1.x/?apikey='+apiKey+'&format=json&geocode='+zipcode+'&lang=en-US')
    json_object = r.json()
    temp_k = json_object
    descrip = json_object['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    temp_f = temp_k['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    tempd = temp_f.split()
    tempc = temp_f.split()
    yy = float(tempc[0])
    kk = float(tempd[1])
    map2 = folium.Map(location=[kk, yy],
    zoom_start=1)
    folium.Marker([kk, yy], 
    popup = '<strong>Location One</strong>',
    tooltip='click here'
    ).add_to(map2)
    ll2 = map2.save('templates/map2.html')
    #df_subr = df_suburbs[['Latitude','Longitude']]    
    #print(df_subr)
    print(type(tempd))
    return render_template('result2.html', temp=temp_f, descrip1=descrip)
#    return temp_f
    


@app.route('/result', methods=['POST'])
def coor():
    coordey = request.form['coordenadasy']
    coordex = request.form['coordenadasx']
    timestr = time.strftime("\nYear: %Y, Month: %m, Day: %d- Hour: %H, Minute: %M, Second: %S\n")
    ff = open('./data/mkd.csv','r')
    lines = ff.readlines()
    userinput = coordey
    for cory in lines:
        if cory.find(userinput) != -1:
            print(cory)
            if cory:
                ww = open('./data/log.txt','a')
                ww.write("\n" + cory + timestr + "\n")
                ww.close()
    a = float(coordey.strip().strip("'"))
    b = float(coordex.strip().strip("'"))
    apiKey = '21451726-4fa5-4fe5-ac0a-64d1e9b30d2a'
    j = requests.get('https://geocode-maps.yandex.ru/1.x/?apikey='+apiKey+'&format=json&geocode='+coordey+','+coordex+'&lang=en-US')
    json_object = j.json()
    lat1 = math.radians(55.755787)
    lon1 = math.radians(37.617634)
    lat2 = math.radians(b)
    map = folium.Map(location=[coordex, coordey],
    zoom_start=1)
    folium.Marker([coordex, coordey],
    popup='<strong> {{ coordex }} </strong>',
    tooltip='Click'
    ).add_to(map)
    folium.Marker([lat1, lon1],
    popup='<strong>Helo woreer</strong>',
    tooltip='hello'
    ).add_to(map)
    ll = map.save('templates/map.html')
    xx = map._repr_html_()
    R = 6373.0
    lon2 = math.radians(a)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    ecu = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(ecu), math.sqrt(1 - ecu))
    distance = round(R * c)
    Pais = json_object['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['description']
    return render_template('result.html', distance=distance, pais1=Pais,cory=cory)
    #return json_object


@app.route('/map2', methods=['GET'])
def mapp():
    return render_template('map2.html')

@app.route('/map', methods=['GET'])
def map():
    return render_template('map.html')

@app.route('/', methods=['GET'])

def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=4000, debug=True)