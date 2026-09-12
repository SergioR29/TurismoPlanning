package com.tfg.myapplication.clima;

import com.google.gson.annotations.SerializedName;

// Clase para la sección "sys" de la respuesta JSON (información del sistema, país, amanecer, atardecer)
public class Sys {
    @SerializedName("type")
    private int type;
    @SerializedName("id")
    private int id;
    @SerializedName("country")
    private String country; // Código del país (ej: "ES")
    @SerializedName("sunrise")
    private long sunrise; // Hora del amanecer (tiempo UNIX, UTC)
    @SerializedName("sunset")
    private long sunset; // Hora del atardecer (tiempo UNIX, UTC)

    public int getType() {
        return type;
    }

    public int getId() {
        return id;
    }

    public String getCountry() {
        return country;
    }

    public long getSunrise() {
        return sunrise;
    }

    public long getSunset() {
        return sunset;
    }
}