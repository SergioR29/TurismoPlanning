package com.tfg.myapplication.utilidades;

import android.util.Base64; // Importar la clase Base64 de Android
import android.util.Log; // Importar Log (opcional para depuración)

public class DataUtils {

    /**
     * Convierte un array de bytes (Blob) a una cadena de texto codificada en Base64.
     *
     * @param byteArray El array de bytes que se desea codificar.
     * @return Una cadena de texto Base64 si la codificación es exitosa, o null si el array de bytes es nulo o vacío.
     */
    public static String byteArrayToBase64(byte[] byteArray) {
        // Verifica si el array de bytes es nulo o vacío
        if (byteArray == null || byteArray.length == 0) {
            Log.w("DataUtils", "El array de bytes es nulo o vacío, no se puede codificar a Base64.");
            return null;
        }

        try {
            // Codificar el array de bytes a Base64.
            // Usamos la bandera Base64.DEFAULT para la codificación estándar.
            // Puedo usar otras banderas como Base64.NO_WRAP si no quiero saltos de línea.
            String base64String = Base64.encodeToString(byteArray, Base64.DEFAULT);

            Log.d("DataUtils", "Array de bytes codificado a Base64. Longitud: " + base64String.length());

            return base64String;

        } catch (Exception e) {
            Log.e("DataUtils", "Error al codificar byte array a Base64", e);
            // Maneja cualquier excepción durante la codificación
            return null;
        }
    }

    // Opcional: Método inverso para decodificar Base64 a byte[]
    /**
     * Decodifica una cadena de texto Base64 a un array de bytes.
     *
     * @param base64String La cadena de texto Base64 que se desea decodificar.
     * @return Un array de bytes si la decodificación es exitosa, o null si la cadena Base64 es nula, vacía o inválida.
     */
    public static byte[] base64ToByteArray(String base64String) {
        // Verifica si la cadena Base64 es nula o vacía
        if (base64String == null || base64String.trim().isEmpty()) {
            Log.w("DataUtils", "La cadena Base64 es nula o vacía, no se puede decodificar.");
            return null;
        }

        try {
            // Decodificar la cadena Base64 a un array de bytes.
            // Usamos la misma bandera que se usó para codificar (Base64.DEFAULT).
            byte[] byteArray = Base64.decode(base64String, Base64.DEFAULT);

            Log.d("DataUtils", "Cadena Base64 decodificada a byte array. Longitud: " + (byteArray != null ? byteArray.length : 0));

            return byteArray;

        } catch (IllegalArgumentException e) {
            Log.e("DataUtils", "Error al decodificar cadena Base64: Cadena inválida.", e);
            // Maneja el caso donde la cadena Base64 no es válida
            return null;
        } catch (Exception e) {
            Log.e("DataUtils", "Error inesperado al decodificar cadena Base64", e);
            // Maneja cualquier otra excepción
            return null;
        }
    }
}
