package com.tfg.myapplication;

import android.os.Bundle;
import android.util.Log;
import android.view.*;

import com.google.android.material.navigation.NavigationView;

import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.snackbar.Snackbar;
import com.tfg.myapplication.databinding.ActivityMainBinding;

import android.database.*;
import android.database.sqlite.SQLiteDatabase;

import java.time.LocalDate;

public class MainActivity extends AppCompatActivity {

    private AppBarConfiguration mAppBarConfiguration;
    private ActivityMainBinding binding;

    private GestorBD gestorBD;
    private SQLiteDatabase DB;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        setSupportActionBar(binding.appBarMain.toolbar);
        binding.appBarMain.fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                /*Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null)
                        .setAnchorView(R.id.fab).show();*/
                NavController navController = Navigation.findNavController(MainActivity.this, R.id.nav_host_fragment_content_main);
                navController.navigate(R.id.nav_home);
            }
        });
        DrawerLayout drawer = binding.drawerLayout;
        NavigationView navigationView = binding.navView;

        mAppBarConfiguration = new AppBarConfiguration.Builder(
                R.id.nav_home, R.id.nav_sitios, R.id.nav_calendario, R.id.nav_notas, R.id.nav_categorias, R.id.nav_eventos)
                .setOpenableLayout(drawer)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        NavigationUI.setupActionBarWithNavController(this, navController, mAppBarConfiguration);
        NavigationUI.setupWithNavController(navigationView, navController);

        gestorBD = new GestorBD(this);
        try {
            DB = gestorBD.openDataBase();
            Log.i("MainActivity", "Base de datos abierta correctamente.");

            eliminarPasados();
        } catch (android.database.sqlite.SQLiteCantOpenDatabaseException e) {
            Log.e("MainActivity", "Error al abrir la base de datos en MainActivity:", e);
        }
    }

    private void eliminarPasados() {
        //Método que automáticamente elimina los eventos pasados en vista de la fecha de hoy
        try {
            LocalDate fechaHoy = LocalDate.now();
            String texto = fechaHoy.getDayOfMonth() + "/" + fechaHoy.getMonthValue() + "/" + fechaHoy.getYear();

            int borrados = DB.delete("Tareas", "Plazo_Fecha < '" + texto + "'", null);
            if(borrados > 0) {
                Log.i("Info", "Eventos pasados de fecha borrados");
            } else {
                Log.i("Info", "No hay eventos pasados de fecha");
            }
            Log.i("Fecha de hoy", texto);
        } catch(SQLException ex) {
            Log.e("Error", "Error al eliminar eventos pasados de fecha", ex);
        }
    }

    @Override
    public boolean onSupportNavigateUp() {
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        return NavigationUI.navigateUp(navController, mAppBarConfiguration)
                || super.onSupportNavigateUp();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if(gestorBD != null) {
            gestorBD.close();
        }
    }
}