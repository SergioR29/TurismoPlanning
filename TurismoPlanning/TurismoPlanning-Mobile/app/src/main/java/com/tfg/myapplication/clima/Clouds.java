package com.tfg.myapplication.clima;

import com.google.gson.annotations.SerializedName;

// Clase para la sección "clouds" de la respuesta JSON (nubosidad)
public class Clouds {
    @SerializedName("all")
    private int all; // Porcentaje de nubosidad

    public int getAll() {
        return all;
    }
}