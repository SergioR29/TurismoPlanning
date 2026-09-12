import sys
import os
import ipinfo
import requests
import urllib.parse

from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from vistas.actualidad_ui import Ui_actualidad

class Actualidad(QWidget, Ui_actualidad):
    closing = Signal()

    def __init__(self, ciudad=None):
        super().__init__()
        self.setupUi(self)

        self.ciudad_inicial = ciudad
        if(ciudad == "Guadalajara"):
            self.ciudad_inicial = "Guadalajara, Castilla-La Mancha, España"

        print(f"--- Depuración ---")
        print(f"Valor de self.ciudad_inicial al inicio de __init__: '{self.ciudad_inicial}' (Tipo: {type(self.ciudad_inicial)})")
        print(f"Evaluación de la condición 'if self.ciudad_inicial': {bool(self.ciudad_inicial)}")
        print(f"------------------")

        ciudad_determinada = "Desconocida"
        lat_determinada = 40.416775 # Coordenadas por defecto (Madrid)
        lon_determinada = -3.703790 # Coordenadas por defecto (Madrid)
        temperatura_str = "Obteniendo datos..."

        ipinfo_access_token = ''
        openweathermap_api_key = ''
        base_url_owm = "http://api.openweathermap.org/data/2.5/weather?"


        if self.ciudad_inicial:
            print("--- Entrando en modo: Buscar ciudad específica ---")

            ciudad_a_buscar = str(self.ciudad_inicial)
            ciudad_determinada = ciudad_a_buscar

            if openweathermap_api_key == 'TU_API_KEY_DE_OPENWEATHERMAP' or not openweathermap_api_key:
                temperatura_str = "Error: API Key de OpenWeatherMap no configurada."
                print(temperatura_str)
            else:
                try:
                    encoded_city_name = urllib.parse.quote(ciudad_a_buscar)
                    complete_url_owm = f"{base_url_owm}q={encoded_city_name}&appid={openweathermap_api_key}&units=metric&lang=es"

                    print(f"Consultando API de clima por nombre: {complete_url_owm}")
                    weather_response = requests.get(complete_url_owm)
                    weather_data = weather_response.json()
                    print(f"Respuesta API Clima (nombre): {weather_data}")

                    if weather_data.get("cod") == 200:
                        main_data = weather_data["main"]
                        current_temperature = main_data["temp"]
                        weather_description = weather_data["weather"][0]["description"]
                        ciudad_determinada = weather_data.get("name", ciudad_a_buscar)
                        coord_data = weather_data.get("coord", {})
                        lat_determinada = coord_data.get("lat", lat_determinada)
                        lon_determinada = coord_data.get("lon", lon_determinada)

                        temperatura_str = f"{current_temperature:.1f}°C ({weather_description})"
                        print(f"Datos de clima obtenidos (nombre): {temperatura_str}")

                    elif weather_data.get("cod") == "404":
                        temperatura_str = f"Error: Ciudad '{ciudad_a_buscar}' no encontrada en la API del clima."
                        print(temperatura_str)
                        if lat_determinada is None or lon_determinada is None:
                            lat_determinada = 40.416775
                            lon_determinada = -3.703790
                        ciudad_determinada = ciudad_a_buscar
                    else:
                         temperatura_str = f"Error API clima (código {weather_data.get('cod', 'desconocido')}): {weather_data.get('message', 'Error desconocido')}"
                         print(temperatura_str)
                         if lat_determinada is None or lon_determinada is None:
                            lat_determinada = 40.416775
                            lon_determinada = -3.703790
                         ciudad_determinada = ciudad_a_buscar


                except requests.exceptions.RequestException as e:
                    temperatura_str = f"Error de red al consultar API del clima: {e}"
                    print(temperatura_str)
                    if lat_determinada is None or lon_determinada is None:
                        lat_determinada = 40.416775
                        lon_determinada = -3.703790
                    ciudad_determinada = ciudad_a_buscar
                except Exception as e:
                    temperatura_str = f"Ocurrió un error general al buscar ciudad: {e}"
                    print(temperatura_str)
                    if lat_determinada is None or lon_determinada is None:
                        lat_determinada = 40.416775
                        lon_determinada = -3.703790
                    ciudad_determinada = ciudad_a_buscar

        else:
            print("--- Entrando en modo: Obtener ubicación actual por IP ---")

            ciudad_determinada = "Buscando ubicación por IP..."
            try:
                handler = ipinfo.getHandler(ipinfo_access_token)
                details = handler.getDetails()

                ciudad_ip = details.city
                ip_loc = details.loc

                print(f"Dirección IP: {details.ip}")
                print(f"Ciudad IP (ipinfo): {ciudad_ip}")
                print(f"Coordenadas IP (ipinfo): {ip_loc}")
                print(f"Organización IP: {details.org}")
                print(f"País IP: {details.country}")

                ciudad_determinada = ciudad_ip if ciudad_ip else "Ubicación IP desconocida"

                if ip_loc:
                    try:
                        lat_ip, lon_ip = map(float, ip_loc.split(','))
                        lat_determinada = lat_ip
                        lon_determinada = lon_ip
                        print(f"Coordenadas determinadas (desde ipinfo): {lat_determinada}, {lon_determinada}")
                    except ValueError:
                        print("Error al parsear coordenadas de ipinfo.io")
                        lat_determinada = 40.416775
                        lon_determinada = -3.703790
                        print(f"Usando coordenadas por defecto: {lat_determinada}, {lon_determinada}")
                else:
                     print("ipinfo.io no devolvió coordenadas.")
                     lat_determinada = 40.416775
                     lon_determinada = -3.703790
                     print(f"Usando coordenadas por defecto: {lat_determinada}, {lon_determinada}")


                if openweathermap_api_key == 'TU_API_KEY_DE_OPENWEATHERMAP' or not openweathermap_api_key:
                    temperatura_str = "Error: API Key de OpenWeatherMap no configurada."
                    print(temperatura_str)
                elif lat_determinada is not None and lon_determinada is not None:
                    try:
                        complete_url_owm = f"{base_url_owm}lat={lat_determinada}&lon={lon_determinada}&appid={openweathermap_api_key}&units=metric&lang=es"

                        print(f"Consultando API de clima por coordenadas: {complete_url_owm}")
                        weather_response = requests.get(complete_url_owm)
                        weather_data = weather_response.json()
                        print(f"Respuesta API Clima (coordenadas): {weather_data}")

                        if weather_data.get("cod") == 200:
                            main_data = weather_data["main"]
                            current_temperature = main_data["temp"]
                            weather_description = weather_data["weather"][0]["description"]
                            temperatura_str = f"{current_temperature:.1f}°C ({weather_description})"
                            print(f"Datos de clima obtenidos (coordenadas): {temperatura_str}")
                        elif weather_data.get("cod") == "404":
                             temperatura_str = f"Error: No se encontraron datos de clima para las coordenadas."
                             print(temperatura_str)
                        else:
                             temperatura_str = f"Error API clima (código {weather_data.get('cod', 'desconocido')}): {weather_data.get('message', 'Error desconocido')}"
                             print(temperatura_str)

                    except requests.exceptions.RequestException as e:
                        temperatura_str = f"Error de red al consultar API del clima: {e}"
                        print(temperatura_str)
                    except Exception as e:
                        temperatura_str = f"Ocurrió un error general al buscar clima por IP: {e}"
                        print(temperatura_str)
                else:
                    temperatura_str = "No se pudieron obtener coordenadas válidas para el clima."
                    print(temperatura_str)


            except ipinfo.exceptions.RequestQuotaExceeded:
                temperatura_str = "Error: Cuota de ipinfo.io excedida."
                print(temperatura_str)
                ciudad_determinada = "Ubicación IP no disponible"
            except ipinfo.exceptions.IPinfoException as e:
                 temperatura_str = f"Error de ipinfo.io: {e}"
                 print(temperatura_str)
                 ciudad_determinada = "Ubicación IP no disponible"
            except Exception as e:
                temperatura_str = f"Ocurrió un error general al obtener ubicación IP: {e}"
                print(temperatura_str)
                ciudad_determinada = "Ubicación IP no disponible"


        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "recursos/iconos/ic_menu_actualidad.png")))

        self.setWindowTitle(f"Actualidad - {ciudad_determinada or 'Buscando...'}")

        try:
            self.label_temperatura_widget = self.findChild(QLabel, 'label')
            if self.label_temperatura_widget:
                self.label_temperatura_widget.setText(temperatura_str)
                self.label_temperatura_widget.setAlignment(Qt.AlignCenter)
            else:
                 print("Advertencia: No se encontró QLabel 'label' en la UI para mostrar la temperatura.")
        except Exception as e:
             print(f"Error al configurar label de temperatura: {e}")

        map_lat = lat_determinada if lat_determinada is not None else 40.416775
        map_lon = lon_determinada if lon_determinada is not None else -3.703790
        map_city_name = ciudad_determinada if ciudad_determinada is not None else "Ubicación por defecto"

        print(f"--- Depuración ---")
        print(f"Datos finales para el mapa: Ciudad='{map_city_name}', Lat={map_lat}, Lon={map_lon}")
        print(f"Datos finales para la temperatura: '{temperatura_str}'")
        print(f"------------------")

        mapa = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Mapa de Ciudad: {map_city_name}</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        #mapid {{ height: 100%; width: 100%; min-height: 400px; }}
        body {{ margin: 0; padding: 0; }}
        html, body {{ height: 100%; }}
         .info-box {{
             position: absolute; top: 10px; left: 10px; z-index: 1000;
             background: white; padding: 10px; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.3);
             font-family: sans-serif; font-size: 0.9em;
             display: none;
         }}
    </style>
