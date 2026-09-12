package com.tfg.myapplication.clima.repositories;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

// Importar las clases del paquete de la API
import com.tfg.myapplication.clima.OpenWeatherMapService;
import com.tfg.myapplication.clima.WeatherResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class WeatherRepository {

    private OpenWeatherMapService openWeatherMapService;
    private static final String BASE_URL = "https://api.openweathermap.org/";
    private static final String API_KEY = "";

    public WeatherRepository() {
        // Configura y crea la instancia de Retrofit
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create()) // Usa Gson para convertir JSON
                .build();

        // Crea la implementación de la interfaz del servicio API
        openWeatherMapService = retrofit.create(OpenWeatherMapService.class);
    }

    // Método para obtener el clima actual por nombre de ciudad
    // Devuelve un LiveData que la capa ViewModel/UI puede observar
    public LiveData<WeatherResponse> getCurrentWeatherByCity(String cityName) {
        // Usamos MutableLiveData para poder actualizar su valor cuando llegue la respuesta de la API
        MutableLiveData<WeatherResponse> data = new MutableLiveData<>();

        // Realiza la llamada asíncrona a la API
        openWeatherMapService.getCurrentWeatherByCity(cityName, API_KEY, "metric") // "metric" para Celsius
                .enqueue(new Callback<WeatherResponse>() { // enqueue() ejecuta la llamada en segundo plano
                    @Override
                    public void onResponse(Call<WeatherResponse> call, Response<WeatherResponse> response) {
                        if (response.isSuccessful() && response.body() != null) {
                            // Si la respuesta es exitosa y tiene datos, actualiza el LiveData
                            data.setValue(response.body());
                        } else {
                            // Si la respuesta no es exitosa (ej: ciudad no encontrada, error de API)
                            // Puedo loggear el error (response.code(), response.errorBody())
                            data.setValue(null); // Indica a los observadores que hubo un error o no hay datos
                            // Opcional: Usar otro LiveData para mensajes de error
                        }
                    }

                    @Override
                    public void onFailure(Call<WeatherResponse> call, Throwable t) {
                        // Si hay un fallo en la comunicación (ej: sin internet, problema de servidor)
                        t.printStackTrace(); // Loggear la excepción
                        data.setValue(null); // Indica a los observadores que hubo un fallo
                        // Opcional: Usar otro LiveData para mensajes de error de conexión
                    }
                });

        return data; // Devuelve el LiveData inmediatamente. Su valor se actualizará después.
    }

    // Método para obtener el clima actual por coordenadas
    public LiveData<WeatherResponse> getCurrentWeatherByCoordinates(double lat, double lon) {
        MutableLiveData<WeatherResponse> data = new MutableLiveData<>();

        openWeatherMapService.getCurrentWeatherByCoordinates(lat, lon, API_KEY, "metric") // "metric" para Celsius
                .enqueue(new Callback<WeatherResponse>() {
                    @Override
                    public void onResponse(Call<WeatherResponse> call, Response<WeatherResponse> response) {
                        if (response.isSuccessful() && response.body() != null) {
                            data.setValue(response.body());
                        } else {
                            data.setValue(null);
                        }
                    }

                    @Override
                    public void onFailure(Call<WeatherResponse> call, Throwable t) {
                        t.printStackTrace();
                        data.setValue(null);
                    }
                });

        return data;
    }
}