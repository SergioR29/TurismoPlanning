package com.tfg.myapplication.modelos;

public class Categoria {
    private String color;
    private int prioridad;
    private String nombre;

    public Categoria(String color, int prioridad, String nombre) {
        this.color = color;
        this.prioridad = prioridad;
        this.nombre = nombre;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public int getPrioridad() {
        return prioridad;
    }

    public void setPrioridad(int prioridad) {
        this.prioridad = prioridad;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
}
