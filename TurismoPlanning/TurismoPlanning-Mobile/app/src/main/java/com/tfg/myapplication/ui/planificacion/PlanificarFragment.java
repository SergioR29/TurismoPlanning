package com.tfg.myapplication.ui.planificacion;

import static android.app.Activity.RESULT_OK;

import android.app.*;
import android.content.ContentValues;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.res.ColorStateList;
import android.database.*;
import android.database.sqlite.*;
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
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;

import com.itextpdf.html2pdf.HtmlConverter;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.skydoves.colorpickerview.*;
import com.skydoves.colorpickerview.listeners.ColorEnvelopeListener;
import com.tfg.myapplication.GestorBD;
import com.tfg.myapplication.R;
import com.tfg.myapplication.databinding.FragmentPlanificarBinding;
import com.tfg.myapplication.utilidades.ImageUtils;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.Calendar;

public class PlanificarFragment extends Fragment {
    private FragmentPlanificarBinding binding;

    //Elementos de la UI
    private ImageButton ic_Evento;
    private EditText titulo;
    private EditText FI;
    private EditText FF;
    private EditText HI;
    private EditText HF;
    private Spinner listaCategorias;
    private ImageButton crearCat;
    private EditText prioridad;
    private EditText descEvento;

    //BD
    private GestorBD gestorBD;
    private SQLiteDatabase DB;

    //Plantilla HTML
    String html;

    //Variables auxiliares
    String tituloVisita;
    String colorSel;
    boolean vecesImgSel;

    String nombreCatSel;
    int IDcatSel;

    String tituloEditar;
    boolean editarEvento;

    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        binding = FragmentPlanificarBinding.inflate(inflater, container, false);
        setHasOptionsMenu(true);
        View root = binding.getRoot();

        //Obtener elementos mediante vía binding
        ic_Evento = binding.icEvento;
        titulo = binding.tituloEvento;
        FI = binding.editTextDateFI;
        FF = binding.editTextDateFF;
        HI = binding.editTextDateHI;
        HF = binding.editTextDateHF;
        listaCategorias = binding.ListaCategorias;
        crearCat = binding.imageButtonCrearCategoria;
        prioridad = binding.prioridadCategoriaEditText;
        descEvento = binding.descTarea;

        //Obtener referencia a la BD
        gestorBD = new GestorBD(getContext());
        try {
            DB = gestorBD.openDataBase();
            Log.i("Turismo", "Conexión a la BD correcta");
        } catch(Exception e) {
            Log.e("Turismo", "Error al conectar a la BD", e);
        }

        //Configuraciones importantes
        cargarCategorias();

        if(getArguments() != null) {
            tituloVisita = getArguments().getString("tituloV", "");
            if(!tituloVisita.isEmpty()) {
                titulo.setText(tituloVisita);
                editarEvento = false;
            }

            //Para editar un evento
            tituloEditar = getArguments().getString("tituloE", "");
            if(!tituloEditar.isEmpty()) {
                titulo.setText(tituloEditar);
                editarEvento = true;

                sacarDatosEditar();
            } else {
                editarEvento = false;
            }
        }

        //Acciones
        ic_Evento.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.setType("image/*"); // Solo imágenes
                intent.addCategory(Intent.CATEGORY_OPENABLE);

