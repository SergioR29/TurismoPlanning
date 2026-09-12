package com.tfg.myapplication.clima;

import com.google.gson.annotations.SerializedName;

// Clase para la sección "wind" de la respuesta JSON (velocidad y dirección del viento)
public class Wind {
    @SerializedName("speed")
    private double speed; // Velocidad del viento
    @SerializedName("deg")
    private int deg; // Dirección del viento en grados (meteorológicos)
    @SerializedName("gust")
    private double gust; // Ráfaga de viento (si está disponible)

    public double getSpeed() {
        return speed;
    }

    public int getDeg() {
        return deg;
    }

    public double getGust() {
        return gust;
    }
}