package com.tfg.myapplication.ui.sitios;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;

import android.database.*;
import android.database.sqlite.*;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.*;

import com.itextpdf.layout.Document;
import com.tfg.myapplication.GestorBD;
import com.tfg.myapplication.R;
import com.tfg.myapplication.databinding.FragmentSitiosBinding;

import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.html2pdf.HtmlConverter;

import java.io.*;
import java.nio.charset.StandardCharsets;

public class SitiosFragment extends Fragment {
    private FragmentSitiosBinding binding;

    //Elementos de la UI
    private Spinner ciudadesSpinner;
    private Spinner sitiosSpinner;
    private ImageView ciudad_ImgView;
    private ImageView sitio_ImgView;
    private TextView desc_CiudadSitio;
    private TextView ciudadLabel;
    private TextView sitioLabel;

    //BD
    private GestorBD gestorBD;
    private SQLiteDatabase DB;

    //Variables auxiliares
    private String nombreC;
    private String descC;

    private String nombreS;
    private String descS;

    int actionMenu;

    //Plantillas
    String html;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        SitiosViewModel sitiosViewModel =
                new ViewModelProvider(this).get(SitiosViewModel.class);
        setHasOptionsMenu(true);

        binding = FragmentSitiosBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        //Obtener referencias a los objetos de la UI
        ciudadesSpinner = binding.ListaCiudades;
        sitiosSpinner = binding.ListaSitios;
        ciudad_ImgView = binding.imgCiudad;
        sitio_ImgView = binding.imgSitio;
        desc_CiudadSitio = binding.descCiudadYsitio;
        ciudadLabel = binding.ciudad;
        sitioLabel = binding.sitio;

        //Obtener referencia a la BD
        gestorBD = new GestorBD(getContext());
        try {
            DB = gestorBD.openDataBase();
            Log.i("Turismo", "Conexión a la BD correcta");
        } catch(Exception e) {
            Log.e("Turismo", "Error al conectar a la BD", e);
        }

        //Configuraciones importantes
        cargarCiudades();

        //Acciones
        ciudadesSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                String seleccionado = (parent.getItemAtPosition(position)).toString();
                Log.i("Ciudad", seleccionado);

