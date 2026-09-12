package com.tfg.myapplication.ui.actualidad;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.Transformations; // Importa Transformations

// Importa tus clases de datos y repositorios (ajusta los paquetes)
import com.tfg.myapplication.clima.repositories.WeatherRepository; // Tu Repositorio para el Clima
import com.tfg.myapplication.clima.WeatherResponse; // Tu clase de datos de respuesta del Clima

import org.osmdroid.util.GeoPoint; // Para la ubicación actual


public class ActualidadViewModel extends AndroidViewModel {

    // --- Datos relacionados con el Mapa (controlados por el ViewModel) ---

    // LiveData para la ubicación actual del usuario (actualizada por el Fragmento)
    private MutableLiveData<GeoPoint> currentLocation = new MutableLiveData<>();

    // --- Datos relacionados con el Clima (gestionados por el ViewModel) ---

    // Repositorio para obtener datos del clima
    private WeatherRepository weatherRepository;
    // MutableLiveData que usaremos para decirle al switchMap para qué ciudad buscar el clima
    private MutableLiveData<String> cityForWeather = new MutableLiveData<>();
    // LiveData que contendrá la respuesta actual del clima (su valor cambia cuando cityForWeather cambia o el repositorio responde)
    private LiveData<WeatherResponse> currentWeather;

    // Constructor del ViewModel
    public ActualidadViewModel(@NonNull Application application) {
        super(application);

        // **Inicializa tus Repositorios aquí.**
         weatherRepository = new WeatherRepository(); // Ajusta el constructor si es necesario

        // **Configurar la obtención de datos del Clima usando Transformations.switchMap.**
        // switchMap reacciona a los cambios en 'cityForWeather'. Cada vez que cityForWeather cambie,
        // switchMap ejecutará la función proporcionada (una llamada al repositorio) y
        // cambiará el LiveData que 'currentWeather' está observando al nuevo LiveData devuelto por el repositorio.
        currentWeather = Transformations.switchMap(cityForWeather, city -> {
            if (city == null || city.isEmpty()) {
                // Si la ciudad es nula o vacía, devuelve un LiveData vacío (sin datos de clima)
                return new MutableLiveData<>();
            }
            // Llama al repositorio para obtener el LiveData con el clima para la ciudad especificada.
            return weatherRepository.getCurrentWeatherByCity(city);
            // Si también tienes un método en el repositorio para buscar por coordenadas:
            // return weatherRepository.getCurrentWeatherByCoordinates(lat, lon); // Usarías otro MutableLiveData para coordenadas
        });

        // Puedes añadir aquí otras inicializaciones o lógica al crear el ViewModel.
    }

    // --- Métodos Públicos para que el Fragmento observe los datos (LiveData) ---

    // Devuelve el LiveData de la ubicación actual. El Fragmento lo puede observar si necesita mostrar coordenadas, etc.
    public LiveData<GeoPoint> getCurrentLocation() {
        return currentLocation;
    }

    // Devuelve el LiveData de los datos del clima actual. El Fragmento lo observará para actualizar la UI del clima.
    public LiveData<WeatherResponse> getCurrentWeather() {
        return currentWeather;
    }

    // --- Métodos Públicos para que el Fragmento desencadene acciones o actualice datos en el ViewModel ---

    // Método llamado por el Fragmento cuando recibe una nueva actualización de ubicación.
    public void updateCurrentLocation(GeoPoint newLocation) {
        currentLocation.setValue(newLocation); // Actualiza el LiveData de la ubicación actual. Esto notifica a los observadores.
    }

    // Método llamado por el Fragmento (o donde sea necesario) para solicitar la obtención del clima para una ciudad.
    // Al llamar a setValue en cityForWeather, se activa el switchMap y la llamada a la API.
    public void fetchWeatherForCity(String cityName) {
        cityForWeather.postValue(cityName);
    }

    // Opcional: Método para obtener el clima para la ubicación actual (requiere geocodificación inversa o llamada API por coords)
    // public void fetchWeatherForCurrentLocation() {
    //     GeoPoint lastLocation = currentLocation.getValue(); // Obtiene la última ubicación conocida
    //     if (lastLocation != null) {
    //         // Aquí necesitarías la lógica para obtener el nombre de la ciudad a partir de las coordenadas (geocodificación inversa)
    //         // o llamar a un método en el WeatherRepository que obtenga el clima por coordenadas.
    //         // Esto puede requerir un Repositorio de Geocodificación adicional.
    //         // Si tienes el nombre de la ciudad: fetchWeatherForCity(nombreCiudad);
    //         // Si el repositorio puede por coords: weatherRepository.getCurrentWeatherByCoordinates(lastLocation.getLatitude(), lastLocation.getLongitude());
    //     }
    // }

    // Puedes añadir aquí otros métodos si tu ActualidadFragment necesita realizar otras acciones
    // que involucren la lógica de negocio o los datos (ej. seleccionar un sitio al hacer clic en un marcador).
}