plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.tfg.myapplication"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.tfg.myapplication"
        minSdk = 27
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    buildFeatures {
        viewBinding = true
    }
}

dependencies {

    implementation(libs.appcompat)
    implementation(libs.material)
    implementation(libs.constraintlayout)
    implementation(libs.lifecycle.livedata.ktx)
    implementation(libs.lifecycle.viewmodel.ktx)
    implementation(libs.navigation.fragment)
    implementation(libs.navigation.ui)
    implementation(libs.play.services.maps)
    implementation(libs.firebase.firestore)
    testImplementation(libs.junit)
    androidTestImplementation(libs.ext.junit)
    androidTestImplementation(libs.espresso.core)
    implementation(libs.osmdroid.android)

    // Retrofit para las llamadas de red
    implementation(libs.retrofit)
    // Converter de Gson para Retrofit (para parsear JSON a objetos Java)
    implementation(libs.converter.gson)

    // Lifecycle extensions (para LiveData y ViewModel)
    implementation(libs.lifecycle.livedata)
    implementation(libs.colorpickerview)

    //iText (PDF)
    implementation(libs.itext7.core)
    implementation(libs.html2pdf)

    //Calendario
    implementation(libs.kalendarview)
}