                if(position > 0) {
                    ciudad_ImgView.setVisibility(View.VISIBLE);
                    ciudadLabel.setVisibility(View.VISIBLE);
                    desc_CiudadSitio.setVisibility(View.VISIBLE);

                    cargarInfoCiudad(seleccionado);
                    cargarSitios(seleccionado);
                } else {
                    ciudad_ImgView.setVisibility(View.INVISIBLE);
                    ciudadLabel.setVisibility(View.INVISIBLE);

                    sitio_ImgView.setVisibility(View.INVISIBLE);
                    sitioLabel.setVisibility(View.INVISIBLE);
                    desc_CiudadSitio.setVisibility(View.INVISIBLE);

                    sitiosSpinner.setAdapter(null);
                    descC = "";
                    descS = "";

                    desc_CiudadSitio.setText("");
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });

        sitiosSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                String seleccionado = (parent.getItemAtPosition(position)).toString();
                Log.i("Sitio", seleccionado);

                if(position > 0) {
                    sitioLabel.setVisibility(View.VISIBLE);
                    sitio_ImgView.setVisibility(View.VISIBLE);

                    cargarInfoSitio(seleccionado);
                    desc_CiudadSitio.setText(nombreC + ": " + descC + "\n\n\n" + nombreS + ": " + descS);
                } else {
                    sitio_ImgView.setVisibility(View.INVISIBLE);
                    sitioLabel.setVisibility(View.INVISIBLE);
                    descS = "";

                    desc_CiudadSitio.setText(descC);
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });

        return root;
    }

    private void cargarInfoCiudad(String ciudad) {
        //Método que carga la información de la ciudad seleccionada
        try {
            if(DB == null) {
                Log.e("Turismo", "Error: La base de datos no está abierta al cargar la información de la ciudad " + ciudad);
                return;
            }
            nombreC = ciudad;

            String[] args = new String[]{ciudad};
            Cursor cursor = DB.rawQuery("SELECT c.Imagen, c.Descripcion FROM Ciudades c WHERE c.Nombre = ?", args);
            if(cursor.moveToFirst()) {
                do {
                    byte[] datosBlob = cursor.getBlob(0);
                    descC = cursor.getString(1);

                    if(datosBlob != null) {
                        Bitmap bitmap = BitmapFactory.decodeByteArray(datosBlob, 0, datosBlob.length);
                        ciudad_ImgView.setImageBitmap(bitmap);
                        ciudad_ImgView.setScaleType(ImageView.ScaleType.FIT_XY);
                        ciudadLabel.setText(ciudad);
                        desc_CiudadSitio.setText(descC);
                    } else {
                        ciudad_ImgView.setImageBitmap(null);
                        ciudadLabel.setText(ciudad);
                    }

                } while(cursor.moveToNext());
            }
            cursor.close();

        } catch(SQLException e) {
            Log.e("Turismo", "Error al cargar la información de la ciudad " + ciudad, e);
        }
    }

    private void cargarInfoSitio(String sitio) {
        //Método que carga la información del sitio seleccionado
        try {
            if(DB == null) {
                Log.e("Turismo", "Error: La base de datos no está abierta al cargar la información del sitio " + sitio);
                return;
            }
            nombreS = sitio;

            String[] args = new String[]{sitio};
            Cursor cursor = DB.rawQuery("SELECT s.Imagen, s.Descripcion FROM Sitios s WHERE s.Nombre = ?", args);
            if(cursor.moveToFirst()) {
                do {
                    byte[] datosBlob = cursor.getBlob(0);
                    descS = cursor.getString(1);

                    if(datosBlob != null) {
                        Bitmap bitmap = BitmapFactory.decodeByteArray(datosBlob, 0, datosBlob.length);
                        sitio_ImgView.setImageBitmap(bitmap);
                        sitio_ImgView.setScaleType(ImageView.ScaleType.FIT_XY);
                        sitioLabel.setText(sitio);

                    } else {
                        sitio_ImgView.setImageBitmap(null);
                        sitioLabel.setText(sitio);
                    }
                } while(cursor.moveToNext());
            } else {
                Log.i("Turismo", "Error al leer sitio " + sitio);
            }
            cursor.close();

        } catch(SQLException e) {
            Log.e("Turismo", "Error al cargar la información del sitio " + sitio, e);
        } catch(Exception e) {
            Log.e("Turismo", "Otro error al cargar info del sitio '" + sitio + "':", e);
        }
    }

    private void cargarSitios(String ciudad) {
        //Método que carga el listado de sitios de una ciudad
        try {
            if(DB == null) {
                Log.e("Turismo", "Error: La base de datos no está abierta al cargar sitios de la ciudad " + ciudad);
                sitiosSpinner.setAdapter(null);
                return;
            }

            String[] params = new String[]{ciudad};
            Cursor cursor = DB.rawQuery("SELECT c.ID FROM Ciudades c WHERE c.Nombre = ?", params);
            int cID = 0;

            if(cursor.moveToFirst()) {
                do {
                    cID = cursor.getInt(0);
                } while(cursor.moveToNext());
                cursor.close();
            }

            if(cID > 0) {
                params = new String[]{String.valueOf(cID)};
                Cursor filas = DB.rawQuery("SELECT s.Nombre FROM Sitios s WHERE s.Ciudad = ?", params);

                if(filas.moveToFirst()) {
                    String[] listado = new String[filas.getCount() + 1];
                    int i=1;
                    listado[0] = "Seleccione un sitio";
                    do {
                        String sitio = filas.getString(0);
                        listado[i] = sitio;
                        i++;
                    } while (filas.moveToNext());
                    filas.close();

                    ArrayAdapter<String> adapter = new ArrayAdapter<>(requireContext(), R.layout.custom_spinner_item, listado);
                    adapter.setDropDownViewResource(androidx.appcompat.R.layout.support_simple_spinner_dropdown_item);
                    sitiosSpinner.setAdapter(adapter);

                    //sin seleccionar
                    sitiosSpinner.setSelection(0);
                }
            }

        } catch(SQLException e) {
            Log.e("Turismo", "Error al cargar el listado de sitios de la ciudad " + ciudad, e);
        }
    }

    private void cargarCiudades() {
        //Método que infla el listado de ciudades
        try {
            ciudad_ImgView.setVisibility(View.INVISIBLE);
            ciudadLabel.setVisibility(View.INVISIBLE);

            sitio_ImgView.setVisibility(View.INVISIBLE);
            sitioLabel.setVisibility(View.INVISIBLE);
            desc_CiudadSitio.setVisibility(View.INVISIBLE);

            if(DB == null) {
                Log.e("Turismo", "Error: La base de datos no está abierta al cargar ciudades.");
                ciudadesSpinner.setAdapter(null);
                return; // Salir de la función si la BD no está lista
            }

            Cursor filas = DB.rawQuery("SELECT c.Nombre FROM Ciudades c", null);
            if(filas.moveToFirst()) {
                String[] listado = new String[filas.getCount() + 1];
                int i=1;
                listado[0] = "Seleccione una ciudad";
                do {
                    String ciudad = filas.getString(0);
                    listado[i] = ciudad;
                    i++;
                } while (filas.moveToNext());
                filas.close();

                ArrayAdapter<String> adapter = new ArrayAdapter<>(requireContext(), R.layout.custom_spinner_item, listado);
                adapter.setDropDownViewResource(androidx.appcompat.R.layout.support_simple_spinner_dropdown_item);
                ciudadesSpinner.setAdapter(adapter);

                //sin seleccionar
                ciudadesSpinner.setSelection(0);
            }
        } catch(SQLException e) {
            Log.e("Turismo", "Error al cargar el listado de ciudades", e);
        }
    }

    @Override
    public void onCreateOptionsMenu(@NonNull Menu menu, @NonNull MenuInflater inflater) {
        super.onCreateOptionsMenu(menu, inflater);
        inflater.inflate(R.menu.sitios, menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if(id == R.id.action_exportar_html) {
            if(ciudadLabel.getText().equals("Ciudad") || sitioLabel.getText().equals("Sitio")) {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Aviso");
                builder.setMessage("Ciudad o sitio no seleccionados");
                builder.setIcon(R.drawable.informacion);

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

                AlertDialog dialog = builder.create();
                dialog.show();

            } else {
                actionMenu = id;

                String imagenCiudad = "data:image/png;base64," + imageViewToBase64(ciudad_ImgView);
                String imagenSitio = "data:image/png;base64," + imageViewToBase64(sitio_ImgView);

                html = "<!DOCTYPE html> " + "<html>" + "<head>" + "<title>" + ciudadLabel.getText() + "-" + sitioLabel.getText() + "</title>" + "<style>" + "img{width:241px;height:181px;vertical-align:middle;object-fit:contain;}" + "div{width:241px;text-align:center;}" + "#desc_Ciudad{width:723px;text-align:left;}" + "#desc_Sitio{width:723px;text-align:left;}" + "h3{font-size:20px;}" + "p{font-size:14px;}" + "</style>" + "</head>" + "<body><div id=\"Ciudad\"><img src=\"" + imagenCiudad + "\"/><br/><h3 id=\"nombreCiudad\">" + ciudadLabel.getText() + "</h3><br/></div><div id=\"desc_Ciudad\"><p>" + descC + "</p></div><br/><br/><br/><br/><div id=\"Sitio\">" + "<img src=\"" + imagenSitio + "\"/><br/><h3 id=\"nombreSitio\">" + sitioLabel.getText() + "</h3><br/></div><div id=\"desc_Sitio\"><p>" + descS + "</p></div></body></html>";
                String nombreArchivo = ciudadLabel.getText() + "-" + sitioLabel.getText() + ".html";

                Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("text/html");
                intent.putExtra(Intent.EXTRA_TITLE, nombreArchivo);

                try {
                    startActivityForResult(intent, 2);
                } catch(Exception e) {
                    Toast.makeText(getContext(), "No se pudo abrir el diálogo de guardado: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                }
            }

        } else if(id == R.id.action_exportar_pdf) {
            if(ciudadLabel.getText().equals("Ciudad") || sitioLabel.getText().equals("Sitio")) {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Aviso");
                builder.setMessage("Ciudad o sitio no seleccionados");
                builder.setIcon(R.drawable.informacion);

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

                AlertDialog dialog = builder.create();
                dialog.show();

            } else {
                actionMenu = id;

                String imagenCiudad = "data:image/png;base64," + imageViewToBase64(ciudad_ImgView);
                String imagenSitio = "data:image/png;base64," + imageViewToBase64(sitio_ImgView);

                html = "<!DOCTYPE html> " + "<html>" + "<head>" + "<title>" + ciudadLabel.getText() + "-" + sitioLabel.getText() + "</title>" + "<style>" + "img{width:241px;height:181px;vertical-align:middle;object-fit:contain;}" + "div{width:241px;text-align:center;}" + "#desc_Ciudad{width:723px;text-align:left;}" + "#desc_Sitio{width:723px;text-align:left;}" + "h3{font-size:20px;}" + "p{font-size:14px;}" + "</style>" + "</head>" + "<body><div id=\"Ciudad\"><img src=\"" + imagenCiudad + "\"/><br/><h3 id=\"nombreCiudad\">" + ciudadLabel.getText() + "</h3><br/></div><div id=\"desc_Ciudad\"><p>" + descC + "</p></div><br/><br/><br/><br/><div id=\"Sitio\">" + "<img src=\"" + imagenSitio + "\"/><br/><h3 id=\"nombreSitio\">" + sitioLabel.getText() + "</h3><br/></div><div id=\"desc_Sitio\"><p>" + descS + "</p></div></body></html>";
                String nombreArchivo = ciudadLabel.getText() + "-" + sitioLabel.getText() + ".pdf";

                Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("application/pdf");
                intent.putExtra(Intent.EXTRA_TITLE, nombreArchivo);

                try {
                    startActivityForResult(intent, 3);
                } catch(Exception e) {
                    Toast.makeText(getContext(), "No se pudo abrir el diálogo de guardado: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                }
            }

        } else if(id == R.id.ubiClimaSitio) {
            if(!ciudadLabel.getText().equals("Ciudad")) {
                try {
                    NavController navController = Navigation.findNavController(requireActivity(), R.id.nav_host_fragment_content_main);
                    Bundle bundle = new Bundle();
                    bundle.putString("cityName", (String) ciudadLabel.getText());
                    navController.navigate(R.id.nav_actualidad, bundle);

                } catch(Exception ex) {
                    ex.printStackTrace();
                }
            } else if(ciudadLabel.getText().equals("Ciudad")) {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Aviso");
                builder.setMessage("Ciudad no seleccionada");
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
        } else if(id == R.id.planificarVisita) {
            if(!ciudadLabel.getText().equals("Ciudad")) {
                try {
                    NavController navController = Navigation.findNavController(requireActivity(), R.id.nav_host_fragment_content_main);
                    Bundle bundle = new Bundle();
                    bundle.putString("tituloV", "Visita a " + (!sitioLabel.getText().equals("Sitio") ? sitioLabel.getText() : ciudadLabel.getText()));
                    navController.navigate(R.id.nav_planificar, bundle);

                } catch (Exception e) {
                    e.printStackTrace();
                }

            } else if(ciudadLabel.getText().equals("Ciudad")) {
                AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
                builder.setTitle("Aviso");
                builder.setMessage("Ciudad no seleccionada");
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
        return super.onOptionsItemSelected(item);
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
                            com.itextpdf.kernel.pdf.PdfDocument pdfDocument = new com.itextpdf.kernel.pdf.PdfDocument(writer);
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
    /**
     * Convierte el contenido de un ImageView a una cadena Base64.
     *
     * @param imageView El ImageView que contiene la imagen.
     * @return La cadena Base64 de la imagen, o null si no hay imagen o hay un error.
     */
    public static String imageViewToBase64(ImageView imageView) {
        if (imageView == null) {
            return null;
        }

        // 1. Obtener el Drawable del ImageView
        Drawable drawable = imageView.getDrawable();

        if (drawable == null) {
            // No hay imagen en el ImageView
            return null;
        }

        // 2. Convertir el Drawable a un Bitmap
        Bitmap bitmap = null;
        if (drawable instanceof BitmapDrawable) {
            // Si ya es un BitmapDrawable, obtener el Bitmap directamente
            bitmap = ((BitmapDrawable) drawable).getBitmap();
        } else {
            // Si es otro tipo de Drawable (ej: ColorDrawable, VectorDrawable),
            // dibujar el Drawable en un nuevo Bitmap
            try {
                bitmap = Bitmap.createBitmap(
                        drawable.getIntrinsicWidth(),
                        drawable.getIntrinsicHeight(),
                        Bitmap.Config.ARGB_8888 // O RGB_565 si no necesito transparencia
                );
                Canvas canvas = new Canvas(bitmap);
                drawable.setBounds(0, 0, canvas.getWidth(), canvas.getHeight());
                drawable.draw(canvas);
            } catch (IllegalArgumentException e) {
                // Esto puede ocurrir si el drawable no tiene dimensiones intrínsecas (ej: 0x0)
                e.printStackTrace();
                return null;
            }
        }

        if (bitmap == null) {
            // No se pudo obtener o crear el Bitmap
            return null;
        }

        // 3. Comprimir el Bitmap a un array de bytes
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        // Puedo elegir el formato (PNG, JPEG) y la calidad (para JPEG)
        // PNG es sin pérdida, JPEG permite ajustar la calidad (0-100)
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream);
        byte[] byteArray = byteArrayOutputStream.toByteArray();

        // Cerrar el flujo (aunque ByteArrayOutputStream no necesita ser cerrado explícitamente en la mayoría de los casos)
        try {
            byteArrayOutputStream.close();
        } catch (java.io.IOException e) {
            e.printStackTrace();
            // Continuar, el array de bytes ya se obtuvo
        }


        // 4. Codificar el array de bytes a una cadena Base64
        // Usa Base64.NO_WRAP para evitar saltos de línea en la cadena Base64
        String base64String = Base64.encodeToString(byteArray, Base64.NO_WRAP);

        return base64String;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;

        if(gestorBD != null) {
            gestorBD.close();
        }
    }
}
