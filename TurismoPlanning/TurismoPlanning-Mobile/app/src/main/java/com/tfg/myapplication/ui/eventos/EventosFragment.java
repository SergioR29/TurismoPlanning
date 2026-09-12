package com.tfg.myapplication.ui.eventos;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.drawable.Drawable;
import android.net.Uri;
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
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.itextpdf.html2pdf.HtmlConverter;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.tfg.myapplication.GestorBD;
import com.tfg.myapplication.R;
import com.tfg.myapplication.databinding.FragmentEventosBinding;
import com.tfg.myapplication.modelos.*;
import com.tfg.myapplication.utilidades.DataUtils;
import com.tfg.myapplication.utilidades.ImageUtils;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class EventosFragment extends Fragment implements EventoAdapter.OnItemClickListener {
    private FragmentEventosBinding binding;

    //Elementos de la UI
    private Spinner listaCategorias;
    private TextView titulo;
    private RecyclerView listaEventos;

    //BD
    private GestorBD gestorBD;
    private SQLiteDatabase DB;

    //Variables auxiliares
    String nameCatSel = "Seleccione una categoría";
    int IDcatSel;

    private List<Evento> eventos;
    private EventoAdapter eventoAdapter;

    //Plantilla HTML
    String cabeceraHTML = "<!DOCTYPE html><html><head><style>#ic_Tarea{width:52px; height:52px;margin-right:10px;text-align:left;padding-left:5px;border:none;}#titulo{padding-top:5px;font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 20px; margin-right: 10px}#desc{font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 15px;}table{border:none;margin-bottom:20px;}td{margin-right:10px;}</style></head>";
    String cabeceraPDF = "<!DOCTYPE html><html><head><style>#ic_Tarea{width:52px; height:52px;margin-right:10px;text-align:left;padding-left:5px;border:none;}#titulo{padding-top:5px;font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 20px; margin-right: 10px}#desc{font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 15px;}table{border:none;margin-bottom:20px;}td{margin-right:10px;}</style></head>";

    String infoHTML, infoPDF;
    String pieHTML = "</body></html>";

    String HTML, PDF;

    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        //Inflar el layout para este fragmento
        binding = FragmentEventosBinding.inflate(inflater, container, false);
        View root = binding.getRoot();
        setHasOptionsMenu(true);

        //Inicializar los elementos mediante vía binding
        listaCategorias = binding.ListaCategorias;
        titulo = binding.titulo;
        listaEventos = binding.recyclerViewEventos;

        //Obtener conexión a la BD
        gestorBD = new GestorBD(getContext());
        try {
            DB = gestorBD.openDataBase();
            Log.i("Turismo", "Conexión a la BD correcta");
        } catch(Exception e) {
            Log.e("Turismo", "Error al conectar a la BD", e);
        }

        //Configurar el LayoutManager para el RecyclerView
        listaEventos.setLayoutManager(new LinearLayoutManager(getContext()));

        //Inicializar variables auxiliares
        eventos = new ArrayList<>();
        eventoAdapter = new EventoAdapter(eventos);
        eventoAdapter.setOnItemClickListener(this);
        listaEventos.setAdapter(eventoAdapter);

        //Configuraciones iniciales
        cargarCategorias();

        //Acciones
        listaCategorias.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                infoHTML = "";
                infoPDF = "";

                nameCatSel = (parent.getItemAtPosition(position)).toString();
                IDcatSel = obtenerIDCat();

                int posSpinner = getSpinnerPositionByText(listaCategorias, nameCatSel);
                if(posSpinner > 0) cargarEventosCat();
                else titulo.setText("NO SE HA SELECCIONADO UNA CATEGORÍA");
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });
        return root;
    }

    private void cargarEventosCat() {
        //Método que carga los eventos asociados a una categoría seleccionada
        eventos = new ArrayList<>();
        eventoAdapter.setEventos(eventos);
        try {
            if(DB == null) {
                Log.e("Error", "Error: Se intentó cargar los eventos de una fecha cuando la BD no estaba conectada");
                eventoAdapter.setEventos(eventos);
                return;
            }
            String[] args = new String[]{String.valueOf(IDcatSel), String.valueOf(IDcatSel)};
            Cursor filas = DB.rawQuery("SELECT t.Titulo, t.Icono, t.Plazo_Fecha, c.Color, t.Fecha_Inicio FROM Tareas t, Categorias c WHERE c.ID = ? AND t.Categoria = ?", args);
            if(filas.moveToFirst()) {
                do {
                    String titulo = filas.getString(0);
                    byte[] icono = filas.getBlob(1);
                    String FF = filas.getString(2);
                    String color = filas.getString(3);
                    String fechaI = filas.getString(4);

                    eventos.add(new Evento(titulo, FF, icono, color));
                    String desc = !fechaI.isEmpty() ? (fechaI + " hasta el " + FF) : FF;

                    String iconoB64 = DataUtils.byteArrayToBase64(icono);
                    infoHTML += "<table id=\"contenedor\"><tr><td><img id=\"ic_Tarea\" src=\"" + "data:image/png;base64," + iconoB64 + "\"/></td></tr><tr><td id=\"titulo\"><strong>" + titulo + "</strong></td></tr><tr><td id=\"desc\">" + desc + "</td></tr></table>";
                    infoPDF += "<table id=\"contenedor\"><tr><td><img id=\"ic_Tarea\" src=\"" + "data:image/png;base64," + iconoB64 + "\"/></td></tr><tr><td id=\"titulo\"><strong>" + titulo + "</strong></td></tr><tr><td id=\"desc\">" + desc + "</td></tr></table>";

                } while(filas.moveToNext());
                filas.close();
            } else {
                titulo.setText("NO HAY EVENTOS CREADOS");
            }

        } catch(SQLException ex) {
            Log.e("Error", "Error al cargar eventos de la categoría " + nameCatSel, ex);
        } catch (IllegalArgumentException ex) {
            Log.e("Error", "Error al obtener columna de cursor", ex);
            Toast.makeText(getContext(), "Error al procesar datos de eventos.", Toast.LENGTH_SHORT).show();
        } finally {
            if(!eventos.isEmpty()) eventoAdapter.setEventos(eventos);
            else titulo.setText("NO HAY EVENTOS CREADOS");
        }
    }

    private int obtenerIDCat() {
        //Método que devuelve el ID de una categoría seleccionada
        try {
            if(DB == null || !DB.isOpen()) {
                Log.e("Error", "BD no conectada");
                return 0;
            }
            String[] args = new String[]{nameCatSel};
            Cursor miCursor = DB.rawQuery("SELECT c.ID FROM Categorias c WHERE c.Nombre = ?", args);
            if(miCursor.moveToFirst()) {
                do {
                    IDcatSel = miCursor.getInt(0);
                } while(miCursor.moveToNext());
                miCursor.close();

                titulo.setText("EVENTOS Y TAREAS");
            } else if(!nameCatSel.equals("Seleccione una categoría")) {
                titulo.setText("NO HAY EVENTOS CREADOS");
                eventos = new ArrayList<>();
                eventoAdapter.setEventos(eventos);
            } else {
                eventos = new ArrayList<>();
                eventoAdapter.setEventos(eventos);
            }

        } catch(SQLException ex) {
            Log.e("Error", "Error al cargar el ID de la categoría " + nameCatSel, ex);
        }
        return IDcatSel;
    }

    /**
     * Busca la posición de un elemento en un Spinner por su texto.
     *
     * @param spinner El Spinner en el que buscar.
     * @param text El texto del elemento que se busca.
     * @return La posición del elemento si se encuentra, o -1 si no se encuentra.
     */
    public int getSpinnerPositionByText(Spinner spinner, String text) {
        // Verifica si el Spinner o el texto son nulos
        if (spinner == null || text == null) {
            return -1;
        }

        // Obtener el adaptador del Spinner
        SpinnerAdapter adapter = spinner.getAdapter();

        // Verificar si el adaptador no es nulo y tiene elementos
        if (adapter != null) {
            // Iterar a través de los elementos del adaptador
            for (int i = 0; i < adapter.getCount(); i++) {
                // Obtener el elemento en la posición actual
                Object item = adapter.getItem(i);

                // Convertir el elemento a String y comparar con el texto buscado
                // Puedo necesitar ajustar la conversión a String dependiendo del tipo de objeto en mi adaptador
                if (item != null && item.toString().equals(text)) {
                    // Si el texto coincide, devolver la posición actual
                    return i;
                }
            }
        }

        // Si el texto no se encontró después de iterar por todos los elementos, devolver -1
        return -1;
    }

    private void cargarCategorias() {
        //Método que carga las categorías del usuario
        try {
            if(DB == null) {
                Log.e("Categorías", "Error: La base de datos no está abierta al cargar el listado de categorías ");
                return;
            }

            Cursor filas = DB.rawQuery("SELECT c.Nombre FROM Categorias c", null);
            if(filas.moveToFirst()) {
                String[] listado = new String[filas.getCount() + 1];
                listado[0] = "Seleccione una categoría";
                nameCatSel = "Seleccione una categoría";

                int i=1;
                do {
                    String nombre = filas.getString(0);
                    listado[i] = nombre;
                    i++;
                } while(filas.moveToNext());
                filas.close();

                ArrayAdapter<String> adapter = new ArrayAdapter<>(requireContext(), R.layout.custom_spinner_item, listado);
                adapter.setDropDownViewResource(androidx.appcompat.R.layout.support_simple_spinner_dropdown_item);
                listaCategorias.setAdapter(adapter);
                listaCategorias.setSelection(0);
            } else {
                titulo.setText("NO HAY EVENTOS CREADOS");
            }
        } catch(SQLException ex) {
            Log.e("Turismo", "Error al cargar la información de las categorías", ex);
        }
    }

    // Manejar el resultado de los Intents de crear documento (HTML o PDF)
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        // Manejar el resultado de la exportación HTML
        if (requestCode == 2 && resultCode == Activity.RESULT_OK) {
            handleExportResult(data, "HTML");
        }
        // Manejar el resultado de la exportación PDF
        else if (requestCode == 3 && resultCode == Activity.RESULT_OK) {
            handleExportResult(data, "PDF");
        } else {
            // El usuario canceló el diálogo o ocurrió un error para cualquier Intent
            Toast.makeText(getContext(), "Guardado de archivo cancelado.", Toast.LENGTH_SHORT).show();
        }
    }

    // Método auxiliar para manejar el resultado de la exportación (HTML o PDF)
    private void handleExportResult(Intent data, String fileType) {
        if (data != null && data.getData() != null) {
            Uri fileUri = data.getData(); // Esta es la Uri del archivo que el usuario eligió crear

            OutputStream outputStream = null;
            try {
                outputStream = requireContext().getContentResolver().openOutputStream(fileUri);

                if (outputStream != null) {
                    if ("HTML".equals(fileType)) {
                        // --- Escribir el contenido HTML en el flujo de salida ---
                        if (HTML != null) {
                            byte[] htmlBytes = HTML.getBytes(StandardCharsets.UTF_8);
                            outputStream.write(htmlBytes);
                            Toast.makeText(getContext(), "Archivo HTML exportado exitosamente.", Toast.LENGTH_LONG).show();
                        } else {
                            Toast.makeText(getContext(), "El contenido HTML a exportar es nulo.", Toast.LENGTH_SHORT).show();
                        }

                    } else if ("PDF".equals(fileType)) {
                        // --- Convertir HTML a PDF usando iText y escribir en el flujo ---
                        if (PDF != null) {
                            PdfWriter writer = new PdfWriter(outputStream);
                            com.itextpdf.kernel.pdf.PdfDocument pdfDocument = new com.itextpdf.kernel.pdf.PdfDocument(writer);
                            Document document = new Document(pdfDocument); // iText Document class

                            // Usar HtmlConverter para convertir la cadena HTML a PDF
                            HtmlConverter.convertToPdf(PDF, pdfDocument.getWriter()); // Convertir directamente a PdfDocument

                            // No es necesario cerrar el 'document' o 'pdfDocument' explícitamente
                            // HtmlConverter.convertToPdf() y PdfWriter gestionan el cierre del stream

                            Toast.makeText(getContext(), "Archivo PDF exportado exitosamente.", Toast.LENGTH_LONG).show();

                        } else {
                            Toast.makeText(getContext(), "El contenido HTML para generar el PDF es nulo.", Toast.LENGTH_SHORT).show();
                        }
                    }

                } else {
                    Toast.makeText(getContext(), "Error al obtener el flujo de salida para la Uri.", Toast.LENGTH_LONG).show();
                }

            } catch (IOException e) {
                e.printStackTrace();
                Toast.makeText(getContext(), "Error de E/S al escribir el archivo: " + e.getMessage(), Toast.LENGTH_LONG).show();
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(getContext(), "Ocurrió un error inesperado durante la exportación: " + e.getMessage(), Toast.LENGTH_LONG).show();
            } finally {
                // Asegurarse de que el flujo se cierra si no fue cerrado por la librería de escritura
                // En el caso de iText HtmlConverter.convertToPdf(), el writer y el stream se cierran.
                // Para la escritura directa de bytes (HTML), cerramos explícitamente.
                if (outputStream != null && "HTML".equals(fileType)) {
                    try {
                        outputStream.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }

        } else {
            // El resultado fue OK, pero no se recibió una Uri (esto es inusual)
            Toast.makeText(getContext(), "No se recibió una Uri para guardar el archivo.", Toast.LENGTH_SHORT).show();
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
        inflater.inflate(R.menu.eventos, menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if(id == R.id.action_ayudaE) {
            AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
            builder.setTitle("Ayuda");
            builder.setMessage("En esta sección se puede visualizar un listado de eventos pertenecientes a la categoría seleccionada. Si se pulsa sobre uno de ellos se pueden modificar sus datos o incluso eliminarlo. También se puede exportar el listado a PDF o HTML.");
            builder.setIcon(R.drawable.ic_ayuda);

            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                }
            });

            AlertDialog dialog = builder.create();
            dialog.show();

        } else if(id == R.id.action_exportar_html) {
            HTML = cabeceraHTML + infoHTML + pieHTML;

            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("text/html");
            intent.putExtra(Intent.EXTRA_TITLE, "ListadoEventos - " + nameCatSel + ".html");

            try {
                startActivityForResult(intent, 2);
            } catch(Exception e) {
                Toast.makeText(getContext(), "No se pudo abrir el diálogo de guardado: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }

        } else if(id == R.id.action_exportar_pdf) {
            PDF = cabeceraPDF + infoPDF + pieHTML;

            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("application/pdf");
            intent.putExtra(Intent.EXTRA_TITLE, "ListadoEventos - " + nameCatSel + ".pdf");

            try {
                startActivityForResult(intent, 3);
            } catch(Exception e) {
                Toast.makeText(getContext(), "No se pudo abrir el diálogo de guardado: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }
        }
        return super.onOptionsItemSelected(item);
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
                                    cargarEventosCat();
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
