package com.tfg.myapplication.clima;

import com.google.gson.annotations.SerializedName;

// Clase principal que representa la respuesta completa de la API de clima actual
public class WeatherResponse {
    @SerializedName("coord")
    private Coord coord;
    @SerializedName("weather")
    private Weather[] weather; // Array de objetos Weather (puede haber más de uno, aunque usualmente el primero es el principal)
    @SerializedName("base")
    private String base;
    @SerializedName("main")
    private Main main; // Información principal (temperatura, humedad, etc.)
    @SerializedName("visibility")
    private int visibility;
    @SerializedName("wind")
    private Wind wind;
    @SerializedName("clouds")
    private Clouds clouds;
    @SerializedName("dt")
    private long dt; // Tiempo de cálculo de datos (tiempo UNIX, UTC)
    @SerializedName("sys")
    private Sys sys; // Información del sistema (país, amanecer, atardecer)
    @SerializedName("timezone")
    private int timezone; // Zona horaria en segundos
    @SerializedName("id")
    private int id; // ID de la ciudad
    @SerializedName("name")
    private String name; // Nombre de la ciudad
    @SerializedName("cod")
    private int cod; // Código de respuesta HTTP de la API (ej: 200 para éxito)

    public Coord getCoord() {
        return coord;
    }

    public Weather[] getWeather() {
        return weather;
    }

    public String getBase() {
        return base;
    }

    public Main getMain() {
        return main;
    }

    public int getVisibility() {
        return visibility;
    }

    public Wind getWind() {
        return wind;
    }

    public Clouds getClouds() {
        return clouds;
    }

    public long getDt() {
        return dt;
    }

    public Sys getSys() {
        return sys;
    }

    public int getTimezone() {
        return timezone;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getCod() {
        return cod;
    }
}