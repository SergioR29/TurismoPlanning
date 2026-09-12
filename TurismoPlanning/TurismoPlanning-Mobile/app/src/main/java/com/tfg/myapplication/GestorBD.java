package com.tfg.myapplication;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import androidx.annotation.Nullable;

import java.io.*;

public class GestorBD extends SQLiteOpenHelper {

    private static String DB_PATH = ""; // Ruta a la carpeta de bases de datos de la aplicación
    private static final String DB_NAME = "datos.db"; // El nombre de mi archivo de base de datos en la carpeta assets
    private SQLiteDatabase myDataBase;
    private final Context myContext;
    private boolean dbCopied = false; // Bandera para evitar copia repetida

    public GestorBD(@Nullable Context context) {
        super(context, DB_NAME, null, 1);
        this.myContext = context;

        assert context != null;
        DB_PATH = context.getDatabasePath(DB_NAME).getPath();
        Log.i("GestorBD", "Constructor llamado. DB_PATH: " + DB_PATH);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // No necesitamos copiar la BD aquí, lo haremos en openDataBase
        Log.i("GestorBD", "onCreate llamado (pero la lógica de copia se mueve a openDataBase).");
    }

    /**
     * Comprueba si la base de datos ya existe.
     */
    public boolean checkDataBase() {
        Log.i("GestorBD", "checkDataBase() llamado. DB_PATH: " + DB_PATH);
        File dbFile = new File(DB_PATH);
        boolean exists = dbFile.exists();
        Log.i("GestorBD", "¿Existe el archivo de la base de datos? " + exists);
        return exists;
    }

    @Override
    public synchronized void close() {
        if (myDataBase != null) myDataBase.close();
        super.close();
    }

    /**
     * Copia la base de datos desde assets al sistema.
     */
    public void copyDataBase() throws IOException {
        Log.i("GestorBD", "copyDataBase() llamado.");
        InputStream myInput = null;
        OutputStream myOutput = null;
        try {
            myInput = myContext.getAssets().open(DB_NAME);
            Log.i("GestorBD", "Archivo de base de datos abierto desde assets: " + DB_NAME);
            myOutput = new FileOutputStream(DB_PATH);
            Log.i("GestorBD", "FileOutputStream creado en: " + DB_PATH);
            byte[] buffer = new byte[1024];
            int length;
            while ((length = myInput.read(buffer)) > 0) {
                myOutput.write(buffer, 0, length);
            }
            myOutput.flush();
            Log.i("GestorBD", "Base de datos copiada correctamente.");
            dbCopied = true; // Marca que la copia se realizó
        } catch (IOException e) {
            Log.e("GestorBD", "Error durante la copia de la base de datos:", e);
            throw e;
        } finally {
            if (myOutput != null) myOutput.close();
            if (myInput != null) myInput.close();
        }
    }

    public SQLiteDatabase openDataBase() {
        Log.i("GestorBD", "openDataBase() llamado. Intentando abrir en: " + DB_PATH);
        if (!dbCopied && !checkDataBase()) {
            try {
                this.getWritableDatabase(); // Forzar la creación de la carpeta databases
                copyDataBase();
            } catch (IOException e) {
                Log.e("GestorBD", "Error al copiar la base de datos en openDataBase:", e);
            }
        }
        myDataBase = SQLiteDatabase.openDatabase(DB_PATH, null, SQLiteDatabase.OPEN_READWRITE);
        return myDataBase;
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // Manejar las actualizaciones de la base de datos si es necesario
    }
}