package com.example.abhisek.nistev_login;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
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

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import butterknife.BindView;
import butterknife.ButterKnife;

;

public class MainActivity extends AppCompatActivity implements View.OnClickListener, AdapterView.OnItemSelectedListener {

    @BindView(R.id.editTextName) EditText editTextName;
    @BindView(R.id.editTextAge) EditText editTextAge;
    @BindView(R.id.spinnerGender) Spinner spinnerGender;
    @BindView(R.id.editTextOccupation) EditText editTextOccupation;
    @BindView(R.id.editTextAddress) EditText editTextAddress;
    @BindView(R.id.editTextEmail) EditText editTextEmail;
    @BindView(R.id.editTextMobile) EditText editTextMobile;
    @BindView(R.id.spinnerBlood) Spinner spinnerBlood;
    @BindView(R.id.editTextPassword) EditText editTextPassword;
    @BindView(R.id.editTextRePassword) EditText editTextRePassword;
    @BindView(R.id.buttonSignup) Button buttonRegister;
    @BindView(R.id.textViewSignin) TextView textViewSignin;

    private String blood;
    private String gender;
    private ProgressDialog progressDialog;

    private DatabaseReference databaseReference;
    private FirebaseAuth mAuth;
    private FirebaseAuth.AuthStateListener mAuthListener;

