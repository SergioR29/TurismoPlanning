package com.tfg.myapplication.ui.actualidad;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import org.osmdroid.config.Configuration;
import org.osmdroid.util.GeoPoint;
import org.osmdroid.views.MapView;
import org.osmdroid.views.overlay.mylocation.GpsMyLocationProvider;
import org.osmdroid.views.overlay.mylocation.MyLocationNewOverlay;

import com.tfg.myapplication.R;
import com.tfg.myapplication.databinding.FragmentActualidadBinding;
import com.tfg.myapplication.clima.WeatherResponse;

import java.util.ArrayList;

import android.location.Address;
import android.location.Geocoder;
import java.io.IOException;
import java.util.List;
import java.util.Locale;
import android.os.AsyncTask;

public class ActualidadFragment extends Fragment {

    private MapView mapView = null;
    private ActualidadViewModel actualidadViewModel;
    private MyLocationNewOverlay locationOverlay;
    private static final int REQUEST_LOCATION_PERMISSION = 1;
    private FragmentActualidadBinding binding;

    // Elementos de UI para mostrar el clima
    private TextView ciudadTextView;
    private TextView temperaturaTextView;
    private ImageView weatherIconImageView;
    private GridLayout layoutClima;

    //Variables auxiliares
    String ciudadSeleccionada; // Usamos un nombre más descriptivo para el argumento

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        // **Configuración de OSMDroid (DEBE IR ANTES DE INFLAR EL MAPVIEW)**
        Configuration.getInstance().load(getContext(), PreferenceManager.getDefaultSharedPreferences(getContext()));
        Configuration.getInstance().setUserAgentValue(requireContext().getPackageName());

        // Usando ViewBinding para inflar el layout
        binding = FragmentActualidadBinding.inflate(inflater, container, false);
        View view = binding.getRoot();
        setHasOptionsMenu(true); // Si este fragmento tiene opciones de menú

        // **Obtener referencias a los elementos de la UI (MAPA y CLIMA) usando binding**
        mapView = binding.mapa;
        layoutClima = binding.gridLayoutClima;
        ciudadTextView = binding.ciudad;
        temperaturaTextView = binding.temperatura;
        weatherIconImageView = binding.imgClima;

        // **Configuración básica del MapView**
        mapView.setBuiltInZoomControls(true);
        mapView.setMultiTouchControls(true);

        // Configurar el MyLocationNewOverlay
        GpsMyLocationProvider locationProvider = new GpsMyLocationProvider(requireContext());
        locationOverlay = new MyLocationNewOverlay(locationProvider, mapView);

        // Añadir el overlay al mapa
        mapView.getOverlays().add(locationOverlay);

        // Opcional: Configurar un punto central inicial si no se tiene la ubicación aún
        // Este punto inicial se usará solo si no se recibe argumento de ciudad y no se obtiene ubicación de usuario
        // GeoPoint startPoint = new GeoPoint(40.416775, -3.703790); // Ejemplo: Madrid
        // mapView.getController().setCenter(startPoint);
        // mapView.getController().setZoom(10.0); // Zoom inicial


        // **<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< FLUJO DE OBTENCIÓN DE UBICACIÓN Y CLIMA >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>**

        // Obtener el argumento de la ciudad pasada desde SitiosFragment
        if(getArguments() != null) {
            ciudadSeleccionada = getArguments().getString("cityName"); // Obtener el argumento

            assert ciudadSeleccionada != null;
            if(ciudadSeleccionada.equals("Guadalajara")) {
                ciudadSeleccionada = "Guadalajara, Castilla-La Mancha, España";
            }
        }

