package com.example.abhisek.nistev_login;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;

public class ProfileActivity extends AppCompatActivity implements View.OnClickListener {

    private FirebaseAuth mAuth;
    private DatabaseReference databaseReference;
    private FirebaseDatabase database;
    private FirebaseUser user;

    private EditText editTextage;
    private Spinner spinnerGender;
    private EditText editTextOccupation;
    private EditText editTextMobile,editTextAddress;
    private Spinner spinnerBlood;
    private Button buttonSave;

    UserInformation userInformation;
    public static final String TAG = MainActivity.class.getSimpleName();

    private String blood,gender;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        editTextage = (EditText) findViewById(R.id.editTextAge);
        spinnerGender = (Spinner) findViewById(R.id.spinnerGender);
        editTextOccupation = (EditText) findViewById(R.id.editTextOccupation);
        editTextAddress = (EditText) findViewById(R.id.editTextAddress);
        editTextMobile = (EditText) findViewById(R.id.editTextMobile);
        spinnerBlood = (Spinner) findViewById(R.id.spinnerBlood);
        TextView textViewUserEmail = (TextView) findViewById(R.id.textViewUserEmail);
        buttonSave = (Button) findViewById(R.id.buttonSave);
        setSpinners();


        mAuth = FirebaseAuth.getInstance();
        if (mAuth.getCurrentUser() == null){
            Log.d("firebase", "user doesnot exists");
            finish();
            startActivity(new Intent(getApplicationContext(),LoginActivity.class));
        }
        Log.d("firebase", "creating instance ...");
        database = FirebaseDatabase.getInstance();
//        databaseReference = database.getReference();
        Log.d("firebase", "creating user");
        user = mAuth.getCurrentUser();
        Log.d("firebase", "creating reference");
        databaseReference = database.getReference(user.getUid());
        Log.d("firebase", "reference");
        textViewUserEmail.setText(String.format("Welcome %s", user.getEmail()));
        databaseReference.child("users").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                userInformation = dataSnapshot.getValue(UserInformation.class);
                System.out.println(userInformation);
                Log.d("firebase", "User data is changed!" + userInformation.address);
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                Log.d("firebase", "Failed to read value.", databaseError.toException());
            }
        });
//        editTextMobile.setText("999999");
//        editTextAddress.removeTextChangedListener((TextWatcher) this);
//        editTextAddress.setText(userInformation.address);
//        editTextAddress.addTextChangedListener((TextWatcher) this);

        buttonSave.setOnClickListener(this);
    }

    @Override
    protected void onDestroy()
    {
        super.onDestroy();
//        updateUserStatus(false);
    }

    @Override
    protected void onResume()
    {
        super.onResume();
        updateUserStatus(true);

    }

    private void updateUserStatus(boolean b) {
        database.getReference().child("users").child(user.getUid()).child("online").setValue(b);
    }

    private void setSpinners() {
        // Spinner Drop down elements
        List<String> categories = new ArrayList<String>();
        categories.add("Select ...");
        categories.add("A+");
        categories.add("B+");
        categories.add("AB+");
        categories.add("O+");
        categories.add("A-");
        categories.add("B-");
        categories.add("AB-");
        categories.add("O-");

        blood = "Select ...";

        // Creating adapter for spinner
        ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, categories);

        // Drop down layout style - list view with radio button
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        // attaching data adapter to spinner
        spinnerBlood.setAdapter(dataAdapter);

        List<String> categories1 = new ArrayList<String>();
        categories1.add("Select ...");
        categories1.add("Male");
        categories1.add("Female");
        categories1.add("Other");

        gender = "Select ...";
        // Creating adapter for spinner
        ArrayAdapter<String> dataAdapter1 = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, categories1);

        // Drop down layout style - list view with radio button
        dataAdapter1.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        // attaching data adapter to spinner
        spinnerGender.setAdapter(dataAdapter1);

        spinnerBlood.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                blood = parent.getItemAtPosition(position).toString();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                blood = "Select ...";
            }
        });
        spinnerGender.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                gender = parent.getItemAtPosition(position).toString();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                gender = "Select ...";
            }
        });
    }

    private void saveUserInformation(){
        String address = editTextAddress.getText().toString().trim();
        String mobile = editTextMobile.getText().toString().trim();
        String age = editTextage.getText().toString().trim();
        String occupation = editTextOccupation.getText().toString().trim();


//        databaseReference.child(user.getUid()).setValue(userInformation);


        databaseReference.child("address").setValue(address);
        databaseReference.child("mobile").setValue(mobile);
        databaseReference.child("age").setValue(age);
        databaseReference.child("occupation").setValue(occupation);
        databaseReference.child("blood").setValue(blood);
        databaseReference.child("gender").setValue(gender);


        Toast.makeText(this,"Information Saved Successfully...",Toast.LENGTH_SHORT).show();

        finish();
        startActivity(new Intent(this,SelectionActivity.class));
    }
    @Override
    public void onClick(View v) {

        if (v == buttonSave){
            saveUserInformation();
        }
    }
}
