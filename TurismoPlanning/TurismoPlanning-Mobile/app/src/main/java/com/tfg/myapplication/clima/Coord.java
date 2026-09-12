package com.tfg.myapplication.clima;

import com.google.gson.annotations.SerializedName;

// Clase para la sección "coord" de la respuesta JSON (coordenadas de la ubicación)
public class Coord {
    @SerializedName("lon")
    private double lon;
    @SerializedName("lat")
    private double lat;

    public double getLon() {
        return lon;
    }

    public double getLat() {
        return lat;
    }
}