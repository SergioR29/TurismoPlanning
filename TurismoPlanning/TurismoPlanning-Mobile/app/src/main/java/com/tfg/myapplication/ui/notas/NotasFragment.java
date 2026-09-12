package com.tfg.myapplication.ui.notas;

import static android.app.Activity.RESULT_OK;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.OpenableColumns; // Importar OpenableColumns
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable; // Importar Nullable
import androidx.fragment.app.*;

import com.itextpdf.html2pdf.HtmlConverter;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.tfg.myapplication.R;
import com.tfg.myapplication.databinding.FragmentNotasBinding;

import java.io.*;

public class NotasFragment extends Fragment {
    private FragmentNotasBinding binding;

    //Elementos de la UI
    private EditText nota;

    // Variables para manejar el archivo actual
    private Uri currentFileUri = null; // Almacenará la Uri del archivo si se abre o guarda
    private String currentFileName = null; // Almacenará el nombre del archivo

    private static final int PICK_FILE_REQUEST_CODE = 1; // Código para abrir archivo
    private static final int CREATE_FILE_REQUEST_CODE = 2; // Código para guardar/crear archivo

    //Plantilla HTML
    String html;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        // Inflar el layout para este fragmento
        binding = FragmentNotasBinding.inflate(inflater, container, false);
        setHasOptionsMenu(true);

        View root = binding.getRoot();

        //Obtener elementos por binding
        nota = binding.editTextTextMultiLine;

        // Si hay una Uri guardada en el estado, cargar el archivo
        // Esto es útil si el Fragmento se recrea (por ejemplo, por rotación de pantalla)
        if (savedInstanceState != null) {
            String uriString = savedInstanceState.getString("currentFileUri");
            if (uriString != null) {
                currentFileUri = Uri.parse(uriString);
                currentFileName = savedInstanceState.getString("currentFileName");
                // Intentar recargar el contenido del archivo
                loadFileContent(currentFileUri);
            }
        }


