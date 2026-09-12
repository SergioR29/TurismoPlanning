package com.tfg.myapplication.clima;

import com.google.gson.annotations.SerializedName;

// Clase para la sección "main" de la respuesta JSON (temperatura, humedad, presión, etc.)
public class Main {
    @SerializedName("temp")
    private double temp; // Temperatura
    @SerializedName("feels_like")
    private double feelsLike; // Sensación térmica
    @SerializedName("temp_min")
    private double tempMin; // Temperatura mínima actual
    @SerializedName("temp_max")
    private double tempMax; // Temperatura máxima actual
    @SerializedName("pressure")
    private int pressure; // Presión atmosférica (hPa)
    @SerializedName("humidity")
    private int humidity; // Humedad (%)
    @SerializedName("sea_level")
    private int seaLevel; // Presión a nivel del mar (si está disponible)
    @SerializedName("grnd_level")
    private int grndLevel; // Presión a nivel del suelo (si está disponible)

    // Por defecto, la temperatura viene en Kelvin.
    // Puedo añadir el parámetro 'units' en la petición API ("metric" para Celsius, "imperial" para Fahrenheit)
    // para recibir la temperatura directamente en la unidad deseada.

    public double getTemp() {
        return temp;
    }

    public double getFeelsLike() {
        return feelsLike;
    }

    public double getTempMin() {
        return tempMin;
    }

    public double getTempMax() {
        return tempMax;
    }

    public int getPressure() {
        return pressure;
    }

    public int getHumidity() {
        return humidity;
    }

    public int getSeaLevel() {
        return seaLevel;
    }

    public int getGrndLevel() {
        return grndLevel;
    }
}