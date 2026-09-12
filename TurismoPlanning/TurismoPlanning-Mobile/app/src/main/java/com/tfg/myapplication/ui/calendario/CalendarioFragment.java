package com.tfg.myapplication.ui.calendario;

import android.content.DialogInterface;
import android.database.*;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;
import androidx.navigation.*;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.ak.*;
import com.tfg.myapplication.GestorBD;
import com.tfg.myapplication.R;
import com.tfg.myapplication.databinding.FragmentCalendarioBinding;
import com.tfg.myapplication.modelos.Evento;
import com.tfg.myapplication.modelos.EventoAdapter;
import com.tfg.myapplication.utilidades.ImageUtils;

import java.time.Instant;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class CalendarioFragment extends Fragment implements EventoAdapter.OnItemClickListener {
    private FragmentCalendarioBinding binding;

    //Elementos UI
    private KalendarView calendario;
    private RecyclerView listadoEventos;

    //BD
    private GestorBD gestorBD;
    private SQLiteDatabase DB;

    //Variables auxiliares
    private EventoAdapter eventoAdapter;
    private List<Evento> listaDeEventos;
    String FSel;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        // Inflar el layout para este fragmento
        binding = FragmentCalendarioBinding.inflate(inflater, container, false);
        View root = binding.getRoot();
        setHasOptionsMenu(true);

        //Referencias a los elementos vía binding
        calendario = binding.calendarView;
        listadoEventos = binding.recyclerViewEventos;

        //Configurar el LayoutManager para el RecyclerView
        listadoEventos.setLayoutManager(new LinearLayoutManager(getContext()));

        //Inicializar variables auxiliares
        listaDeEventos = new ArrayList<>();
        eventoAdapter = new EventoAdapter(listaDeEventos);
        eventoAdapter.setOnItemClickListener(this);
        listadoEventos.setAdapter(eventoAdapter);

        //Obtener referencia a la BD
        gestorBD = new GestorBD(getContext());
        try {
            DB = gestorBD.openDataBase();
            Log.i("Turismo", "Conexión a la BD correcta");
        } catch(Exception e) {
            Log.e("Turismo", "Error al conectar a la BD", e);
        }

        //Configuraciones iniciales
        calendario.setInitialSelectedDate(Date.from(Instant.now()));
        cargarEventos_deHoy();
        detectarEventos_Mes();

        //Acciones
        calendario.setDateSelector(new KalendarView.DateSelector() {
            @Override
            public void onDateClicked(Date selectedDate) {
                Calendar calendar = Calendar.getInstance();
                calendar.setTime(selectedDate);

                String fechaSeleccionada = calendar.get(Calendar.DAY_OF_MONTH) + "/" + (calendar.get(Calendar.MONTH) + 1) + "/" + calendar.get(Calendar.YEAR);
                FSel = fechaSeleccionada;
                cargarEventos_dia(fechaSeleccionada);
            }
        });
        calendario.setMonthChanger(new KalendarView.MonthChanger() {
            @Override
            public void onMonthChanged(Date changedMonth) {
                detectarEventos_Mes();
            }
        });

        return root;
    }

    private void detectarEventos_Mes() {
        //Método que detecta los eventos del mes, coloreando así los días que los tienen
        try {
            if(DB == null || !DB.isOpen()) {
                Log.e("Error", "Se intentaron detectar los eventos del mes cuando no había conexión a la BD");
                return;
            }
            Calendar calendar = Calendar.getInstance();
            calendar.setTime(calendario.getShowingMonth());
            String[] args = new String[]{String.valueOf(calendar.get(Calendar.MONTH) + 1)};

            Cursor miCursor = DB.rawQuery("SELECT t.Plazo_Fecha, t.Categoria as cat, c.Color FROM Tareas t, Categorias c WHERE c.ID = cat AND CAST(SUBSTR(t.Plazo_Fecha, INSTR(t.Plazo_Fecha, '/') + 1, INSTR(SUBSTR(t.Plazo_Fecha, INSTR(t.Plazo_Fecha, '/') + 1), '/') - 1) AS INTEGER) = ?", args);
            if(miCursor.moveToFirst()) {
                List<ColoredDate> coloredDates = new ArrayList<>();
                do {
                    String plazoFecha = miCursor.getString(0);
                    LocalDate fechaFormateada = LocalDate.parse(plazoFecha, DateTimeFormatter.ofPattern("d/M/yyyy"));

                    Calendar calendar1 = Calendar.getInstance();
                    calendar1.set(fechaFormateada.getYear(), fechaFormateada.getMonthValue() - 1, fechaFormateada.getDayOfMonth());
                    Date fecha = calendar1.getTime();

                    String colorStr = miCursor.getString(2);
                    coloredDates.add(new ColoredDate(fecha, Color.parseColor(colorStr)));

                } while(miCursor.moveToNext());
                miCursor.close();

                if(calendario != null) {
                    calendario.setColoredDates(coloredDates);
                    calendario.invalidate();
                }
            } else {
                Log.i("Eventos", "Eventos no encontrados");
            }
        } catch (Exception e) {
            Log.e("Error", "Error al detectar los eventos del mes");
        }
    }

    private void cargarEventos_dia(String fechaSeleccionada) {
        //Método que carga los eventos del día seleccionado en el calendario, también actualiza los que ya hay
        listaDeEventos = new ArrayList<>();
        eventoAdapter.setEventos(listaDeEventos);

        try {
            if(DB == null) {
                Log.e("Error", "Error: Se intentó cargar los eventos de una fecha cuando la BD no estaba conectada");
                eventoAdapter.setEventos(listaDeEventos);
                return;
            }
            String[] args = new String[]{fechaSeleccionada};
            Cursor filas = DB.rawQuery("SELECT t.Titulo, t.Icono, t.Categoria, c.Color FROM Tareas t, Categorias c WHERE t.Plazo_Fecha = ? AND c.ID = t.Categoria", args);
            if(filas.moveToFirst()) {
                do {
                    String titulo = filas.getString(0);
                    byte[] icono = filas.getBlob(1);
                    String color = filas.getString(3);

                    listaDeEventos.add(new Evento(titulo, fechaSeleccionada, icono, color));
                } while(filas.moveToNext());
                filas.close();
            }

        } catch(SQLException ex) {
            Log.e("Error", "Error al cargar eventos de la fecha " + fechaSeleccionada, ex);
        } catch (IllegalArgumentException ex) {
            Log.e("Error", "Error al obtener columna de cursor", ex);
            Toast.makeText(getContext(), "Error al procesar datos de eventos.", Toast.LENGTH_SHORT).show();
        } finally {
            eventoAdapter.setEventos(listaDeEventos);
        }
    }

    private String nombreCategoria(int categoria) {
        //Método que devuelve el nombre de la categoría según su ID
        String nombre = null;
        try {
            String[] args = new String[]{String.valueOf(categoria)};
            Cursor cursor = DB.rawQuery("SELECT c.Nombre FROM Categorias c WHERE c.ID = ?", args);
            if(cursor.moveToFirst()) {
                do {
                    nombre = cursor.getString(0);
                } while(cursor.moveToNext());
                cursor.close();
            }

        } catch(SQLException ex) {
            Log.e("Error", "Error al obtener nombre de la categoría", ex);
        }
        return nombre;
    }

    private void cargarEventos_deHoy() {
        //Método que carga los eventos de la fecha de hoy automáticamente
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(calendario.getSelectedDate());

        String fechaSeleccionada = calendar.get(Calendar.DAY_OF_MONTH) + "/" + (calendar.get(Calendar.MONTH) + 1) + "/" + calendar.get(Calendar.YEAR);
        Log.i("Fecha de hoy", fechaSeleccionada);

        try {
            if(DB == null) {
                Log.e("Error", "Error: Se intentó cargar los eventos de una fecha cuando la BD no estaba conectada");
                eventoAdapter.setEventos(listaDeEventos);
                return;
            }
            String[] args = new String[]{fechaSeleccionada};
            Cursor filas = DB.rawQuery("SELECT t.Titulo, t.Icono, t.Categoria, c.Color FROM Tareas t, Categorias c WHERE t.Plazo_Fecha = ? AND c.ID = t.Categoria", args);
            if(filas.moveToFirst()) {
                do {
                    String titulo = filas.getString(0);
                    byte[] icono = filas.getBlob(1);
                    String color = filas.getString(3);

                    listaDeEventos.add(new Evento(titulo, fechaSeleccionada, icono, color));
                } while(filas.moveToNext());
                filas.close();
            }

        } catch(SQLException ex) {
            Log.e("Error", "Error al cargar eventos de la fecha " + LocalDate.now().getDayOfMonth() + "/" + LocalDate.now().getMonthValue() + "/" + LocalDate.now().getYear(), ex);
        } catch (IllegalArgumentException ex) {
            Log.e("Error", "Error al obtener columna de cursor", ex);
            Toast.makeText(getContext(), "Error al procesar datos de eventos.", Toast.LENGTH_SHORT).show();
        } catch (Exception ex) {
            Log.e("Error", "Error inesperado al cargar eventos de la fecha " + fechaSeleccionada, ex);
            Toast.makeText(getContext(), "Error inesperado al cargar eventos.", Toast.LENGTH_SHORT).show();
        }
        finally {
            eventoAdapter.setEventos(listaDeEventos);
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    @Override
    public void onCreateOptionsMenu(@NonNull Menu menu, @NonNull MenuInflater inflater) {
        super.onCreateOptionsMenu(menu, inflater);
        inflater.inflate(R.menu.calendario, menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if(id == R.id.action_ayudaC) {
            AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
            builder.setTitle("Ayuda");
            builder.setMessage("Este calendario ha sido diseñado para poder ver una lista de eventos de un día seleccionado en el calendario.\n\nAl pulsar a un evento se verán sus datos completos, y también se pueden editar o eliminar directamente el evento.");
            builder.setIcon(R.drawable.ic_ayuda);

            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                }
            });

            AlertDialog dialog = builder.create();
            dialog.show();

            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onItemClick(Evento evento) {
        String tituloEvento = evento.getTitulo();
        if(!tituloEvento.isEmpty()) {
            try {
                if(DB == null) {
                    Log.e("Error", "Error: Se intentó cargar el evento de una fecha cuando la BD no estaba conectada");
                    return;
                }
                String[] args = new String[]{tituloEvento};
                Cursor cursor = DB.rawQuery("SELECT t.Fecha_Inicio, t.Hora_Inicio, t.Plazo_Hora, t.Prioridad, t.Categoria, t.Descripcion FROM Tareas t WHERE t.Titulo = ?", args);
                if(cursor.moveToFirst()) {
                    String fechaInicio, horaInicio, horaFin, descE;
                    String nombreC;

                    int prioridad, categoria;
                    do {
                        fechaInicio = cursor.getString(0);
                        horaInicio = cursor.getString(1);
                        horaFin = cursor.getString(2);

                        prioridad = cursor.getInt(3);
                        categoria = cursor.getInt(4);
                        nombreC = nombreCategoria(categoria);
                        descE = cursor.getString(5);

                    } while(cursor.moveToNext());
                    cursor.close();

                    //Preparar datos para el diálogo
                    String datos = (!fechaInicio.isEmpty() ? ("Fecha de Inicio: " + fechaInicio + "\n") : "") +
                            (!horaInicio.isEmpty() ? ("Hora de Inicio: " + horaInicio + "\n") : "") +
                            (!fechaInicio.isEmpty() && !horaInicio.isEmpty() ? "\n" : "") +

                            ("Fecha de Finalización: " + evento.getFechaFin()) + "\n" +
                            (!horaFin.isEmpty() ? ("Hora de Finalización: " + horaFin + "\n\n") : "\n") +

                            ("Categoría: " + nombreC) + "\n" +
                            ("Prioridad: " + prioridad) +
                            "\n\n\n" +
                            descE +
                            "\n\n";
                    Drawable icDialogo = ImageUtils.byteArrayToDrawable(getContext(), evento.getIconoBlob());

                    //Construir el diálogo
                    AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                    builder.setTitle(tituloEvento);
                    builder.setMessage(datos);
                    builder.setIcon(icDialogo);

                    builder.setNeutralButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                           dialog.dismiss();
                        }
                    });
                    builder.setNegativeButton("EDITAR", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            try {
                                NavController navController = Navigation.findNavController(requireActivity(), R.id.nav_host_fragment_content_main);
                                Bundle bundle = new Bundle();
                                bundle.putString("tituloE", evento.getTitulo());
                                navController.navigate(R.id.nav_planificar, bundle);

                            } catch(Exception ex) {
                                ex.printStackTrace();
                            }
                        }
                    });
                    builder.setPositiveButton("ELIMINAR", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            try {
                                int eliminado = DB.delete("Tareas", "Titulo = '" + evento.getTitulo() + "'", null);
                                if(eliminado > 0) {
                                    Toast.makeText(getContext(), "Evento " + evento.getTitulo() + " eliminado correctamente", Toast.LENGTH_LONG).show();
                                    cargarEventos_dia(FSel != null ? FSel : (LocalDate.now().getDayOfMonth() + "/" + LocalDate.now().getMonthValue() + "/" + LocalDate.now().getYear()));
                                } else {
                                    Toast.makeText(getContext(), "Error al eliminar el evento " + evento.getTitulo(), Toast.LENGTH_LONG).show();
                                }
                            } catch(SQLException ex) {
                                Log.e("Error", "Error al eliminar el evento " + evento.getTitulo(), ex);
                            }
                        }
                    });

                    AlertDialog dialog = builder.create();
                    dialog.show();
                } else {
                    Log.e("Error", "BD no disponible");
                }

            } catch(SQLException ex) {
                Log.e("Error", "Error al cargar evento", ex);
            }
        } else {
            Log.i("Error", "Título del evento vacío");
        }
    }
}
