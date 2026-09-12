package com.tfg.myapplication.ui.categorias;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ContentValues;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.res.ColorStateList;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Color;
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
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.itextpdf.html2pdf.HtmlConverter;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.skydoves.colorpickerview.ColorEnvelope;
import com.skydoves.colorpickerview.ColorPickerDialog;
import com.skydoves.colorpickerview.listeners.ColorEnvelopeListener;
import com.tfg.myapplication.GestorBD;
import com.tfg.myapplication.R;
import com.tfg.myapplication.databinding.FragmentCategoriasBinding;
import com.tfg.myapplication.modelos.*;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class CategoriasFragment extends Fragment {
    private FragmentCategoriasBinding binding;

    //Elementos de la UI
    private Spinner listaCategorias;
    private TextView label;
    private RecyclerView listadoCategorias;

    //BD
    private GestorBD gestorBD;
    private SQLiteDatabase DB;

    //Variables auxiliares
    private CategoriaAdapter categoriaAdapter;
    private List<Categoria> listaDeCategorias;
    String colorSel;

    String colorCatSel;
    int priorCatSel;
    String nameCatSel;
    int IDcatSel;

    //Plantillas (HTML y PDF)
    String plantillaHTML = "<!DOCTYPE html><html><head><style>#contenedor{display: flex;align-items: center;}div{margin-bottom: 20px;}#color{width: 40px;height: 40px;border:5px solid black;margin-right: 10px;min-width: 40px;}#prioridad{font-family: 'Segoe UI';font-size: 27px;font-style: normal;position:relative;top: -10px;margin-right: 10px;}#nombre{font-family: 'Segoe UI';font-size: 22px;font-style: normal;vertical-align: center;position: relative;top: -10px;flex-grow: 1}</style></head><body>";
    String plantillaPDF = "<!DOCTYPE html><html><head><style>#contenedor{display: flex;align-items: center;}div{margin-bottom: 20px;}#color{width: 40px;height: 40px;border:5px solid black;margin-right: 10px;min-width: 40px;}#prioridad{font-family: 'Segoe UI';font-size: 27px;font-style: normal;position:relative;top: -10px;margin-right: 10px;}#nombre{font-family: 'Segoe UI';font-size: 22px;font-style: normal;vertical-align: center;position: relative;top: -10px;flex-grow: 1}</style></head><body>";

    String infoHTML = "";
    String infoPDF = "";
    String finalPL = "</body></html>";

    //Documentos finales
    String HTML, PDF;

    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {

        // Inflar el layout para este fragmento
        binding = FragmentCategoriasBinding.inflate(inflater, container, false);
        View root = binding.getRoot();
        setHasOptionsMenu(true);

        //Obtener elementos vía binding
        listaCategorias = binding.ListaCategorias;
        label = binding.textViewCategoriasTitle;
        listadoCategorias = binding.recyclerViewCategoriesList;

        //Configurar el LayoutManager para el RecyclerView
        listadoCategorias.setLayoutManager(new LinearLayoutManager(getContext()));

        //Inicializar variables auxiliares
        listaDeCategorias = new ArrayList<>();
        categoriaAdapter = new CategoriaAdapter(listaDeCategorias);
        listadoCategorias.setAdapter(categoriaAdapter);

        //Obtener referencia a la BD
        gestorBD = new GestorBD(getContext());
        try {
            DB = gestorBD.openDataBase();
            Log.i("Turismo", "Conexión a la BD correcta");
        } catch(Exception e) {
            Log.e("Turismo", "Error al conectar a la BD", e);
        }

        //Configuraciones iniciales
        cargarCategorias();
        cargarListadoCategorias();

        //Acciones
        listaCategorias.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                IDcatSel = 0;
                nameCatSel = "";

                String seleccionada = (parent.getItemAtPosition(position)).toString();
                try {
                    if(DB == null) {
                        Log.e("Categorías", "Error: La base de datos no está abierta al seleccionar una categoría");
                    } else {
                        String[] args = new String[]{seleccionada};
                        Cursor cursor = DB.rawQuery("SELECT c.ID, c.Prioridad, c.Color FROM Categorias c WHERE c.Nombre = ?", args);
                        if(cursor.moveToFirst()) {
                            do {
                                IDcatSel = cursor.getInt(0);
                                nameCatSel = seleccionada;

                                priorCatSel = cursor.getInt(1);
                                colorCatSel = cursor.getString(2);

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

        return root;
    }

    private void cargarListadoCategorias() {
        //Método que carga el listado de categorías ordenadas por prioridad
        listaDeCategorias = new ArrayList<>();
        try {
            if(DB == null) {
                Log.e("Error", "Error: Se intentó cargar el listado de categorías ordenadas por prioridad cuando la BD no estaba conectada");
                categoriaAdapter.setCategorias(listaDeCategorias);
                return;
            }
            Cursor miCursor = DB.rawQuery("SELECT c.Nombre, c.Prioridad, c.Color FROM Categorias c", null);
            if(miCursor.moveToFirst()) {
                do {
                    String nombre = miCursor.getString(0);
                    int prioridad = miCursor.getInt(1);
                    String color = miCursor.getString(2);

                    //Ir creando los elementos de las categorías para el listado
                    listaDeCategorias.add(new Categoria(color, prioridad, nombre));

                    //Preparar las plantillas con toda la información a exportar
                    infoHTML += "<div id=\"contenedor\"><div id=\"color\" style=\"background-color:" + ("#" + (color != null && color.length() > 3 ? color.substring(3) : "")) + "\"></div><label id=\"prioridad\"><strong>" + prioridad + "&deg)&nbsp;&nbsp;&nbsp;</strong></label><label id=\"nombre\">" + nombre + "</label></div>";
                    infoPDF += "<div id=\"contenedor\"><div id=\"color\" style=\"background-color:" + ("#" + (color != null && color.length() > 3 ? color.substring(3) : "")) + "\"></div><label id=\"prioridad\"><strong>" + prioridad + "&deg)&nbsp;&nbsp;&nbsp;</strong></label><label id=\"nombre\">" + nombre + "</label></div><br/>";

                } while(miCursor.moveToNext());
                miCursor.close();

            } else {
                label.setText("NO HAY CATEGORÍAS CREADAS");
            }

        } catch(SQLException ex) {
            Log.e("Error", "Error al cargar el listado de categorías ordenadas por prioridad ", ex);
        } catch (IllegalArgumentException ex) {
            Log.e("Error", "Error al obtener columna de cursor", ex);
            Toast.makeText(getContext(), "Error al procesar datos de categorías.", Toast.LENGTH_SHORT).show();
        } finally {
            categoriaAdapter.setCategorias(listaDeCategorias);
        }
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
                label.setText("NO HAY CATEGORÍAS CREADAS");
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

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    @Override
    public void onCreateOptionsMenu(@NonNull Menu menu, @NonNull MenuInflater inflater) {
        super.onCreateOptionsMenu(menu, inflater);
        inflater.inflate(R.menu.acciones_categorias, menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if(id == R.id.menu_editar) {
            //Comprobar que se haya seleccionado una categoría
            int posCatSel = getSpinnerPositionByText(listaCategorias, nameCatSel);
            if(posCatSel > 0) {
                //Construir diálogo de edición de los datos de una categoría
                AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
                builder.setTitle("Editar categoría");
                builder.setIcon(R.drawable.ic_editar);

                LayoutInflater inflater = LayoutInflater.from(getContext());
                View customLayout = inflater.inflate(R.layout.dialogo_crear_categorias, null);
                builder.setView(customLayout);

                //Referencias
                EditText nombreCat = customLayout.findViewById(R.id.nombreCategoria);
                nombreCat.setText(nameCatSel);

                EditText priorCat = customLayout.findViewById(R.id.prioridadCategoria);
                priorCat.setText(String.valueOf(priorCatSel));

                ImageButton colorCat = customLayout.findViewById(R.id.colorCategoria);
                try {
                    if(colorCatSel != null && !colorCatSel.isEmpty()) {
                        colorCat.setBackgroundColor(Color.parseColor(colorCatSel));
                        colorCat.setImageURI(null);
                        colorCat.setImageBitmap(null);
                    }
                } catch(Exception ex) {
                    Log.e("Error", "Error al cargar color de la categoría", ex);
                }

                //Acciones
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

                builder.setPositiveButton("GUARDAR", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        //Actualizar los datos de la categoría editada
                        try {
                            if(DB == null || !DB.isOpen()) {
                                Log.e("Categorías", "Error: La base de datos no está abierta al editar una categoría");
                                return;
                            }
                            if(!nombreCat.getText().toString().isBlank() && !priorCat.getText().toString().isBlank()) {
                                ContentValues nuevosValores = new ContentValues();
                                nuevosValores.put("nombre", nombreCat.getText().toString());
                                nuevosValores.put("prioridad", Integer.valueOf(priorCat.getText().toString()));
                                nuevosValores.put("color", colorSel != null && !colorSel.isEmpty() ? colorSel : colorCatSel);

                                int actualizado = DB.update("Categorias", nuevosValores, "ID = " + IDcatSel, null);
                                if(actualizado == 1) {
                                    Toast.makeText(getContext(), "Categoría " + nameCatSel + " modificada", Toast.LENGTH_LONG).show();
                                    listaCategorias.setAdapter(null);

                                    infoHTML = "";
                                    infoPDF = "";

                                    cargarCategorias();
                                    cargarListadoCategorias();

                                    colorSel = "";
                                    nombreCat.setText("");
                                    priorCat.setText("");
                                    nameCatSel = "";
                                    IDcatSel = 0;

                                } else if(actualizado > 1) {
                                    Log.e("Error", "Se han modificado más categorías de las que se debería");
                                    cargarCategorias();
                                    cargarListadoCategorias();
                                } else {
                                    Toast.makeText(getContext(), "Error al modificar la categoría  " + nameCatSel, Toast.LENGTH_LONG).show();
                                }
                            } else {
                                Toast.makeText(getContext(), "Faltan valores por rellenar (obligatorios el nombre y la prioridad de la categoría)", Toast.LENGTH_LONG).show();
                            }

                        } catch(SQLException ex) {
                            Log.e("Error", "Error al modificar los datos de una categoría", ex);
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
            } else if(!listaDeCategorias.isEmpty()) {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Aviso");
                builder.setIcon(R.drawable.informacion);
                builder.setMessage("No se ha seleccionado ninguna categoría");

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

                AlertDialog dialog = builder.create();
                dialog.show();
            } else {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Aviso");
                builder.setIcon(R.drawable.informacion);
                builder.setMessage("No hay categorías creadas");

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

                AlertDialog dialog = builder.create();
                dialog.show();
            }

        } else if(id == R.id.menu_eliminar) {
            //Comprobar que se haya seleccionado una categoría
            int posCatSel = getSpinnerPositionByText(listaCategorias, nameCatSel);
            if(posCatSel > 0) {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Aviso");
                builder.setIcon(R.drawable.informacion);
                builder.setMessage("¿Está seguro de que desea eliminar la categoría " + nameCatSel + "?");

                builder.setPositiveButton("SÍ", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        try {
                            int eliminada = DB.delete("Categorias", "ID = " + IDcatSel, null);
                            if(eliminada == 1) {
                                Toast.makeText(getContext(), "Categoría " + nameCatSel + " eliminada", Toast.LENGTH_SHORT).show();
                                int IDCatEliminada = IDcatSel;
                                listaCategorias.setAdapter(null);

                                int eventosEliminados = DB.delete("Tareas", "Categoria = " + IDCatEliminada, null);
                                if(eventosEliminados > 0) {
                                    Toast.makeText(getContext(), "Eventos de la categoría " + nameCatSel + " eliminados", Toast.LENGTH_LONG).show();
                                    Log.i("Eliminación de categoría", "Eventos de la categoría " + nameCatSel + " eliminados");

                                } else {
                                    Log.i("Eliminación de categoría", "La categoría " + nameCatSel + " no tenía eventos asociados");
                                }

                                colorSel = "";
                                nameCatSel = "";
                                IDcatSel = 0;

                                infoHTML = "";
                                infoPDF = "";

                                cargarCategorias();
                                cargarListadoCategorias();

                            } else if(eliminada > 1) {
                                Log.e("Error", "Se han eliminado más categorías de las que se debería");
                                infoHTML = "";
                                infoPDF = "";

                                cargarCategorias();
                                cargarListadoCategorias();
                            }

                        } catch(SQLException ex) {
                            Log.e("Error", "Error al eliminar la categoría " + nameCatSel, ex);
                        }
                    }
                });
                builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });

                AlertDialog dialog = builder.create();
                dialog.show();
            } else if(!listaDeCategorias.isEmpty()) {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Aviso");
                builder.setIcon(R.drawable.informacion);
                builder.setMessage("No se ha seleccionado ninguna categoría");

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

                AlertDialog dialog = builder.create();
                dialog.show();
            } else {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Aviso");
                builder.setIcon(R.drawable.informacion);
                builder.setMessage("No hay categorías creadas");

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

                AlertDialog dialog = builder.create();
                dialog.show();
            }

        } else if(id == R.id.action_exportar_html) {
            HTML = plantillaHTML + infoHTML + finalPL;

            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("text/html");
            intent.putExtra(Intent.EXTRA_TITLE, "ListadoCategorias.html");

            try {
                startActivityForResult(intent, 2);
            } catch(Exception e) {
                Toast.makeText(getContext(), "No se pudo abrir el diálogo de guardado: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }

        } else if(id == R.id.action_exportar_pdf) {
            PDF = plantillaPDF + infoPDF + finalPL;

            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("application/pdf");
            intent.putExtra(Intent.EXTRA_TITLE, "ListaCategorias.pdf");

            try {
                startActivityForResult(intent, 3);
            } catch(Exception e) {
                Toast.makeText(getContext(), "No se pudo abrir el diálogo de guardado: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }

        } else if(id == R.id.action_ayudaCE) {
            AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
            builder.setTitle("Ayuda");
            builder.setIcon(R.drawable.ic_ayuda);
            builder.setMessage("Para editar o eliminar una categoría seleccione una del desplegable primero (el que está al lado del texto de \"Categoría\")");

            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                }
            });

            AlertDialog dialog = builder.create();
            dialog.show();
        }

        return super.onOptionsItemSelected(item);
    }
}