        return root;
    }

    @Override
    public void onSaveInstanceState(@NonNull Bundle outState) {
        super.onSaveInstanceState(outState);
        // Guardar la Uri y el nombre del archivo actual en el estado
        if (currentFileUri != null) {
            outState.putString("currentFileUri", currentFileUri.toString());
            outState.putString("currentFileName", currentFileName);
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
        // Inflar el menú de opciones desde el archivo XML
        inflater.inflate(R.menu.notas, menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if(id == R.id.action_abrir) {
            // Acción para abrir un archivo existente
            openFilePicker();
            return true; // Consumir el evento

        } else if(id == R.id.action_guardar) {
            // Acción para guardar el archivo
            saveFile();
            return true; // Consumir el evento

        } else if(id == R.id.action_exportar_html) {
            html = "<html>\n" +
                    "    <head>\n" +
                    "        <title></title>\n" +
                    "        <style>\n" +
                    "            p{font-size:14px;}\n" +
                    "        </style>\n" +
                    "    </head>\n" +
                    "    <body>\n" +
                    "        <p>" + nota.getText().toString() + "</p>\n" +
                    "    </body>\n" +
                    "</html>";

            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("text/html");

            try {
                startActivityForResult(intent, 3);
            } catch(Exception e) {
                Toast.makeText(getContext(), "No se pudo abrir el diálogo de guardado: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }

        } else if(id == R.id.action_exportar_pdf) {
            html = "<html>\n" +
                    "    <head>\n" +
                    "        <title></title>\n" +
                    "        <style>\n" +
                    "            p{font-size:14px;}\n" +
                    "        </style>\n" +
                    "    </head>\n" +
                    "    <body>\n" +
                    "        <p>" + nota.getText().toString() + "</p>\n" +
                    "    </body>\n" +
                    "</html>";

            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("application/pdf");

            try {
                startActivityForResult(intent, 4);
            } catch(Exception e) {
                Toast.makeText(getContext(), "No se pudo abrir el diálogo de guardado: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }

        } else if(id == R.id.action_help) {
            AlertDialog.Builder builder =new AlertDialog.Builder(requireContext());
            builder.setTitle("Ayuda");
            builder.setMessage("Este apartado es un bloc de notas con el que puede tomar apuntes y exportarlo a donde sea (txt, html, pdf).");
            builder.setIcon(R.drawable.ic_ayuda);

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

    // Método para lanzar el Intent de seleccionar archivo
    private void openFilePicker() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.setType("text/plain"); // Solo archivos de texto plano
        intent.addCategory(Intent.CATEGORY_OPENABLE); // Solo archivos que se puedan abrir

        try {
            // Usar startActivityForResult con el código correcto
            startActivityForResult(Intent.createChooser(intent, "Selecciona un fichero TXT"), PICK_FILE_REQUEST_CODE);
        } catch (Exception e) {
            Log.e("NotasFragment", "Error al abrir el selector de archivos", e);
            Toast.makeText(getContext(), "No se pudo abrir el selector de archivos.", Toast.LENGTH_SHORT).show();
        }
    }

    // Método para lanzar el Intent de guardar/crear archivo
    private void saveFile() {
        if (currentFileUri != null) {
            // Si ya tenemos una Uri (archivo abierto previamente), guardar directamente en esa Uri
            writeFileContent(currentFileUri);
        } else {
            // Si no tenemos una Uri (archivo nuevo), lanzar el selector para crear un nuevo archivo
            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            intent.setType("text/plain"); // Tipo MIME para archivo de texto
            intent.addCategory(Intent.CATEGORY_OPENABLE); // Asegurarse de que se pueda abrir después de crear

            // Sugerir un nombre de archivo (opcional, el usuario puede cambiarlo)
            // Si ya tenemos un nombre de archivo (por ejemplo, si se abrió y se modificó), usar ese
            String suggestedFileName = (currentFileName != null && !currentFileName.isEmpty()) ? currentFileName : "nueva_nota.txt";
            intent.putExtra(Intent.EXTRA_TITLE, suggestedFileName);

            try {
                // Usar startActivityForResult con el código correcto
                startActivityForResult(intent, CREATE_FILE_REQUEST_CODE);
            } catch(Exception e) {
                Log.e("NotasFragment", "Error al abrir el diálogo de guardar archivo", e);
                Toast.makeText(getContext(), "No se pudo abrir el diálogo de guardar archivo.", Toast.LENGTH_SHORT).show();
            }
        }
    }


    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (resultCode == RESULT_OK && data != null && data.getData() != null) {
            Uri uri = data.getData(); // Obtiene la URI del archivo

            if (requestCode == PICK_FILE_REQUEST_CODE) {
                // Resultado de abrir archivo
                currentFileUri = uri; // Almacenar la Uri del archivo abierto
                currentFileName = getDisplayNameFromUri(getContext(), uri); // Almacenar el nombre

                // Leer el contenido del archivo
                loadFileContent(currentFileUri);

            } else if (requestCode == CREATE_FILE_REQUEST_CODE) {
                // Resultado de guardar/crear archivo
                currentFileUri = uri; // Almacenar la Uri del archivo creado
                currentFileName = getDisplayNameFromUri(getContext(), uri); // Almacenar el nombre

                // Escribir el contenido actual del EditText en el nuevo archivo
                writeFileContent(currentFileUri);

            } else if(requestCode == 3) {
                handleExportResult(data, "HTML");

            } else if(requestCode == 4) {
                handleExportResult(data, "PDF");
            }
        } else if (resultCode == Activity.RESULT_CANCELED) {
            // El usuario canceló la operación (abrir o guardar)
            Toast.makeText(getContext(), "Operación cancelada.", Toast.LENGTH_SHORT).show();
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
                            byte[] htmlBytes = html.getBytes("UTF-8");
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

    // Método para leer el contenido de un archivo dado su Uri
    private void loadFileContent(Uri uri) {
        if (uri == null || getContext() == null) {
            Toast.makeText(getContext(), "Uri inválida para leer archivo.", Toast.LENGTH_SHORT).show();
            return;
        }
        try {
            // Usar try-with-resources para asegurar que los streams se cierran
            try(InputStream inputStream = getContext().getContentResolver().openInputStream(uri);
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream))) {

                if (inputStream == null) {
                    Toast.makeText(getContext(), "No se pudo abrir el stream de entrada.", Toast.LENGTH_SHORT).show();
                    return;
                }

                StringBuilder stringBuilder = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    stringBuilder.append(line).append("\n");
                }
                String contenidoArchivo = stringBuilder.toString();
                nota.setText(contenidoArchivo);
                Toast.makeText(getContext(), "Archivo '" + currentFileName + "' cargado.", Toast.LENGTH_SHORT).show();
                Log.d("NotasFragment", "Archivo cargado: " + currentFileName);

            }
        } catch(FileNotFoundException e) {
            Log.e("NotasFragment", "Archivo no encontrado al leer: " + uri.toString(), e);
            Toast.makeText(getContext(), "Error: Archivo no encontrado.", Toast.LENGTH_SHORT).show();
        } catch(IOException e) {
            Log.e("NotasFragment", "Error de E/S al leer archivo: " + uri.toString(), e);
            Toast.makeText(getContext(), "Error al leer el archivo.", Toast.LENGTH_SHORT).show();
        } catch(SecurityException e) {
            Log.e("NotasFragment", "Error de seguridad al leer archivo: " + uri.toString(), e);
            Toast.makeText(getContext(), "Permiso denegado para leer el archivo.", Toast.LENGTH_SHORT).show();
        } catch(Exception ex) {
            Log.e("NotasFragment", "Error inesperado al leer archivo: " + uri.toString(), ex);
            Toast.makeText(getContext(), "Error al leer el archivo.", Toast.LENGTH_SHORT).show();
        }
    }

    // Método para escribir el contenido del EditText en un archivo dado su Uri
    private void writeFileContent(Uri uri) {
        if (uri == null || getContext() == null) {
            Toast.makeText(getContext(), "Uri inválida para guardar archivo.", Toast.LENGTH_SHORT).show();
            return;
        }
        try {
            // Usar try-with-resources para asegurar que los streams se cierran
            try(OutputStream outputStream = getContext().getContentResolver().openOutputStream(uri)) {

                if (outputStream == null) {
                    Toast.makeText(getContext(), "No se pudo abrir el stream de salida.", Toast.LENGTH_SHORT).show();
                    return;
                }

                outputStream.write(nota.getText().toString().getBytes());
                Toast.makeText(getContext(), "Archivo '" + currentFileName + "' guardado correctamente.", Toast.LENGTH_SHORT).show();
                Log.d("NotasFragment", "Archivo guardado: " + currentFileName);

            }
        } catch(FileNotFoundException e) {
            Log.e("NotasFragment", "Archivo no encontrado al guardar: " + uri.toString(), e);
            Toast.makeText(getContext(), "Error: Archivo no encontrado al guardar.", Toast.LENGTH_SHORT).show();
        } catch(IOException e) {
            Log.e("NotasFragment", "Error de E/S al guardar archivo: " + uri.toString(), e);
            Toast.makeText(getContext(), "Error al guardar el archivo.", Toast.LENGTH_SHORT).show();
        } catch(SecurityException e) {
            Log.e("NotasFragment", "Error de seguridad al guardar archivo: " + uri.toString(), e);
            Toast.makeText(getContext(), "Permiso denegado para guardar el archivo.", Toast.LENGTH_SHORT).show();
        } catch(Exception ex) {
            Log.e("NotasFragment", "Error inesperado al guardar archivo: " + uri.toString(), ex);
            Toast.makeText(getContext(), "Error al guardar el archivo.", Toast.LENGTH_SHORT).show();
        }
    }


    // Método para obtener el nombre de visualización de una Uri (funciona con SAF)
    public static String getDisplayNameFromUri(Context context, Uri uri) {
        if (uri == null || context == null) {
            return null;
        }
        String result = null;
        // Usar try-with-resources para asegurar que el cursor se cierra
        try (Cursor cursor = context.getContentResolver().query(uri, null, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                int columnIndex = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                if (columnIndex != -1) { // Verificar si la columna existe
                    result = cursor.getString(columnIndex);
                } else {
                    Log.w("NotasFragment", "Columna DISPLAY_NAME no encontrada para Uri: " + uri.toString());
                }
            } else {
                Log.w("NotasFragment", "Cursor es nulo o vacío para Uri: " + uri.toString());
            }
        } catch (Exception e) {
            Log.e("NotasFragment", "Error al obtener display name de Uri: " + uri.toString(), e);
        }
        // Si no se pudo obtener el nombre, intentar extraerlo de la propia Uri
        if (result == null) {
            String path = uri.getPath();
            if (path != null) {
                int cut = path.lastIndexOf('/');
                if (cut != -1) {
                    result = path.substring(cut + 1);
                } else {
                    result = path; // Si no hay barras, el path completo podría ser el nombre
                }
            }
        }
        return result;
    }
}
