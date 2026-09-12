package com.tfg.myapplication.clima;

import com.google.gson.annotations.SerializedName;

// Clase para cada objeto dentro del array "weather" (descripción del clima)
public class Weather {
    @SerializedName("id")
    private int id;
    @SerializedName("main")
    private String main; // Ej: "Clear", "Clouds", "Rain"
    @SerializedName("description")
    private String description; // Ej: "clear sky", "few clouds", "light rain"
    @SerializedName("icon")
    private String icon; // Código del icono (ej: "01d", "10n")

    public int getId() {
        return id;
    }

    public String getMain() {
        return main;
    }

    public String getDescription() {
        return description;
    }

    public String getIcon() {
        return icon;
    }
}