'''Librerias usadas'''
import requests # libreria para una consulta a una API
from geopy.geocoders import Nominatim   #libreria de Geocoder Inversa
import folium

'''Solicita al usuario ingresar un Nuemero de catastro'''
numero=int(input("ingrese un Número catastro: "))
''' funcion de ingreso de catastro'''
def my_catastro():
    while True:      # condicion si es distinto de 0 continua. 
        if numero!=0: 
            print(f"El catastro seleccionado es {numero} ")
        else:
            print(f"El Numero ingresado NO es un resultados validos, vuleva a ingresar al sistema") 
        break
my_catastro()

'''  Realizar una Consulta a la Api de catastros: 
Url de donde va el catastro : https://municipalidadsalta.gob.ar/ws_catastro/get_data.php?id={numero}")
hacer la pericion a la url anterior Para eso debemos importar el paquete=> request (Ejemplo de https://www.youtube.com/watch?v=fOR4bLgR00I)
y Codigo Facilito https://www.youtube.com/watch?v=hNbv1EIUW6g&list=PLpOqH6AE0tNguX5SG8HpcD3lfmzWrIn9n&index=5 '''
''' La una API que da el siguiente estructura de JSON: 
[
  {
    "catastro": 4324,
    "distrito": "R1",
    "calle": "BOLIVAR SIMON GRAL.",
    "nro": "310",
    "barrio": "SAN MARTIN",
    "latitud": -24.7852397516655,
    "longitud": -65.4202018100968,
    "observaciones": ""
  }
]
'''
''' mediante el metodo post y get hacemos las solicitudes al a la api: 
    1) post: enviamos a la url el numero ingresado, mediante la palabras reservada=> playload={clave:valor} 
    2) get: guardamos la respuesta en el parametro response, mediante la palabras reservadas=> requests.get(url, params=payload)
    3) traemos los datos en formatos json=> data=response.json()
'''
payload={'id':numero}  #clave valor o diccionario que contiene el numero de catastro que solicito. Uso el metodo post
url = "https://municipalidadsalta.gob.ar/ws_catastro/get_data.php"   #llama a la api
response = requests.get(url, params=payload) # pide los parametrso solicitados
if response.status_code == 200:  #capta el error si es servidor no esta escuchando
         data = response.json()  # pido que la restpuesta sea en un Json. El Json es un diccionario en Py
        #  print(data) # imprime el valor obtenido-> toda la info. yo solo necesito lat/long.
         json_data=data[0] # Transforma los datos en una Lista y  Obtiene el primer elemento del resultado
         lat=json_data.get('latitud')
         lng=json_data.get('longitud')
         print(lat,lng)
else:
    print("Error en el servidor. Código de estado:", response.status_code) # captua un error por si el servidor esta fuera de funcionamiento.

'''pip install geopy 
uso del Geocodificacion Inversa de GeoPy . Usa Nominatim para geocodificar.
'''
geolocator= Nominatim(user_agent="My_app")  #debo ingresar un valor en user_agent siempre
location = geolocator.reverse((lat,lng))     #paso las coordenadas como una tupla
print(location.address)     # muestra la direccion obtenida en Nominatim.

'''tranformo lo obtenido porque es una linea de texto plano que no puedo extraer los valores por separado para pasarle al Popous del Marker 
1) tranformo en json los dato -> con la palabra reservada .raw segun la documentacion
2) guardo en variables cada uno de los atributos que deseo guardar mediante una solicitud .get()
'''

direccion=location.raw     #segun la documentacion para que sea devuelto en json debe ser RAW de Nominatim
calle = direccion.get('address', {}).get('road')  ### Aca obtengo los valores dentro de la tupla segun OpenAi
numeracion = direccion.get('address', {}).get('house_number') 
barrio=direccion.get('address', {}).get('city_district') 
ciudad=direccion.get('address', {}).get('city') 
codigopostal=direccion.get('address', {}).get('postcode') 
pais=direccion.get('address', {}).get('country') 
#print(calle)

'''pip install folium
Para generar el mapa de localización con un marcador
1) genero un mapa con los atributos normales
2) genero un Style del Popup para que se vea bonito
3) Genero un Marker con el dato traido de Lat/Lng y coloco en el Popup los datos de Direccion bien bonitos.
4) Guardo el Mapa y lo exporto a html para verlo en el fronted.
'''
mapa=folium.Map(
       location=[lat, lng],
       tiles='Stamen Terrain',
       zoom_start=13,
       control_scale=True 
       )

#Estilo de popups
PopupStyle= {"width": "40px",
        "height": "20px",
        "position": "absolute",
        "left": "50 %",
        " margin- left": "-20px"}

folium.Marker(
     [lat, lng],
    #  popup=(f"Esta es el Catastro N° {numero}<br>El domicilio es: <b>Calle: </b>{calle} {numeracion}, <br><b> Barrio:</b> {barrio} <br><b>Pais:</b> {pais}, <b>Codigo postal : </b>{codigopostal}", 
    #  popup_style=PopupStyle)
     popup=f"Esta es el Catastro N° {numero}<br>El domicilio es: <b>Calle:</b> {calle} {numeracion},<br><b>Barrio:</b> {barrio}<br><b>País:</b> {pais}, <b>Código postal:</b> {codigopostal}",
            tooltip=f"Catastro N° {numero}",
            popup_style=PopupStyle  # Agregar el estilo PopupStyle al popu
).add_to(mapa)
#exporto el mapa
outmap="mapa.html"
mapa.save(outmap)
