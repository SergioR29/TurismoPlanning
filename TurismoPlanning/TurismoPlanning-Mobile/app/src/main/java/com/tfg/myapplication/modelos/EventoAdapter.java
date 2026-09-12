package com.tfg.myapplication.modelos;

import android.content.*;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.drawable.*;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.core.content.*;
import androidx.core.content.res.ResourcesCompat;
import androidx.recyclerview.widget.RecyclerView;

import com.tfg.myapplication.R;
import java.util.List;

public class EventoAdapter extends RecyclerView.Adapter<EventoViewHolder> {

    private List<Evento> listaEventos;

    // ** 1. Definir la Interfaz de Listener **
    public interface OnItemClickListener {
        void onItemClick(Evento evento); // Método que se llamará al hacer clic
    }

    // ** 2. Variable para almacenar la referencia al Listener **
    private OnItemClickListener listener;

    // Constructor del Adapter
    public EventoAdapter(List<Evento> listaEventos) {
        this.listaEventos = listaEventos;
    }

    // ** 3. Método para establecer el Listener desde fuera (Fragmento/Activity) **
    public void setOnItemClickListener(OnItemClickListener listener) {
        this.listener = listener;
    }


    @NonNull
    @Override
    public EventoViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_evento, parent, false);

        // Crear y devolver un nuevo ViewHolder con la vista inflada
        return new EventoViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull EventoViewHolder holder, int position) {
        // Obtener el objeto Evento en la posición actual
        Evento evento = listaEventos.get(position);

        // Unir los datos del objeto Evento a las vistas del ViewHolder
        holder.tituloTextView.setText(evento.getTitulo());

        try {
            if(evento.getColor() != null && !evento.getColor().isEmpty()) {
                holder.componenteEvento.setBackgroundColor(Color.parseColor(evento.getColor()));
            }
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        }

        if (evento.getFechaFin() != null && !evento.getFechaFin().isEmpty()) {
            holder.fechaFinTextView.setText("Fecha de Fin: " + evento.getFechaFin());
        } else {
            holder.fechaFinTextView.setText("Fecha de Fin: N/A");
        }

        byte[] iconoBlob = evento.getIconoBlob();
        if (iconoBlob != null && iconoBlob.length > 0) {
            Bitmap bitmap = BitmapFactory.decodeByteArray(iconoBlob, 0, iconoBlob.length);
            holder.iconoImageView.setImageBitmap(bitmap);
        } else {
            holder.iconoImageView.setImageResource(R.drawable.ic_icono);
        }

        // ** 4. Establecer el OnClickListener en el itemView del ViewHolder **
        // Mover la lógica de clic aquí desde el constructor del ViewHolder
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Obtener la posición del elemento clicado
                int position = holder.getAdapterPosition();
                // Asegurarse de que la posición sea válida y que haya un listener establecido
                if (position != RecyclerView.NO_POSITION && listener != null) {
                    // Llamar al método del listener, pasando el objeto Evento clicado
                    listener.onItemClick(listaEventos.get(position));
                }
            }
        });
    }

    @Override
    public int getItemCount() {
        return listaEventos.size();
    }

    public void setEventos(List<Evento> nuevosEventos) {
        this.listaEventos = nuevosEventos;
        notifyDataSetChanged();
    }

    public Evento getEventoAt(int position) {
        if (position >= 0 && position < listaEventos.size()) {
            return listaEventos.get(position);
        }
        return null;
    }
}
