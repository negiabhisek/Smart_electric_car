package com.example.abhisek.nistev_login;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import static com.example.abhisek.nistev_login.R.id.editTextName;

public class ProfileActivity extends AppCompatActivity implements View.OnClickListener {

    private FirebaseAuth mAuth;
    private DatabaseReference databaseReference;
    private FirebaseDatabase database;

    private EditText editTextMobile,editTextAddress;
    private Button buttonSave;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);
        mAuth = FirebaseAuth.getInstance();
        if (mAuth.getCurrentUser() == null){
            finish();
            startActivity(new Intent(getApplicationContext(),LoginActivity.class));
        }

        database = FirebaseDatabase.getInstance();
//        databaseReference = database.getReference();
        FirebaseUser user = mAuth.getCurrentUser();
        editTextAddress = (EditText) findViewById(R.id.editTextAddress);
        editTextMobile = (EditText) findViewById(R.id.editTextMobile);
        TextView textViewUserEmail = (TextView) findViewById(R.id.textViewUserEmail);
        textViewUserEmail.setText("Welcome "+user.getEmail());
        buttonSave = (Button) findViewById(R.id.buttonSave);

        buttonSave.setOnClickListener(this);
    }

    private void saveUserInformation(){
        String address = editTextAddress.getText().toString().trim();
        String mobile = editTextMobile.getText().toString().trim();

//        UserInformation userInformation = new UserInformation(address,mobile);

        FirebaseUser user = mAuth.getCurrentUser();

//        databaseReference.child(user.getUid()).setValue(userInformation);

        if (user != null) {
            databaseReference = database.getReference(user.getUid());
        }
        databaseReference.child("address").setValue(address);
        databaseReference.child("mobile").setValue(mobile);

        Toast.makeText(this,"Information Saved Successfully...",Toast.LENGTH_SHORT).show();
    }
    @Override
    public void onClick(View v) {

        if (v == buttonSave){
            saveUserInformation();
        }
    }
}