                try {
                    startActivityForResult(Intent.createChooser(intent, "Selecciona una imagen"), 1);
                } catch (Exception e) {
                    e.printStackTrace();
                    Toast.makeText(getContext(), "Error al cargar la imagen", Toast.LENGTH_SHORT).show();
                }
            }
        });

        FI.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final Calendar calen = Calendar.getInstance();
                int year = calen.get(Calendar.YEAR);
                int month = calen.get(Calendar.MONTH);
                int day = calen.get(Calendar.DAY_OF_MONTH);

                DatePickerDialog fecha = new DatePickerDialog(requireContext(), new DatePickerDialog.OnDateSetListener() {
                    @Override
                    public void onDateSet(DatePicker view, int year, int monthofYear, int dayOfMonth) {
                        FI.setText(dayOfMonth + "/" + (monthofYear + 1) + "/" + year);
                    }
                }, year, month, day);

                fecha.getDatePicker().setMinDate(System.currentTimeMillis());
                fecha.show();
            }
        });

        FF.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final Calendar calen = Calendar.getInstance();
                int year = calen.get(Calendar.YEAR);
                int month = calen.get(Calendar.MONTH);
                int day = calen.get(Calendar.DAY_OF_MONTH);

                DatePickerDialog fecha = new DatePickerDialog(requireContext(), new DatePickerDialog.OnDateSetListener() {
                    @Override
                    public void onDateSet(DatePicker view, int year, int monthofYear, int dayOfMonth) {
                        FF.setText(dayOfMonth + "/" + (monthofYear + 1) + "/" + year);
                    }
                }, year, month, day);

                fecha.getDatePicker().setMinDate(System.currentTimeMillis());
                fecha.show();
            }
        });

        HI.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final Calendar calen = Calendar.getInstance();
                int hour = calen.get(Calendar.HOUR_OF_DAY);
                int minute = calen.get(Calendar.MINUTE);

                TimePickerDialog hora = new TimePickerDialog(getContext(), new TimePickerDialog.OnTimeSetListener() {
                    @Override
                    public void onTimeSet(TimePicker view, int hourofDay, int minute) {
                        HI.setText(hourofDay + ":" + (minute >= 10 ? minute : "0" + minute));
                    }
                }, hour, minute, true);

                hora.show();
            }
        });
        HF.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final Calendar calen = Calendar.getInstance();
                int hour = calen.get(Calendar.HOUR_OF_DAY);
                int minute = calen.get(Calendar.MINUTE);

                TimePickerDialog hora = new TimePickerDialog(getContext(), new TimePickerDialog.OnTimeSetListener() {
                    @Override
                    public void onTimeSet(TimePicker view, int hourofDay, int minute) {
                        HF.setText(hourofDay + ":" + (minute >= 10 ? minute : "0" + minute));
                    }
                }, hour, minute, true);

                hora.show();
            }
        });
        listaCategorias.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                String seleccionada = (parent.getItemAtPosition(position)).toString();
                try {
                    if(DB == null) {
                        Log.e("Categorías", "Error: La base de datos no está abierta al seleccionar una categoría");
                    } else {
                        String[] args = new String[]{seleccionada};
                        Cursor cursor = DB.rawQuery("SELECT c.ID FROM Categorias c WHERE c.Nombre = ?", args);
                        if(cursor.moveToFirst()) {
                            do {
                                IDcatSel = cursor.getInt(0);
                                nombreCatSel = seleccionada;
                            } while(cursor.moveToNext());
                            cursor.close();
                        }
                    }
                } catch(SQLException ex) {
                    ex.printStackTrace();
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });

        crearCat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                View customLayout = inflater.inflate(R.layout.dialogo_crear_categorias, null);

                //Referencias
                EditText nombreCat = customLayout.findViewById(R.id.nombreCategoria);
                EditText priorCat = customLayout.findViewById(R.id.prioridadCategoria);
                ImageButton colorCat = customLayout.findViewById(R.id.colorCategoria);

                colorCat.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        ColorPickerDialog.Builder builderColor = new ColorPickerDialog.Builder(requireContext());
                        builderColor.setTitle("Seleccionar color");
                        builderColor.setPreferenceName("colorLast");
                        builderColor.setPositiveButton("OK", new ColorEnvelopeListener() {
                            @Override
                            public void onColorSelected(ColorEnvelope envelope, boolean fromUser) {
                                colorSel = "#" + Integer.toHexString(envelope.getColor());

                                colorCat.setImageURI(null);
                                colorCat.setImageBitmap(null);

                                colorCat.setBackgroundColor(envelope.getColor());
                                colorCat.setBackgroundTintList(ColorStateList.valueOf(envelope.getColor()));
                            }
                        });
                        builderColor.setNegativeButton("Cancelar", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                dialog.dismiss();
                            }
                        });
                        builderColor.setBottomSpace(12);
                        builderColor.show();
                    }
                });

                //Construir el diálogo principal
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext(), R.style.elementosGenerales);
                builder.setTitle("Detalles de la categoría");
                builder.setView(customLayout);

                builder.setPositiveButton("ACEPTAR", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        if(!nombreCat.getText().toString().isBlank() && !priorCat.getText().toString().isBlank()) {
                            try {
                                ContentValues nuevaCategoria = new ContentValues();
                                nuevaCategoria.put("nombre", nombreCat.getText().toString());
                                nuevaCategoria.put("prioridad", Integer.valueOf(!priorCat.getText().toString().isBlank() ? priorCat.getText().toString() : "1"));
                                nuevaCategoria.put("color", colorSel);

                                long creada = DB.insert("Categorias", null, nuevaCategoria);
                                if(creada != -1) {
                                    Toast.makeText(getContext(), "Categoría " + nombreCat.getText().toString() + " creada", Toast.LENGTH_SHORT).show();

                                    //Actualizar el listado de categorías
                                    listaCategorias.setAdapter(null);
                                    cargarCategorias();
                                }

                            } catch(SQLException ex) {
                                ex.printStackTrace();
                                Log.e("Categorías", "Error al guardar una nueva categoría", ex);
                                Toast.makeText(getContext(), "Error al guardar una nueva categoría", Toast.LENGTH_SHORT).show();
                            }
                        } else {
                            Toast.makeText(getContext(), "Faltan valores por rellenar (obligatorios el nombre y la prioridad de la categoría)", Toast.LENGTH_LONG).show();
                        }
                    }
                });
                builder.setNegativeButton("CANCELAR", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });

                AlertDialog dialog = builder.create();
                dialog.show();
            }
        });

        return root;
    }

    private void sacarDatosEditar() {
        //Método que carga los datos del evento a editar
        try {
            if(DB == null) {
                Log.e("Error", "BD no conectada para editar un evento");
                return;
            }
            String[] args = new String[]{tituloEditar};
            Cursor miCursor = DB.rawQuery("SELECT t.Icono, t.Fecha_Inicio, t.Plazo_Fecha, t.Hora_Inicio, t.Plazo_Hora, t.Categoria, t.Prioridad, t.Descripcion FROM Tareas t WHERE t.Titulo = ?", args);
            if(miCursor.moveToFirst()) {
                do {
                    byte[] icono = miCursor.getBlob(0);
                    String FIE = miCursor.getString(1);
                    String FFE = miCursor.getString(2);
                    String HIE = miCursor.getString(3);
                    String HFE = miCursor.getString(4);

                    int IdCat = miCursor.getInt(5);
                    String nombreCat = nombreCategoria(IdCat);

                    int prioridadE = miCursor.getInt(6);
                    String descE = miCursor.getString(7);

                    //Transformar algunos datos y ponerlos
                    Drawable icE = ImageUtils.byteArrayToDrawable(getContext(), icono);
                    if(icE != null) ic_Evento.setImageDrawable(icE);

                    FI.setText(FIE);
                    FF.setText(FFE);
                    HI.setText(HIE);
                    HF.setText(HFE);

                    int posCat = getSpinnerPositionByText(listaCategorias, nombreCat);
                    listaCategorias.setSelection(posCat);

                    prioridad.setText(String.valueOf(prioridadE));
                    descEvento.setText(descE);

                } while(miCursor.moveToNext());
                miCursor.close();
            } else {
                Log.e("Error", "Evento no existente");
            }

        } catch(SQLException ex) {
            Log.e("Error", "Error al cargar los datos del evento a editar", ex);
        }
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
            }


        } catch(SQLException ex) {
            Log.e("Turismo", "Error al cargar la información de las categorías", ex);
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 1 && resultCode == RESULT_OK) {
            Uri uri = data.getData();
            ic_Evento.setImageURI(uri);

            ic_Evento.setScaleType(ImageView.ScaleType.FIT_XY);
            ic_Evento.setAdjustViewBounds(true);

            vecesImgSel = true;

        } else if (requestCode == 2 && resultCode == RESULT_OK) {
            handleExportResult(data, "HTML");

        } else if (requestCode == 3 && resultCode == RESULT_OK) {
            handleExportResult(data, "PDF");
        }
    }

    // Método auxiliar para manejar el resultado de la exportación (HTML o PDF)
    private void handleExportResult(Intent data, String fileType) {
        if (data != null && data.getData() != null) {
            Uri fileUri = data.getData(); // Esta es la Uri del archivo que el usuario eligió crear

            OutputStream outputStream = null;
            try {
                outputStream = getContext().getContentResolver().openOutputStream(fileUri);

                if (outputStream != null) {
                    if ("HTML".equals(fileType)) {
                        // --- Escribir el contenido HTML en el flujo de salida ---
                        if (html != null) {
                            byte[] htmlBytes = html.getBytes(StandardCharsets.UTF_8);
                            outputStream.write(htmlBytes);
                            Toast.makeText(getContext(), "Archivo HTML exportado exitosamente.", Toast.LENGTH_LONG).show();
                        } else {
                            Toast.makeText(getContext(), "El contenido HTML a exportar es nulo.", Toast.LENGTH_SHORT).show();
                        }

                    } else if ("PDF".equals(fileType)) {
                        // --- Convertir HTML a PDF usando iText y escribir en el flujo ---
                        if (html != null) {
                            PdfWriter writer = new PdfWriter(outputStream);
                            PdfDocument pdfDocument = new PdfDocument(writer);
                            Document document = new Document(pdfDocument); // iText Document class

                            // Usar HtmlConverter para convertir la cadena HTML a PDF
                            HtmlConverter.convertToPdf(html, pdfDocument.getWriter()); // Convertir directamente a PdfDocument

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
        inflater.inflate(R.menu.planificacion, menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("d/M/yyyy");
        DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("H:mm");

        LocalDate fechaI = LocalDate.of(2000, 1, 1);
        LocalDate fechaIN = LocalDate.of(2000, 1, 1);

        LocalDate fechaF = LocalDate.of(2000, 1, 1);
        LocalDate fechaFN = LocalDate.of(2000, 1, 1);

        LocalTime horaI = LocalTime.of(0, 0);
        LocalTime horaIN = LocalTime.of(0, 0);

        LocalTime horaF = LocalTime.of(0, 0);
        LocalTime horaFN = LocalTime.of(0, 0);

        boolean FIQ = false;
        boolean FFQ = false;
        boolean HIQ = false;
        boolean HFQ = false;

        try {
            if (!titulo.getText().toString().isBlank() && !FF.getText().toString().isBlank()
                    && !prioridad.getText().toString().isBlank() && IDcatSel > 0) {

                if(!FI.getText().toString().isEmpty()) fechaI = LocalDate.parse(FI.getText().toString(), formatter);
                if(!FF.getText().toString().isEmpty()) fechaF = LocalDate.parse(FF.getText().toString(), formatter);

                if(!HI.getText().toString().isEmpty()) horaI = LocalTime.parse(HI.getText().toString(), timeFormatter);
                if(!HF.getText().toString().isEmpty()) horaF = LocalTime.parse(HF.getText().toString(), timeFormatter);

                if(!fechaI.isEqual(fechaIN)) FIQ = true;
                if(!fechaF.isEqual(fechaFN)) FFQ = true;
                if(!horaI.equals(horaIN)) HIQ = true;
                if(!horaF.equals(horaFN)) HFQ = true;
            }

            if(id == R.id.action_guardar) {
                byte[] imageBlob = ImageUtils.getImageButtonAsByteArray(ic_Evento);
                if (!vecesImgSel && !editarEvento) {
                    imageBlob = null;
                }

                if (!titulo.getText().toString().isBlank() && !FF.getText().toString().isBlank()
                        && !prioridad.getText().toString().isBlank() && IDcatSel > 0) {

                    assert fechaI != null : "Nulo";
                    if (fechaI.isAfter(fechaF)) {
                        AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                        builder.setTitle("Aviso");
                        builder.setMessage("La fecha de inicio no puede ser más lejana que la fecha de finalización del evento.");
                        builder.setIcon(R.drawable.informacion);

                        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                dialog.dismiss();
                            }
                        });

                        AlertDialog dialog = builder.create();
                        dialog.show();

                        return false;

                    } else if (fechaI.isEqual(fechaF)) {
                        assert horaI != null : "Nulo";
                        assert horaF != null : "Nulo";

                        if (horaI.isAfter(horaF)) {
                            AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                            builder.setTitle("Aviso");
                            builder.setMessage("La hora de inicio no puede ser más lejana que la hora de finalización del evento.");
                            builder.setIcon(R.drawable.informacion);

                            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    dialog.dismiss();
                                }
                            });

                            AlertDialog dialog = builder.create();
                            dialog.show();

                            return false;
                        }
                    }
                    try {
                        ContentValues nuevoEvento = new ContentValues();
                        nuevoEvento.put("titulo", titulo.getText().toString());
                        nuevoEvento.put("icono", imageBlob);
                        nuevoEvento.put("descripcion", descEvento.getText().toString());
                        nuevoEvento.put("fecha_inicio", FIQ ? FI.getText().toString() : "");
                        nuevoEvento.put("plazo_fecha", FFQ ? FF.getText().toString() : "");
                        nuevoEvento.put("hora_inicio", HIQ ? HI.getText().toString() : "");
                        nuevoEvento.put("plazo_hora", HFQ ? HF.getText().toString() : "");
                        nuevoEvento.put("prioridad", Integer.valueOf(prioridad.getText().toString()));
                        nuevoEvento.put("categoria", IDcatSel);

                        if(!editarEvento) {
                            long registrado = DB.insert("Tareas", null, nuevoEvento);
                            if(registrado != -1) {
                                Toast.makeText(getContext(), "Evento programado para el " + FF.getText().toString(), Toast.LENGTH_LONG).show();
                            } else {
                                Toast.makeText(getContext(), "Evento modificado para el " + FF.getText().toString(), Toast.LENGTH_LONG).show();
                            }
                        } else {
                            int modificado = DB.update("Tareas", nuevoEvento, "Titulo = '" + tituloEditar + "'", null);
                            if(modificado > 0) {
                                Toast.makeText(getContext(), "Evento modificado para el " + FF.getText().toString(), Toast.LENGTH_LONG).show();
                            } else {
                                Toast.makeText(getContext(), "Error al modificar el evento", Toast.LENGTH_LONG).show();
                            }
                        }

                    } catch (SQLException ex) {
                        ex.printStackTrace();
                        Toast.makeText(getContext(), "Error al programar el evento", Toast.LENGTH_SHORT).show();
                    }
                } else {
                    AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                    builder.setTitle("Aviso");
                    builder.setMessage("Faltan valores por rellenar.");
                    builder.setIcon(R.drawable.informacion);

                    builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            dialog.dismiss();
                        }
                    });

                    AlertDialog dialog = builder.create();
                    dialog.show();
                }
            } else if (id == R.id.action_ayudaT) {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Ayuda");
                builder.setMessage("Valores obligatorios: Título, Fecha de Finalización, Categoría y Prioridad del evento.\n\nOtras funciones: Puedes exportar a HTML o PDF una tarjeta con los datos del evento programado.");
                builder.setIcon(R.drawable.ic_ayuda);

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

                AlertDialog dialog = builder.create();
                dialog.show();

            } else if (id == R.id.action_exportar_html) {
                String icBlob = "data:image/png;base64," +  ImageUtils.imageButtonToBase64(ic_Evento);
                if (!vecesImgSel) {
                    icBlob = null;
                }

                if (!titulo.getText().toString().isBlank() && !FF.getText().toString().isBlank()
                        && !prioridad.getText().toString().isBlank() && IDcatSel > 0) {

                    html = "<html>" +
                            "<head>" +
                            "<style>" +
                            "*{font-family:Aptos}" +
                            "h2{margin-left:32px;margin-bottom:25px;font-size:20px;}" +
                            "label{margin-right: 2px;font-size:14px;}" +
                            "h3{font-size:17px}" +
                            "data{font-size:14px;}" +
                            "textarea{font-size:14px;font-family:Aptos}" +
                            "img{width:50px;height:50px;object-fit:contain;}" +
                            "</style>" +
                            "</head>" +
                            "<body>" +
                            "<img src=\"" + icBlob + "\"/>" +
                            "<h2>" + titulo.getText().toString() + "</h2>" +
                            "<label>Fecha de Inicio:  </label>" +
                            "<data>" + FI.getText().toString() + "</data><br/>" +
                            "<label>Fecha de Finalización:  </label>" +
                            "<data>" + FF.getText().toString() + "</data><br/><br/>" +
                            "<label>Hora de Inicio:  </label>" +
                            "<data>" + HI.getText().toString() + "</data><br/>" +
                            "<label>Hora de Finalización:  </label>" +
                            "<data>" + HF.getText().toString() + "</data><br/><br/>" +
                            "<label>Categoría:  </label>" +
                            "<data>" + nombreCatSel + "</data><br/>" +
                            "<label>Prioridad:  </label>" +
                            "<data>" + Integer.valueOf(prioridad.getText().toString()) + "</data><br/><br/>" +
                            "<h3>DESCRIPCIÓN</h3>" +
                            "<textarea cols=\"100\" rows=\"28\" readonly=\"\">" + descEvento.getText().toString() + "</textarea></body></html>";

                    assert fechaI != null : "Nulo";
                    if (fechaI.isAfter(fechaF)) {
                        AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                        builder.setTitle("Aviso");
                        builder.setMessage("La hora de inicio no puede ser más lejana que la hora de finalización del evento.");
                        builder.setIcon(R.drawable.informacion);

                        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                dialog.dismiss();
                            }
                        });

                        AlertDialog dialog = builder.create();
                        dialog.show();

                        return false;

                    } else if (fechaI.isEqual(fechaF)) {
                        assert horaI != null : "Nulo";
                        assert horaF != null : "Nulo";

                        if (horaI.isAfter(horaF)) {
                            AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                            builder.setTitle("Aviso");
                            builder.setMessage("La hora de inicio no puede ser más lejana que la hora de finalización del evento.");
                            builder.setIcon(R.drawable.informacion);

                            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    dialog.dismiss();
                                }
                            });

                            AlertDialog dialog = builder.create();
                            dialog.show();

                            return false;
                        }
                    }
                    String nombreArchivo = titulo.getText().toString() + ".html";

                    Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                    intent.setType("text/html");
                    intent.putExtra(Intent.EXTRA_TITLE, nombreArchivo);

                    try {
                        startActivityForResult(intent, 2);
                    } catch(Exception e) {
                        Toast.makeText(getContext(), "No se pudo abrir el diálogo de exportación a HTML: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                } else {
                    AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                    builder.setTitle("Aviso");
                    builder.setMessage("Faltan valores por rellenar.");
                    builder.setIcon(R.drawable.informacion);

                    builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            dialog.dismiss();
                        }
                    });

                    AlertDialog dialog = builder.create();
                    dialog.show();
                }
            } else if(id == R.id.action_exportar_pdf) {
                String icBlob = "data:image/png;base64," +  ImageUtils.imageButtonToBase64(ic_Evento);
                if (!vecesImgSel) {
                    icBlob = null;
                }

                if (!titulo.getText().toString().isBlank() && !FF.getText().toString().isBlank()
                        && !prioridad.getText().toString().isBlank() && IDcatSel > 0) {

                    html = "<html>" +
                            "<head>" +
                            "<style>" +
                            "*{font-family:Aptos}" +
                            "h2{margin-left:32px;margin-bottom:25px;font-size:20px;}" +
                            "label{margin-right: 2px;font-size:14px;}" +
                            "h3{font-size:17px}" +
                            "data{font-size:14px;}" +
                            "textarea{font-size:14px;font-family:Aptos}" +
                            "img{width:50px;height:50px;object-fit:contain;}" +
                            "</style>" +
                            "</head>" +
                            "<body>" +
                            "<img src=\"" + icBlob + "\"/>" +
                            "<h2>" + titulo.getText().toString() + "</h2>" +
                            "<label>Fecha de Inicio:  </label>" +
                            "<data>" + FI.getText().toString() + "</data><br/>" +
                            "<label>Fecha de Finalización:  </label>" +
                            "<data>" + FF.getText().toString() + "</data><br/><br/>" +
                            "<label>Hora de Inicio:  </label>" +
                            "<data>" + HI.getText().toString() + "</data><br/>" +
                            "<label>Hora de Finalización:  </label>" +
                            "<data>" + HF.getText().toString() + "</data><br/><br/>" +
                            "<label>Categoría:  </label>" +
                            "<data>" + nombreCatSel + "</data><br/>" +
                            "<label>Prioridad:  </label>" +
                            "<data>" + Integer.valueOf(prioridad.getText().toString()) + "</data><br/><br/>" +
                            "<h3>DESCRIPCIÓN</h3>" +
                            "<textarea cols=\"100\" rows=\"28\" readonly=\"\">" + descEvento.getText().toString() + "</textarea></body></html>";

                    assert fechaI != null : "Nulo";
                    if (fechaI.isAfter(fechaF)) {
                        AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                        builder.setTitle("Aviso");
                        builder.setMessage("La hora de inicio no puede ser más lejana que la hora de finalización del evento.");
                        builder.setIcon(R.drawable.informacion);

                        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                dialog.dismiss();
                            }
                        });

                        AlertDialog dialog = builder.create();
                        dialog.show();

                        return false;

                    }  else if (fechaI.isEqual(fechaF)) {
                        assert horaI != null : "Nulo";
                        assert horaF != null : "Nulo";

                        if (horaI.isAfter(horaF)) {
                            AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                            builder.setTitle("Aviso");
                            builder.setMessage("La hora de inicio no puede ser más lejana que la hora de finalización del evento.");
                            builder.setIcon(R.drawable.informacion);

                            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    dialog.dismiss();
                                }
                            });

                            AlertDialog dialog = builder.create();
                            dialog.show();

                            return false;
                        }
                    }
                    String nombreArchivo = titulo.getText().toString() + ".pdf";

                    Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                    intent.setType("application/pdf");
                    intent.putExtra(Intent.EXTRA_TITLE, nombreArchivo);

                    try {
                        startActivityForResult(intent, 3);
                    } catch(Exception e) {
                        Toast.makeText(getContext(), "No se pudo abrir el diálogo de exportación a PDF: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                } else {
                    AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                    builder.setTitle("Aviso");
                    builder.setMessage("Faltan valores por rellenar.");
                    builder.setIcon(R.drawable.informacion);

                    builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            dialog.dismiss();
                        }
                    });

                    AlertDialog dialog = builder.create();
                    dialog.show();
                }
            }
        } catch (Exception e) {
            Log.e("Error", "Error", e);
        }
        return super.onOptionsItemSelected(item);
    }
}
