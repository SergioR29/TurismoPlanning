package com.tfg.myapplication.utilidades;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.util.Base64;
import android.util.Log;
import android.widget.ImageButton;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

public class ImageUtils {

    /**
     * Convierte la imagen de un ImageButton a un array de bytes (Blob).
     *
     * @param imageButton El ImageButton del que obtener la imagen.
     * @return Un array de bytes representando la imagen en formato PNG, o null si falla.
     */
    public static byte[] getImageButtonAsByteArray(ImageButton imageButton) {
        // Verifica si el ImageButton es nulo
        if (imageButton == null) {
            Log.e("ImageUtils", "ImageButton es nulo.");
            return null;
        }

        // Paso 1: Obtener el Drawable
        Drawable drawable = imageButton.getDrawable();

        // Verifica si el drawable no es nulo
        if (drawable == null) {
            Log.w("ImageUtils", "El ImageButton no tiene un drawable establecido.");
            return null;
        }

        // Paso 2: Convertir el Drawable a un Bitmap
        Bitmap bitmap = null;

        if (drawable instanceof BitmapDrawable) {
            // Si el drawable ya es un BitmapDrawable, obtener el bitmap directamente
            bitmap = ((BitmapDrawable) drawable).getBitmap();
        } else {
            // Si no es un BitmapDrawable (ej. VectorDrawable), dibujarlo en un nuevo bitmap
            try {
                // Crear un nuevo bitmap con el mismo tamaño que el drawable
                bitmap = Bitmap.createBitmap(
                        drawable.getIntrinsicWidth(),
                        drawable.getIntrinsicHeight(),
                        Bitmap.Config.ARGB_8888 // ARGB_8888 soporta transparencia
                );

                // Crear un Canvas para dibujar en el bitmap
                Canvas canvas = new Canvas(bitmap);

                // Establecer los límites del drawable
                drawable.setBounds(0, 0, canvas.getWidth(), canvas.getHeight());

                // Dibujar el drawable en el canvas (y en el bitmap)
                drawable.draw(canvas);

            } catch (IllegalArgumentException e) {
                Log.e("ImageUtils", "Error al crear el bitmap a partir del drawable: Dimensiones inválidas", e);
                return null;
            } catch (Exception e) {
                Log.e("ImageUtils", "Error inesperado al convertir drawable a bitmap", e);
                return null;
            }
        }

        // Verifica si se pudo crear el bitmap
        if (bitmap == null) {
            Log.e("ImageUtils", "No se pudo obtener o crear el bitmap a partir del drawable.");
            return null;
        }

        // Paso 3: Comprimir el Bitmap a un array de bytes (Blob)
        byte[] byteArray = null;
        ByteArrayOutputStream stream = null;

        try {
            stream = new ByteArrayOutputStream();

            // Comprimir el bitmap a PNG. PNG es sin pérdida y adecuado para iconos.
            // Si se usa JPEG (con pérdida, tamaño de archivo más pequeño para fotos), usar Bitmap.CompressFormat.JPEG y ajustar la calidad (ej. 80).
            boolean compressed = bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream); // Calidad 100 para PNG se ignora

            if (compressed) {
                byteArray = stream.toByteArray(); // Obtener el array de bytes
                Log.d("ImageUtils", "Bitmap comprimido exitosamente a byte array. Tamaño: " + byteArray.length + " bytes.");
            } else {
                Log.e("ImageUtils", "Error al comprimir el bitmap.");
            }

        } catch (Exception e) {
            Log.e("ImageUtils", "Error inesperado al comprimir el bitmap", e);
        } finally {
            // Asegurarse de cerrar el stream
            if (stream != null) {
                try {
                    stream.close();
                } catch (IOException e) {
                    Log.e("ImageUtils", "Error al cerrar el ByteArrayOutputStream", e);
                }
            }
        }

        // Devolver el array de bytes (Blob)
        return byteArray;
    }

    public static String imageButtonToBase64(ImageButton imageView) {
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

    /**
     * Convierte un array de bytes (Blob) a un Drawable.
     *
     * @param context El contexto de la aplicación o Activity/Fragmento.
     * @param byteArray El array de bytes que contiene los datos de la imagen.
     * @return Un objeto Drawable si la conversión es exitosa, o null si falla.
     */
    public static Drawable byteArrayToDrawable(Context context, byte[] byteArray) {
        // Verifica si el contexto o el array de bytes son nulos o vacíos
        if (context == null || byteArray == null || byteArray.length == 0) {
            Log.w("ImageUtils", "Context o byte array inválido para convertir a Drawable.");
            return null;
        }

        // Paso 1: Decodificar el array de bytes a un Bitmap
        Bitmap bitmap = null;
        try {
            // BitmapFactory.decodeByteArray(byte[], offset, length)
            bitmap = BitmapFactory.decodeByteArray(byteArray, 0, byteArray.length);
        } catch (Exception e) {
            Log.e("ImageUtils", "Error al decodificar byte array a Bitmap", e);
            // Maneja cualquier excepción durante la decodificación
            return null;
        }

        // Verifica si se pudo crear el Bitmap
        if (bitmap == null) {
            Log.e("ImageUtils", "BitmapFactory no pudo decodificar el byte array.");
            return null;
        }

        // Paso 2: Convertir el Bitmap a un BitmapDrawable
        Drawable drawable = null;
        try {
            // Necesito el contexto para crear un BitmapDrawable
            drawable = new BitmapDrawable(context.getResources(), bitmap);
        } catch (Exception e) {
            Log.e("ImageUtils", "Error al crear BitmapDrawable a partir de Bitmap", e);
            // Maneja cualquier excepción
            return null;
        }

        // Devuelve el Drawable resultante
        return drawable;
    }
}