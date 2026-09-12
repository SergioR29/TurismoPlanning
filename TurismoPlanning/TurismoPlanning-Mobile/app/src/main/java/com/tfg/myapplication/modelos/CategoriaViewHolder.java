package com.tfg.myapplication.modelos;

import android.view.View;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.tfg.myapplication.R;

public class CategoriaViewHolder extends RecyclerView.ViewHolder {

    //Referencias a las vistas del layout item_category.xml
    public View colorCat;
    public TextView prioridadCat;
    public TextView nombreCat;

    public CategoriaViewHolder(@NonNull View itemView) {
        super(itemView);

        //Obtener referencias a las vistas
        colorCat = itemView.findViewById(R.id.colorCategoria);
        prioridadCat = itemView.findViewById(R.id.prioridad_Categoria);
        nombreCat = itemView.findViewById(R.id.nombre_Categoria);

        itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int position = getAdapterPosition();
                if(position == RecyclerView.NO_POSITION) {
                    //No se ha encontrado el elemento
                }
            }
        });
    }
}
