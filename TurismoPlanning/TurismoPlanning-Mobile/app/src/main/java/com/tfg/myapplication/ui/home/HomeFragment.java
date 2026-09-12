package com.tfg.myapplication.ui.home;

import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.tfg.myapplication.R;
import com.tfg.myapplication.databinding.FragmentHomeBinding;

public class HomeFragment extends Fragment {
    private FragmentHomeBinding binding;
    private final String[] themeOptions = {"Modo Claro", "Modo Oscuro", "Predeterminado del Sistema"};
    // Variable para guardar el índice de la opción seleccionada
    private int selectedThemeIndex = 0; // Índice por defecto (podría ser el tema actual)

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        HomeViewModel homeViewModel =
                new ViewModelProvider(this).get(HomeViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();
        setHasOptionsMenu(true);

        /*final TextView textView = binding.textHome;
        homeViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);*/
        return root;
    }

    @Override
    public void onCreateOptionsMenu(@NonNull Menu menu, @NonNull MenuInflater inflater) {
        super.onCreateOptionsMenu(menu, inflater);
        // Inflar el menú de opciones desde el archivo XML
        inflater.inflate(R.menu.main, menu);
    }

    // Método para obtener el índice del tema actual guardado en SharedPreferences
    private int getCurrentThemeIndex() {
        SharedPreferences preferences = PreferenceManager.getDefaultSharedPreferences(getContext());
        int currentMode = preferences.getInt("theme_preference", AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM);

        // Mapear el modo actual a un índice del array themeOptions
        if (currentMode == AppCompatDelegate.MODE_NIGHT_NO) {
            return 0; // Tema claro
        } else if (currentMode == AppCompatDelegate.MODE_NIGHT_YES) {
            return 1; // Oscuro
        } else {
            return 2; // Predeterminado (FOLLOW_SYSTEM o AUTO_TIME)
        }
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if(id == R.id.ayudaMain) {
            AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
            builder.setTitle("Ayuda");
            builder.setMessage("Bienvenido a tu mejor organizador diario y guía turístico, para empezar haz clic a las 3 barras de la esquina superior-izquierda para ver todas las opciones disponibles de uso.\n\nPulsa al icono de 3 puntos situado en la esquina superior derecha para ver información adicional de la aplicación y cambiar entre varios temas (claro, oscuro y predeterminado por el sistema) en los ajustes de la sección de inicio.\n\nPulsa al botón de la esquina inferior derecha para volver al inicio de esta genial app.");
            builder.setIcon(R.drawable.ic_ayuda);

            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                }
            });

            AlertDialog dialog = builder.create();
            dialog.show();

        } else if(id == R.id.action_settings) {
            AlertDialog.Builder builder = new AlertDialog.Builder(requireContext(), R.style.elementosGenerales);
            builder.setTitle("Ajustes");
            builder.setIcon(R.drawable.ajustes);

            // Obtener el índice del tema actual para preseleccionar en el diálogo
            selectedThemeIndex = getCurrentThemeIndex();

            // Configurar la lista de opciones de selección única (radio buttons)
            builder.setSingleChoiceItems(themeOptions, selectedThemeIndex, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    // 'which' es el índice del elemento que el usuario ha seleccionado en la lista
                    selectedThemeIndex = which; // Guarda el índice seleccionado
                }
            });

            // Botón Positivo (Aceptar)
            builder.setPositiveButton("Aceptar", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int id) {
                    // Acción a realizar si el usuario pulsa "Aceptar"
                    applySelectedTheme(selectedThemeIndex); // Aplicar y guardar el tema seleccionado
                    dialog.dismiss(); // Cierra el diálogo
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

        } else if(id == R.id.action_info) {
            AlertDialog.Builder builder = new AlertDialog.Builder(requireContext());
            builder.setTitle("Más información");
            builder.setIcon(R.drawable.informacion);
            builder.setMessage("Esta aplicación ha sido diseñada para ayudar al usuario a organizarse en su día a día. También se le muestran unos sitios turísticos de interés al usuario además de poder orientarse mediante un mapa y tomar apuntes.\n\nAutor: Sergio Romero Tejedor\nVersión: 1.0\nFecha de Lanzamiento: 29/05/2025");

            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                }
            });

            AlertDialog dialogo = builder.create();
            dialogo.show();
        }
        return super.onOptionsItemSelected(item);
    }

    // Método para aplicar el tema seleccionado y guardarlo en SharedPreferences
    private void applySelectedTheme(int index) {
        int nightMode;
        SharedPreferences preferences = PreferenceManager.getDefaultSharedPreferences(getContext());
        SharedPreferences.Editor editor = preferences.edit();

        switch (index) {
            case 0: // Tema claro
                nightMode = AppCompatDelegate.MODE_NIGHT_NO;
                editor.putInt("theme_preference", nightMode);
                editor.apply(); // O commit()
                AppCompatDelegate.setDefaultNightMode(nightMode);
                break;
            case 1: // Oscuro
                nightMode = AppCompatDelegate.MODE_NIGHT_YES;
                editor.putInt("theme_preference", nightMode);
                editor.apply();
                AppCompatDelegate.setDefaultNightMode(nightMode);
                break;
            case 2: // Predeterminado (seguir sistema o automático)
                // Usamos FOLLOW_SYSTEM para seguir la configuración del sistema operativo
                nightMode = AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM;
                editor.putInt("theme_preference", nightMode);
                editor.apply();
                AppCompatDelegate.setDefaultNightMode(nightMode);
                break;
            // No hay 'default' necesario si el índice siempre será 0, 1 o 2
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}