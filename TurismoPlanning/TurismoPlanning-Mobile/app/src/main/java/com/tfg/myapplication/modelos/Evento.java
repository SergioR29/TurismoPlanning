package com.tfg.myapplication.modelos;

import android.graphics.drawable.Drawable;

public class Evento {
    private String titulo;
    private String fechaFin;
    private byte[] iconoBlob; // <-- Ahora es un byte[] para el icono (Blob)
    private String color;
    private Drawable estilo;
    // Puedes añadir más propiedades según necesites (descripción, color, etc.)

    // Constructor
    public Evento(String titulo, String fechaFin, byte[] iconoBlob, String color) {
        this.titulo = titulo;
        this.fechaFin = fechaFin;
        this.iconoBlob = iconoBlob;
        this.color = color;
    }

    public Drawable getEstilo() {
        return estilo;
    }

    public void setEstilo(Drawable estilo) {
        this.estilo = estilo;
    }

    // Getters
    public String getTitulo() {
        return titulo;
    }

    public String getFechaFin() {
        return fechaFin;
    }

    public byte[] getIconoBlob() {
        return iconoBlob;
    }

    public String getColor() {
        return color;
    }

    // Opcional: toString() para depuración
    @Override
    public String toString() {
        return "Evento{" +
                ", titulo='" + titulo + '\'' +
                ", fechaFin=" + fechaFin +
                ", iconoBlob=" + (iconoBlob != null ? iconoBlob.length + " bytes" : "null") + // Mostrar tamaño del blob o null
                ", color=" + color +
                '}';
    }
}