    public static final String TAG = MainActivity.class.getSimpleName();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);

        progressDialog = new ProgressDialog(this);
        editTextName = (EditText) findViewById(R.id.editTextName);
        editTextAge = (EditText) findViewById(R.id.editTextAge);
        editTextOccupation = (EditText) findViewById(R.id.editTextOccupation);
        editTextAddress = (EditText) findViewById(R.id.editTextAddress);
        editTextEmail = (EditText) findViewById(R.id.editTextEmail);
        editTextMobile = (EditText) findViewById(R.id.editTextMobile);
        editTextPassword = (EditText) findViewById(R.id.editTextPassword);
        editTextRePassword = (EditText) findViewById(R.id.editTextRePassword);
        buttonRegister = (Button) findViewById(R.id.buttonSignup);
        textViewSignin = (TextView) findViewById(R.id.textViewSignin);

        databaseReference = FirebaseDatabase.getInstance().getReference();

        mAuth = FirebaseAuth.getInstance();
        mAuthListener = new FirebaseAuth.AuthStateListener() {
            @Override
            public void onAuthStateChanged(@NonNull FirebaseAuth firebaseAuth) {
                FirebaseUser user = firebaseAuth.getCurrentUser();
                if (user != null) {
                    // User is signed in
                    Log.d(TAG, "onAuthStateChanged:signed_in:" + user.getUid());
                } else {
                    // User is signed out
                    Log.d(TAG, "onAuthStateChanged:signed_out");
                }
                // ...
            }
        };

        if (mAuth.getCurrentUser() != null){
            finish();
            startActivity(new Intent(getApplicationContext(),SelectionActivity.class));
        }
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

        spinnerBlood.setOnItemSelectedListener(this);
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
        buttonRegister.setOnClickListener(this);
        textViewSignin.setOnClickListener(this);
    }

    private void registerUser(){
        final String name = editTextName.getText().toString().trim();
        final String age = editTextAge.getText().toString().trim();
        final String Gender = gender.trim();
        final String occupation = editTextOccupation.getText().toString().trim();
        final String address = editTextAddress.getText().toString().trim();
        final String email = editTextEmail.getText().toString().trim();
        final String mobile = editTextMobile.getText().toString().trim();
        final String password = editTextPassword.getText().toString().trim();
        final String Blood = blood.trim();


        if (!validate()){
            return;
        }
        final ProgressDialog progressDialog = new ProgressDialog(MainActivity.this,
                R.style.Theme_AppCompat_DayNight_Dialog);
        progressDialog.setMessage("Registering User...");
        progressDialog.show();
        mAuth.createUserWithEmailAndPassword(email,password)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
            @Override
            public void onComplete(@NonNull Task<AuthResult> task) {
                if (task.isSuccessful()){
                    FirebaseUser user = mAuth.getCurrentUser();
                    if (mAuth.getCurrentUser() != null){
                        final UserInformation userInformation = new UserInformation(name,age,Gender,occupation,address,mobile,Blood, user.getUid(),Boolean.TRUE);
                        databaseReference.child("users").child(user.getUid()).setValue(userInformation);
                        Log.d("firebase", "Database Created" + userInformation.address);
                        finish();
                        Log.d("firebase", "New activity running" + userInformation.address);
                        startActivity(new Intent(getApplicationContext(),SelectionActivity.class));
                    }
                    Toast.makeText(MainActivity.this,"Registered Successfully",Toast.LENGTH_SHORT).show();
                }
                else {
                    Toast.makeText(MainActivity.this,"Could not registered. Please try again.",Toast.LENGTH_SHORT).show();
                }
                progressDialog.dismiss();
            }
        });
    }


    @Override
    public void onClick(View v) {
        if (v == buttonRegister){
            registerUser();
        }
        if (v == textViewSignin){
            startActivity(new Intent(this, LoginActivity.class));
        }
    }

    @Override
    public void onStart() {
        super.onStart();
        mAuth.addAuthStateListener(mAuthListener);
    }

    @Override
    public void onStop() {
        super.onStop();
        if (mAuthListener != null) {
            mAuth.removeAuthStateListener(mAuthListener);
        }
    }

    public boolean validate() {
        boolean valid = true;

        String name = editTextName.getText().toString().trim();
        String age = editTextAge.getText().toString().trim();
        String occupation = editTextOccupation.getText().toString().trim();
        String address = editTextAddress.getText().toString().trim();
        String email = editTextEmail.getText().toString().trim();
        String mobile = editTextMobile.getText().toString().trim();
        String password = editTextPassword.getText().toString().trim();
        String reEnterPassword = editTextRePassword.getText().toString().trim();

        if (name.isEmpty() || name.length() < 3) {
            editTextName.setError("at least 3 characters");
            valid = false;
        } else {
            editTextName.setError(null);
        }

        if (age.isEmpty()) {
            editTextAge.setError("Enter Valid Age");
            valid = false;
        } else {
            editTextAge.setError(null);
        }

        if (occupation.isEmpty()) {
            editTextOccupation.setError("Enter Occupation");
            valid = false;
        } else {
            editTextOccupation.setError(null);
        }

        if (address.isEmpty()) {
            editTextAddress.setError("Enter Valid Address");
            valid = false;
        } else {
            editTextAddress.setError(null);
        }


        if (email.isEmpty() || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            editTextEmail.setError("enter a valid email address");
            valid = false;
        } else {
            editTextEmail.setError(null);
        }

        if (mobile.isEmpty() || mobile.length()!=10) {
            editTextMobile.setError("Enter Valid Mobile Number");
            valid = false;
        } else {
            editTextMobile.setError(null);
        }

        if (password.isEmpty() || password.length() < 4 || password.length() > 10) {
            editTextPassword.setError("between 4 and 10 alphanumeric characters");
            valid = false;
        } else {
            editTextPassword.setError(null);
        }

        if (reEnterPassword.isEmpty() || reEnterPassword.length() < 4 || reEnterPassword.length() > 10 || !(reEnterPassword.equals(password))) {
            editTextRePassword.setError("Password Do not match");
            valid = false;
        } else {
            editTextRePassword.setError(null);
        }

        if (blood.isEmpty() || Objects.equals(blood, "") || Objects.equals(blood, "Select ...")) {
            Toast.makeText(this,"Enter Valid Blood Group",Toast.LENGTH_SHORT).show();
            valid = false;
        } else {

        }

        if (gender.isEmpty() || Objects.equals(gender, "") || Objects.equals(gender, "Select ...")) {
            Toast.makeText(this,"Enter Valid Gender",Toast.LENGTH_SHORT).show();
            valid = false;
        } else {
        }

        return valid;
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        blood = parent.getItemAtPosition(position).toString();

        Log.d("bloody", "Selected Blood Group"+blood);
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {
        blood = "";

    }
}
