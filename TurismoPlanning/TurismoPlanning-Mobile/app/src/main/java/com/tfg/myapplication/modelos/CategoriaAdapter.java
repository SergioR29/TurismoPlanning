package com.tfg.myapplication.modelos;

import android.graphics.Color;
import android.view.*;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.tfg.myapplication.R;

import java.util.List;

public class CategoriaAdapter extends RecyclerView.Adapter<CategoriaViewHolder>{
    private List<Categoria> listaCategorias;

    public CategoriaAdapter(List<Categoria> listaCategorias) {
        this.listaCategorias = listaCategorias;
    }

    @NonNull
    @Override
    public CategoriaViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_category, parent, false);
        return new CategoriaViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull CategoriaViewHolder holder, int position) {
        //Obtener la categoría en la posición actual
        Categoria categoria = listaCategorias.get(position);

        //Unir los datos del objeto Categoria a las vistas del ViewHolder
        try {
            if(categoria.getColor() != null && !categoria.getColor().isEmpty()) holder.colorCat.setBackgroundColor(Color.parseColor(categoria.getColor()));
        } catch(IllegalArgumentException ex) {
            ex.printStackTrace();
        }

        holder.prioridadCat.setText(categoria.getPrioridad() + "º)");
        holder.nombreCat.setText(categoria.getNombre());
    }

    @Override
    public int getItemCount() {
        return listaCategorias.size();
    }

    public void setCategorias(List<Categoria> nuevasCategorias) {
        this.listaCategorias = nuevasCategorias;
        notifyDataSetChanged();
    }

    public Categoria getCategoriaAt(int position) {
        if(position >= 0 && position < listaCategorias.size()) {
            return listaCategorias.get(position);
        }
        return null;
    }
}
