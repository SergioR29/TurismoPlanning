package com.tfg.myapplication.ui.planificacion;

import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class PlanificarViewModel extends ViewModel {
    private final MutableLiveData<String> mText;

    public PlanificarViewModel(MutableLiveData<String> mText) {
        this.mText = mText;
    }

    public MutableLiveData<String> getText() {
        return mText;
    }

    public void setText(String text) {
        mText.setValue(text);
    }
}
