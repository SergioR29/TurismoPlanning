package com.tfg.myapplication.clima;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

// Interfaz que define los endpoints de la API de OpenWeatherMap usando Retrofit
public interface OpenWeatherMapService {

    // Endpoint para obtener el clima actual por nombre de ciudad
    @GET("data/2.5/weather")
    Call<WeatherResponse> getCurrentWeatherByCity(
            @Query("q") String cityName,
            @Query("appid") String apiKey,
            @Query("units") String units // Ej: "metric", "imperial", "standard"
    );

    // Endpoint para obtener el clima actual por coordenadas (latitud y longitud)
    @GET("data/2.5/weather")
    Call<WeatherResponse> getCurrentWeatherByCoordinates(
            @Query("lat") double lat,
            @Query("lon") double lon,
            @Query("appid") String apiKey,
            @Query("units") String units // Ej: "metric", "imperial", "standard"
    );

    // Puedes añadir otros métodos para otros endpoints de la API (pronóstico, etc.)
}