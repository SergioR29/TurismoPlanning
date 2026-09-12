package com.tfg.myapplication.ui.notas;

import androidx.lifecycle.*;

public class NotasViewModel extends ViewModel {
    private MutableLiveData<String> mText;

    public NotasViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is notifications fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }

    public void setText(String text) {
        mText.setValue(text);
    }
}
