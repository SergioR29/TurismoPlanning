package com.tfg.myapplication.ui.sitios;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class SitiosViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public SitiosViewModel() {
        mText = new MutableLiveData<>();
    }

    public LiveData<String> getText() {
        return mText;
    }
}
