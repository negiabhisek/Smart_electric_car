package com.example.abhisek.nistev_login;

import android.app.ProgressDialog;
import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.LoginFilter;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import butterknife.BindView;
import butterknife.ButterKnife;;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    String[] blood = { "O+", "A+", "B+", "AB+", "O",  };

    @BindView(R.id.editTextName) EditText editTextName;
    @BindView(R.id.editTextAddress) EditText editTextAddress;
    @BindView(R.id.editTextEmail) EditText editTextEmail;
    @BindView(R.id.editTextMobile) EditText editTextMobile;
    @BindView(R.id.editTextPassword) EditText editTextPassword;
    @BindView(R.id.editTextRePassword) EditText editTextRePassword;
    @BindView(R.id.buttonSignup) Button buttonRegister;
    @BindView(R.id.textViewSignin) TextView textViewSignin;

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

        buttonRegister.setOnClickListener(this);
        textViewSignin.setOnClickListener(this);
    }

    private void registerUser(){
        final String name = editTextName.getText().toString().trim();
        final String address = editTextAddress.getText().toString().trim();
        String email = editTextEmail.getText().toString().trim();
        String mobile = editTextMobile.getText().toString().trim();
        String password = editTextPassword.getText().toString().trim();
        String rePassword = editTextRePassword.getText().toString().trim();

        final UserInformation userInformation = new UserInformation(name,address,mobile);

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
                    databaseReference.child(user.getUid()).setValue(userInformation);
                    if (mAuth.getCurrentUser() != null){
                        finish();
                        startActivity(new Intent(getApplicationContext(),ProfileActivity.class));
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

        return valid;
    }
}
