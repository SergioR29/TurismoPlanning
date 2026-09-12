package com.tfg.myapplication.ui.categorias;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class CategoriasViewModel extends ViewModel {
    private final MutableLiveData<String> mText;

    public CategoriasViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("Categorias");
    }
    public LiveData<String> getText() {
        return mText;
    }
    public void setText(String text) {
        mText.setValue(text);
    }
}
