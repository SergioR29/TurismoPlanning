package com.tfg.myapplication.ui.home;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class HomeViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public HomeViewModel() {
        mText = new MutableLiveData<>();
        //mText.setValue("Bienvenido a tu mejor organizador diario y guía turístico, para empezar haz clic a las 3 barras de la esquina superior-izquierda para ver todas las opciones disponibles de uso.\n\nPulsa al icono de 3 puntos situado en la esquina superior derecha para ver información adicional de la aplicación.\n\nPulsa al botón de la esquina inferior derecha para volver al inicio de esta genial app");
    }

    public LiveData<String> getText() {
        return mText;
    }
}