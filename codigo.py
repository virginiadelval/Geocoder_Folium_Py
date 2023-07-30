'''Librerias usadas'''
import requests  # libreria para una consulta a una API
from geopy.geocoders import Nominatim  # libreria de Geocoder Inversa
import folium


''' funcion de busqueda de domicilio a partir de la API de catastro'''

def my_catastro():
    while True:
        if numero != 0:  # condicion si es distinto de 0 continua.
            ''' se ejecuta el codigo y llamo a la url'''
            print(f"El catastro seleccionado es {numero} ")
            print(f"Buscando coordenadas, aguarde un instante por favor.... ")

            '''  Realizar una Consulta a la Api de catastros: 
                        Url de donde va el catastro : https://municipalidadsalta.gob.ar/ws_catastro/get_data.php?id={numero}")
                        hacer la pericion a la url anterior Para eso debemos importar el paquete=> request (Ejemplo de https://www.youtube.com/watch?v=fOR4bLgR00I)
                        y Codigo Facilito https://www.youtube.com/watch?v=hNbv1EIUW6g&list=PLpOqH6AE0tNguX5SG8HpcD3lfmzWrIn9n&index=5 '''
            url = "https://municipalidadsalta.gob.ar/ws_catastro/get_data.php"  # llama a la api

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
                        mediante el metodo post y get hacemos las solicitudes al a la api: 
                            1) post: enviamos a la url el numero ingresado, mediante la palabras reservada=> playload={clave:valor} 
                            2) get: guardamos la respuesta en el parametro response, mediante la palabras reservadas=> requests.get(url, params=payload)
                            3) traemos los datos en formatos json=> data=response.json()
                        '''
            payload = {'id': numero}  # diccionario que contiene el numero de catastro que solicito. Uso el metodo post
                    # pide los parametrso solicitados
            response = requests.get(url, params=payload)
            if response.status_code == 200:  # capta el error si es servidor no esta escuchando
                        # pido que la restpuesta sea en un Json. El Json es un diccionario en Py
                data = response.json()
                # if data ==None:
                #                  print("Error!! No se encontro datos para este Catastro. Ingrese otro número por favor")
                #                  break     
                #             #  print(data) # imprime el valor obtenido-> toda la info. yo solo necesito lat/long.
                #             # Transforma los datos en una Lista y  Obtiene el primer elemento del resultado
                # else:
                json_data = data[0]
                lat = json_data.get('latitud')
                lng = json_data.get('longitud')
                if lat==None or lng==None:
                     print("Error!! No se encontro datos para este Catastro. Ingrese otro número por favor")
                     break
                else:
                     print(f"Las coordenadas encontradas son: {lat} , {lng}")
                geolocator = Nominatim(user_agent="My_app")  # debo ingresar un valor en user_agent siempre
                # paso las coordenadas como una tupla
                location = geolocator.reverse((lat, lng))
                if location.address != " ":
                                # muestra la direccion obtenida en Nominatim.
                                print(f"El domicilio encontrado es:  {location.address}")
                                '''Mensaje de  para  la ejecucion del index.html en el servidor '''
                                # print("Para visualizar la info en el mapa ejecute index.html en el brower")

                                '''tranformo lo obtenido porque es una linea de texto plano que no puedo extraer los valores por separado para pasarle al Popous del Marker 
                                            1) tranformo en json los dato -> con la palabra reservada .raw segun la documentacion
                                            2) guardo en variables cada uno de los atributos que deseo guardar mediante una solicitud .get()
                                            '''

                                # segun la documentacion para que sea devuelto en json debe ser RAW de Nominatim
                                direccion = location.raw
                                # Aca obtengo los valores dentro de la tupla segun OpenAi
                                calle = direccion.get('address', {}).get('road')
                                numeracion = direccion.get(
                                    'address', {}).get('house_number')
                                barrio = direccion.get('address', {}).get('city_district')
                                ciudad = direccion.get('address', {}).get('city')
                                codigopostal = direccion.get('address', {}).get('postcode')
                                pais = direccion.get('address', {}).get('country')
                                # print(calle)

                                '''pip install folium
                                            Para generar el mapa de localización con un marcador
                                            1) genero un mapa con los atributos normales
                                            2) genero un Style del Popup para que se vea bonito
                                            3) Genero un Marker con el dato traido de Lat/Lng y coloco en el Popup los datos de Direccion bien bonitos.
                                            4) Guardo el Mapa y lo exporto a html para verlo en el fronted.
                                            '''
                                mapa = folium.Map(
                                    location=[lat, lng],
                                    tiles='Stamen Terrain',
                                    name='Capa base: Stamen Terrain',
                                    zoom_start=13,
                                    control_scale=True
                                )

                                # Estilo de popups
                                popup_content = f"""
                                                    <b>Catastro N° {numero}</b><br><br>
                                                    <i>El domicilio encontrado es </i><br><br>
                                                    <b>Calle:</b> {calle} {numeracion},<br>
                                                    <b>Barrio:</b> {barrio}<br>
                                                    <b>Código postal:</b> {codigopostal}<br>
                                                    <b>País:</b> {pais}
                                                    """

                                folium.Marker(
                                    [lat, lng],  # tupla de lat/lon el punto en si mismo
                                    # el popus con el contenido y el ancho maximo
                                    popup=folium.Popup(popup_content, max_width=450),
                                    # pasa por el punto y da el nombre
                                    tooltip=f"El Catastro es {numero}"
                                ).add_to(mapa)  # agrega al mapa

                                folium.LayerControl().add_to(mapa)  # Agrego el control de capas

                                # exporto el mapa
                                outmap = "index.html"
                                mapa.save(outmap)

                                print(f"Ejecute http://127.0.0.1:5500/{outmap} para visualizar la info en el navegador")
                                break
                                ''' todos los else s'''
                else:
                    print("Error no existe domicilio")
                    break                     
            else:
                print("Error en el servidor. Código de estado:", response.status_code)
                break
        else:  # condicion inicial si ingresa un valor =0 o <=0
            print(f"El Numero ingresado NO es valido, vuleva a ingresar al sistema")
            break  # se cierra el sistema
        
    '''Solicita al usuario ingresar un Nuemero de catastro'''
numero = int(input("Ingrese un Número catastro por favor: "))

'''EJECUCION DE LA FUNCION'''
my_catastro()
