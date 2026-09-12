package com.tfg.myapplication.ui.calendario;

import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class CalendarioViewModel extends ViewModel {
    private final MutableLiveData<String> mText;

    public CalendarioViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is calendario fragment");
    }
    public MutableLiveData<String> getText() {
        return mText;
    }
}