        // runOnFirstFix se mantiene, PERO solo se ejecutará si no se recibió un argumento de ciudad.
        // Si se recibió un argumento, la lógica de geocodificación directa se encargará del centrado inicial.
        locationOverlay.runOnFirstFix(new Runnable() {
            @Override
            public void run() {
                // Esta lógica solo se ejecuta si NO se recibió un argumento de ciudad
                if (ciudadSeleccionada == null && locationOverlay.getMyLocation() != null && getActivity() != null) {
                    final GeoPoint currentLocation = locationOverlay.getMyLocation();
                    Log.d("ActualidadFragment", "Primera ubicación de usuario obtenida: " + currentLocation.getLatitude() + ", " + currentLocation.getLongitude());

                    // Mover el mapa a la primera ubicación obtenida (en el hilo principal de UI)
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mapView.getController().animateTo(currentLocation);
                            mapView.getController().setCenter(currentLocation);
                            mapView.getController().setZoom(15.0); // Ajusta el zoom
                            locationOverlay.disableFollowLocation();
                            Log.d("ActualidadFragment", "Mapa centrado en ubicación de usuario.");
                        }
                    });

                    // Realizar la Geocodificación Inversa en un hilo de segundo plano para obtener la ciudad
                    new GetCityFromLocationTask(getActivity(), actualidadViewModel).execute(currentLocation);

                } else if (ciudadSeleccionada == null && getActivity() != null) {
                    // Si no se recibió argumento y no se pudo obtener la primera ubicación
                    getActivity().runOnUiThread(() ->
                            Toast.makeText(getContext(), "No se pudo obtener la primera ubicación válida.", Toast.LENGTH_SHORT).show()
                    );
                    // Opcional: Centrar en un punto por defecto si no se obtiene ubicación de usuario
                    getActivity().runOnUiThread(() -> {
                        GeoPoint startPoint = new GeoPoint(40.416775, -3.703790); // Ejemplo: Madrid
                        mapView.getController().animateTo(startPoint);
                        mapView.getController().setCenter(startPoint);
                        mapView.getController().setZoom(10.0);
                    });
                }
            }
        });

        return view; // Devolvemos la vista raíz inflada por binding
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        // **Obtener instancia del ViewModel**
        actualidadViewModel = new ViewModelProvider(this).get(ActualidadViewModel.class);

        // **Observar el LiveData de los datos del clima del ViewModel**
        actualidadViewModel.getCurrentWeather().observe(getViewLifecycleOwner(), new Observer<WeatherResponse>() {
            @Override
            public void onChanged(WeatherResponse weatherResponse) {
                if (weatherResponse != null && weatherResponse.getWeather() != null && weatherResponse.getWeather().length > 0) {
                    // Si hay datos de clima válidos, actualizar la UI
                    ciudadTextView.setText(weatherResponse.getName()); // Nombre de ciudad de la respuesta API
                    temperaturaTextView.setText(Double.valueOf(weatherResponse.getMain().getTemp()).intValue() + "°C");

                    String iconCode = weatherResponse.getWeather()[0].getIcon();
                    int iconResourceId = mapWeatherIcon(iconCode);

                    if (iconResourceId != 0) {
                        weatherIconImageView.setImageResource(iconResourceId);
                    } else {
                        weatherIconImageView.setImageResource(R.drawable.ic_nodisponible); // Mi icono por defecto
                    }

                    Log.d("WeatherUpdate", "Clima actualizado para: " + weatherResponse.getName()); // Log útil

                } else {
                    // Si los datos del clima son nulos
                    ciudadTextView.setText("Ciudad: N/A");
                    temperaturaTextView.setText("Temp: N/A");
                    weatherIconImageView.setImageResource(R.drawable.ic_nodisponible);

                    // Mostrar un Toast solo la primera vez o si hay un error grave
                    Toast.makeText(getContext(), "No se pudo obtener el clima.", Toast.LENGTH_SHORT).show();
                }
            }
        });

        // **Iniciar la carga inicial del Clima y Ubicación**
        // Si se recibió un argumento de ciudad, usarlo. Si no, solicitar permisos de ubicación de usuario.
        if (ciudadSeleccionada != null && !ciudadSeleccionada.isEmpty() && !ciudadSeleccionada.equals("Seleccione una ciudad")) {
            Log.d("ActualidadFragment", "Argumento de ciudad recibido: " + ciudadSeleccionada + ". Buscando clima y ubicación...");
            // 1. Obtener clima para la ciudad seleccionada
            actualidadViewModel.fetchWeatherForCity(ciudadSeleccionada);
            // 2. Obtener coordenadas de la ciudad seleccionada y centrar el mapa
            new GetLocationFromCityTask(requireActivity(), mapView).execute(ciudadSeleccionada); // <-- Llamar a la tarea de geocodificación directa

        } else {
            Log.d("ActualidadFragment", "No se recibió argumento de ciudad. Solicitando ubicación de usuario...");
            // Si no se recibió argumento, solicitar permisos de ubicación de usuario
            requestLocationPermissions(); // Esto iniciará el proceso que eventualmente activará runOnFirstFix
        }


        // **El manejo del ciclo de vida en onResume, onPause, onDestroyView se mantiene igual.**
    }

    @Override
    public void onResume() {
        super.onResume();
        mapView.onResume();
        if (locationOverlay != null) {
            locationOverlay.enableMyLocation(); // Asegurarse de que el rastreo esté habilitado
        }
    }

    @Override
    public void onPause() {
        super.onPause();
        mapView.onPause();
        if (locationOverlay != null) {
            locationOverlay.disableMyLocation(); // Deshabilitar rastreo para ahorrar batería
            locationOverlay.disableFollowLocation(); // También dejar de seguir
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        mapView.onDetach(); // Liberar recursos del mapa
        binding = null; // Limpiar binding
    }


    // **Método para solicitar permisos de ubicación (mantenemos el que ya tenía)**
    private void requestLocationPermissions() {
        ArrayList<String> permissionsToRequest = new ArrayList<>();

        if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            permissionsToRequest.add(Manifest.permission.ACCESS_FINE_LOCATION);
        }
        if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_COARSE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            permissionsToRequest.add(Manifest.permission.ACCESS_COARSE_LOCATION);
        }

        if (!permissionsToRequest.isEmpty()) {
            ActivityCompat.requestPermissions(requireActivity(),
                    permissionsToRequest.toArray(new String[0]),
                    REQUEST_LOCATION_PERMISSION);
        } else {
            enableMyLocationOverlay(); // Permisos ya concedidos, habilitar overlay
        }
    }

    // **Manejar el resultado de la solicitud de permisos**
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_LOCATION_PERMISSION) {
            boolean allPermissionsGranted = true;
            for (int result : grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    allPermissionsGranted = false;
                    break;
                }
            }
            if (allPermissionsGranted) {
                enableMyLocationOverlay(); // Permisos concedidos, habilitar overlay
            } else {
                Toast.makeText(getContext(), "Permisos de ubicación denegados. No se mostrará tu ubicación.", Toast.LENGTH_SHORT).show();
                // Opcional: Deshabilitar funcionalidades que dependen de la ubicación
            }
        }
    }


    // **Método para habilitar el MyLocationNewOverlay (mantenemos y ajustamos ligeramente)**
    private void enableMyLocationOverlay() {
        if (locationOverlay != null && getContext() != null) { // Añadir verificación de contexto
            if (ContextCompat.checkSelfPermission(getContext(), Manifest.permission.ACCESS_FINE_LOCATION)
                    == PackageManager.PERMISSION_GRANTED) {
                locationOverlay.enableMyLocation(); // Empieza a rastrear la ubicación

                // Opcional: Si quiero que el mapa se centre y siga al usuario por defecto
                locationOverlay.enableFollowLocation(); // Habilitar si quiero que el mapa siga al usuario

            }
        }
    }

    // **Método para mapear el código de icono del clima (ajustado con Color de fondo)**
    private int mapWeatherIcon(String iconCode) {
        // Asegurarme de que 'layoutClima' no sea null antes de intentar cambiar su color
        if (layoutClima != null) {
            // Restablece el color de fondo por defecto si no es un icono de noche
            if (iconCode != null && !iconCode.endsWith("n")) {
                layoutClima.setBackgroundColor(Color.TRANSPARENT); // O mi color de fondo por defecto
            }
        }


        if (iconCode == null) {
            if (layoutClima != null) layoutClima.setBackgroundColor(Color.TRANSPARENT);
            return R.drawable.ic_nodisponible; // O mi icono por defecto
        }

        switch (iconCode) {
            case "01d":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#07acff"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_sunny_day;
            case "01n":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#0013b4"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_clear_night; // Noche: fondo azul
            case "02d":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#07acff"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_few_clouds_day;
            case "02n":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#0013b4"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_few_clouds_night;
            case "03d":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#07acff"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_scattered_clouds;
            case "03n":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#0013b4"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_scattered_clouds;
            case "04d":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#07acff"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_broken_clouds;
            case "04n":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#0013b4"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_broken_clouds;
            case "09d":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#07acff"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_shower_rain;
            case "09n":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#0013b4"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_shower_rain;
            case "10d":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#07acff"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_rain_day;
            case "10n":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#0013b4"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_rain_night;
            case "11d":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#07acff"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_thunderstorm;
            case "11n":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#0013b4"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_thunderstorm;
            case "13d":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#07acff"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_snow;
            case "13n":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#0013b4"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_snow;
            case "50d":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#07acff"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_mist;
            case "50n":
                if (layoutClima != null) {
                    layoutClima.setBackgroundColor(Color.parseColor("#0013b4"));
                    temperaturaTextView.setTextColor(Color.WHITE);
                    ciudadTextView.setTextColor(Color.WHITE);
                }
                return R.drawable.ic_mist;

            default:
                if (layoutClima != null) layoutClima.setBackgroundColor(Color.TRANSPARENT);
                return R.drawable.ic_nodisponible; // Icono por defecto
        }
    }

    // **Clase interna para Geocodificación Inversa (Coordenadas a Ciudad)**
    private static class GetCityFromLocationTask extends AsyncTask<GeoPoint, Void, String> {
        private Geocoder geocoder;
        private ActualidadViewModel viewModel;
        private FragmentActivity activity; // Mantenemos referencia a la Activity

        GetCityFromLocationTask(FragmentActivity activity, ActualidadViewModel viewModel) {
            this.activity = activity;
            this.viewModel = viewModel;
            geocoder = new Geocoder(activity.getApplicationContext(), Locale.getDefault());
        }

        @Override
        protected String doInBackground(GeoPoint... geoPoints) {
            if (geoPoints == null || geoPoints.length == 0 || geoPoints[0] == null) {
                return null;
            }
            GeoPoint location = geoPoints[0];
            String cityName = null;

            try {
                // getFromLocation realiza la geocodificación inversa. Le pedimos solo 1 resultado.
                List<Address> addresses = geocoder.getFromLocation(location.getLatitude(), location.getLongitude(), 1);

                // Extraer el nombre de la ciudad (Locality) del primer resultado, si existe.
                if (addresses != null && !addresses.isEmpty()) {
                    Address address = addresses.get(0);
                    cityName = address.getLocality(); // Locality suele ser el nombre de la ciudad

                    // Si Locality es nulo, probar con otros campos que a veces contienen la ciudad
                    if (cityName == null) {
                        cityName = address.getAdminArea(); // Podría ser estado/provincia
                    }
                    if (cityName == null) {
                        cityName = address.getSubAdminArea(); // Sub-localidad
                    }
                    Log.d("GeocodingTask", "Geocodificación inversa: Coordenadas " + location.getLatitude() + ", " + location.getLongitude() + " -> Ciudad: " + cityName);
                } else {
                    Log.d("GeocodingTask", "Geocodificación inversa: No se encontraron direcciones para " + location.getLatitude() + ", " + location.getLongitude());
                }
            } catch (IOException e) {
                e.printStackTrace();
                Log.e("GeocodingTask", "Error de E/S en geocodificación inversa", e);
            } catch (IllegalArgumentException e) {
                e.printStackTrace();
                Log.e("GeocodingTask", "Argumento inválido en geocodificación inversa", e);
            }
            return cityName; // Devuelve el nombre de la ciudad obtenido (o null si falla)
        }

        @Override
        protected void onPostExecute(String cityName) {
            super.onPostExecute(cityName);
            // Este método se ejecuta en el HILO PRINCIPAL DE LA UI después de que doInBackground termine.

            if (cityName != null && !cityName.isEmpty()) {
                // Si obtuvimos un nombre de ciudad válido, llamamos al ViewModel para que obtenga el clima.
                // Esto actualiza el LiveData en el ViewModel, lo que a su vez notifica al Observer en el Fragmento.
                viewModel.fetchWeatherForCity(cityName);
                // Opcional: Loggear que se está buscando clima para la ciudad
                Log.d("GeocodingTask", "Obtenida ciudad: " + cityName + ". Buscando clima...");
            } else {
                // Si no se pudo obtener el nombre de la ciudad, manejamos el error.
                // Por ejemplo, podemos mostrar un mensaje al usuario o cargar el clima de una ciudad por defecto.
                // Como estamos en AsyncTask (no en el Fragmento directamente), usamos la referencia a la Activity.
                if (activity != null) {
                    Toast.makeText(activity, "No se pudo determinar la ciudad para el clima.", Toast.LENGTH_SHORT).show();
                    // Opcional: Llamar a fetchWeatherForCity("Default City"); si quiero un fallback
                }
            }
        }
    }

    // **NUEVA Clase interna para Geocodificación Directa (Ciudad a Coordenadas)**
    private static class GetLocationFromCityTask extends AsyncTask<String, Void, GeoPoint> {
        private Geocoder geocoder;
        private MapView mapView;
        private FragmentActivity activity; // Mantenemos referencia a la Activity

        GetLocationFromCityTask(FragmentActivity activity, MapView mapView) {
            this.activity = activity;
            this.mapView = mapView;
            geocoder = new Geocoder(activity.getApplicationContext(), Locale.getDefault());
        }

        @Override
        protected GeoPoint doInBackground(String... cityNames) {
            if (cityNames == null || cityNames.length == 0 || cityNames[0] == null || cityNames[0].isEmpty()) {
                return null;
            }
            String cityName = cityNames[0];
            GeoPoint location = null;

            try {
                // getFromLocationName realiza la geocodificación directa. Le pedimos solo 1 resultado.
                List<Address> addresses = geocoder.getFromLocationName(cityName, 1);

                // Extraer las coordenadas del primer resultado, si existe.
                if (addresses != null && !addresses.isEmpty()) {
                    Address address = addresses.get(0);
                    location = new GeoPoint(address.getLatitude(), address.getLongitude());
                    Log.d("GeocodingTask", "Geocodificación directa: Ciudad " + cityName + " -> Coordenadas: " + location.getLatitude() + ", " + location.getLongitude());
                } else {
                    Log.d("GeocodingTask", "Geocodificación directa: No se encontraron coordenadas para la ciudad " + cityName);
                }
            } catch (IOException e) {
                e.printStackTrace();
                Log.e("GeocodingTask", "Error de E/S en geocodificación directa", e);
            } catch (IllegalArgumentException e) {
                e.printStackTrace();
                Log.e("GeocodingTask", "Argumento inválido en geocodificación directa", e);
            }
            return location; // Devuelve el GeoPoint obtenido (o null si falla)
        }

        @Override
        protected void onPostExecute(GeoPoint location) {
            super.onPostExecute(location);
            // Este método se ejecuta en el HILO PRINCIPAL DE LA UI.

            if (location != null) {
                // Si obtuvimos coordenadas válidas, centramos el mapa.
                if (activity != null && mapView != null) {
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mapView.getController().animateTo(location);
                            mapView.getController().setCenter(location);
                            mapView.getController().setZoom(15.0); // Ajusta el zoom según se necesite
                            Log.d("GeocodingTask", "Mapa centrado en la ubicación de la ciudad.");
                        }
                    });
                }
            } else {
                // Si no se pudo obtener la ubicación de la ciudad
                if (activity != null) {
                    Toast.makeText(activity, "No se pudo encontrar la ubicación de la ciudad en el mapa.", Toast.LENGTH_SHORT).show();
                    // Opcional: Centrar en un punto por defecto si falla la geocodificación
                    activity.runOnUiThread(() -> {
                        GeoPoint startPoint = new GeoPoint(40.416775, -3.703790); // Ejemplo: Madrid
                        mapView.getController().animateTo(startPoint);
                        mapView.getController().setCenter(startPoint);
                        mapView.getController().setZoom(10.0);
                    });
                }
            }
        }
    }
}
