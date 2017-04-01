package com.example.abhisek.nistev_login;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.ListView;
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

public class UserListActivity extends AppCompatActivity{

    private FirebaseAuth mAuth;
    private DatabaseReference databaseReference;
    private DatabaseReference databaseReferenceBlank;
    private FirebaseDatabase database;
    public static FirebaseUser user;

    private ArrayList<UserInformation> uList;
    private UserInformation userInformation;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_list);

        mAuth = FirebaseAuth.getInstance();
        user = mAuth.getCurrentUser();
        if (user == null){
            Log.d("firebase", "user doesnot exists");
            finish();
            startActivity(new Intent(getApplicationContext(),LoginActivity.class));
        }
        database = FirebaseDatabase.getInstance();
        databaseReference = database.getReference(user.getUid());
        databaseReferenceBlank = database.getReference();

    }

    @Override
    protected void onDestroy()
    {
        super.onDestroy();
//        updateUserStatus(Boolean.FALSE);
    }

    @Override
    protected void onResume()
    {
        super.onResume();
        loadUserList();
        updateUserStatus(Boolean.TRUE);

    }

    private void updateUserStatus(boolean b) {
        databaseReferenceBlank.child("users").child(user.getUid()).child("online").setValue(b);
    }

    private void loadUserList() {
        Log.e("debug","loaduserlist");
        final ProgressDialog dia = ProgressDialog.show(this, null,
                "Loading Users...");
        databaseReferenceBlank.child("users").addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                Log.e("debug","ondatachange");
                long size = dataSnapshot.getChildrenCount();
                Log.e("debug","getchildrencount"+size);
                if (size == 0){
                    Toast.makeText(UserListActivity.this,"No User Found",Toast.LENGTH_SHORT).show();
                    return;
                }
                uList = new ArrayList<UserInformation>();
                Log.e("debug","arraylist");
                for(DataSnapshot ds : dataSnapshot.getChildren()) {
                    Log.e("debug","snapshot loop");
                    UserInformation user_scanned = ds.getValue(UserInformation.class);
                    Log.e("debug","user information");
                    if(!user.getUid().contentEquals(user_scanned.id))
                        uList.add(user_scanned);
                    Log.e("debug","ulist add");
                }
                Toast.makeText(UserListActivity.this,""+uList.size(), Toast.LENGTH_SHORT).show();
                ListView list = (ListView) findViewById(R.id.list);
                list.setAdapter(new UserAdapter());
                Log.e("debug","setadapter");
                list.setOnItemClickListener(new AdapterView.OnItemClickListener() {

                    @Override
                    public void onItemClick(AdapterView<?> arg0,
                                            View arg1, int pos, long arg3)
                    {
                        Log.e("debug","onitemclicklistener "+uList.get(pos).getId());
                        if (uList.get(pos).isOnline())
                            startActivity(new Intent(UserListActivity.this,
                                Chat.class)
                                .putExtra(
                                "buddy_id", uList.get(pos).getId()));
                    }
                });

            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                Log.e("debug","cancelled");
            }
        });
        Log.e("debug","dismiss");
        dia.dismiss();
    }

    private class UserAdapter extends BaseAdapter{

        @Override
        public int getCount() {
            return uList.size();
        }

        @Override
        public UserInformation getItem(int position) {
            return uList.get(position);
        }

        @Override
        public long getItemId(int position) {
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            if (convertView == null)
                convertView = getLayoutInflater().inflate(R.layout.chat_item, null);

            UserInformation c = getItem(position);
            TextView lbl = (TextView) convertView;
            lbl.setText(c.getName());
            lbl.setCompoundDrawablesWithIntrinsicBounds(
                    c.isOnline() ? R.drawable.ic_online
                            : R.drawable.ic_offline, 0, R.drawable.arrow, 0);

            return convertView;
        }
    }
}

