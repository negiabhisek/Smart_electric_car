package com.example.abhisek.nistev_login;

import android.app.Dialog;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.common.api.GoogleApiActivity;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class SelectionActivity extends AppCompatActivity implements View.OnClickListener {

    private FirebaseAuth mAuth;
    private Button buttonLogout;
    private Button buttonEditProfile;
    private DatabaseReference databaseReference;

    GoogleMap mGoogleMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_selection);

        if (googleServicesAvailable()){
            Toast.makeText(this,"Perfect !!!",Toast.LENGTH_SHORT).show();
        }
        gmap();


        mAuth = FirebaseAuth.getInstance();
        if (mAuth.getCurrentUser() == null){
            finish();
            startActivity(new Intent(getApplicationContext(),LoginActivity.class));
        }

        databaseReference = FirebaseDatabase.getInstance().getReference();
        FirebaseUser user = mAuth.getCurrentUser();
        buttonLogout = (Button) findViewById(R.id.ButtonLogout);
        buttonEditProfile = (Button) findViewById(R.id.buttonEditProfile);

        buttonLogout.setOnClickListener(this);
        buttonEditProfile.setOnClickListener(this);

    }

    private void gmap() {
        MapFragment mapFragment = (MapFragment) getFragmentManager().findFragmentById(R.id.fragmentMap);
        mapFragment.getMapAsync(new OnMapReadyCallback() {
            @Override
            public void onMapReady(GoogleMap googleMap) {
                mGoogleMap = googleMap;
                LatLng l1 = new LatLng(19.197942, 84.747215);
                CameraUpdate update = CameraUpdateFactory.newLatLngZoom(l1,15);
                mGoogleMap.moveCamera(update);
            }
        });
//        mGoogleMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
    }


    public boolean googleServicesAvailable(){
        GoogleApiAvailability api = GoogleApiAvailability.getInstance();
        int isAvailable = api.isGooglePlayServicesAvailable(this);
        if (isAvailable == ConnectionResult.SUCCESS){
            return true;
        }
        else if (api.isUserResolvableError(isAvailable)){
            Dialog dialog = api.getErrorDialog(this,isAvailable,0);
            dialog.show();
        }
        else {
            Toast.makeText(this,"Can't Connect to play services", Toast.LENGTH_LONG).show();
        }
        return false;
    }

    @Override
    public void onClick(View v) {
        if (v == buttonLogout){
            mAuth.signOut();
            finish();
            startActivity(new Intent(this,LoginActivity.class));
        }
        if (v == buttonEditProfile){
            startActivity(new Intent(this,ProfileActivity.class));
        }
    }
}