</head>
<body>

    <div id="mapid"></div>
    <div id="status" class="info-box"></div>

    <script>
        var mapLat = {map_lat};
        var mapLon = {map_lon};
        var mapName = "{map_city_name.replace('"', '\\"')}";

        var mymap = null;
        var initialZoom = 13;
        var defaultView = [40.416775, -3.703790];
        var defaultZoom = 5;

        function updateStatus(message, isError = false) {{
            var statusDiv = document.getElementById('status');
            if (statusDiv) {{
                 statusDiv.innerText = message;
                 statusDiv.style.backgroundColor = isError ? 'pink' : 'white';
                 statusDiv.style.display = 'block';
            }}
        }}

        function showMap(lat, lon, name) {{
             console.log("Mostrando mapa en:", name, [lat, lon]);
             var statusDiv = document.getElementById('status');
             if (statusDiv) statusDiv.style.display = 'none';

            if (mymap === null) {{
                 var cityLatLng = L.latLng(lat, lon);
                 mymap = L.map('mapid').setView(cityLatLng, initialZoom);

                 L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                     maxZoom: 19,
                     attribution: '© OpenStreetMap contributors'
                 }}).addTo(mymap);

                 var marker = L.marker(cityLatLng).addTo(mymap);

                 var popupContent = "<b>" + name + "</b>";
                 marker.bindPopup(popupContent).openPopup();

                 document.title = "Mapa de Ciudad: " + name;
            }} else {{
                 mymap.setView([lat, lon], initialZoom);
            }}
        }}

        console.log("Iniciando script del mapa...");

        if (!isNaN(mapLat) && !isNaN(mapLon)) {{
            console.log("Coordenadas recibidas en JS:", mapLat, mapLon);
            showMap(mapLat, mapLon, mapName);
        }} else {{
            console.warn("Coordenadas inválidas recibidas en JS. Mostrando mapa por defecto.");
            updateStatus("No se pudo obtener la ubicación exacta. Mostrando mapa por defecto.", true);
            showMap(defaultView[0], defaultView[1], "Ubicación por defecto");
        }}

    </script>

</body>
</html>
"""
        self.mapaUbi = self.findChild(QWebEngineView, 'mapaUbiCiudad')
        if self.mapaUbi:
            self.mapaUbi.setHtml(mapa)
        else:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.critical)
            msg_box.setWindowTitle("Error de UI")
            msg_box.setText("No se encontró el widget 'mapaUbiCiudad' (QWebEngineView) en el diseño UI.")
            msg_box.setInformativeText("Asegúrate de que el nombre del objeto en Qt Designer sea 'mapaUbiCiudad'.")
            msg_box.setStyleSheet("color:white;background-color:rgb(30,30,30)")
            msg_box.exec()


    def closeEvent(self, event):
        self.closing.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    actualidad_window = Actualidad()
    actualidad_window.show()
    exit_code = app.exec()
    sys.exit(exit_code)