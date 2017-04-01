package com.example.abhisek.nistev_login;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.text.InputType;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;

public class Chat extends AppCompatActivity {

    private EditText txt;
    private Button buttonSend;
    private Handler handler;
    private String buddy_id;
    private String buddy_name;
    private Bundle extras;
    private ArrayList<MessageInformation> messageList;
    private UserInformation buddy;
    private ChatAdapter adp;
    private FirebaseUser user;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);
        Log.e("debug","loaded chat");

        txt = (EditText) findViewById(R.id.txt);
        txt.setInputType(InputType.TYPE_CLASS_TEXT
                | InputType.TYPE_TEXT_FLAG_MULTI_LINE);
        buttonSend = (Button) findViewById(R.id.btnSend);

        messageList = new ArrayList<MessageInformation>();
        Log.e("debug","message list");
        ListView list = (ListView) findViewById(R.id.list);
        Log.e("debug","listview");
        adp = new ChatAdapter();
        list.setAdapter(adp);
        list.setTranscriptMode(AbsListView.TRANSCRIPT_MODE_ALWAYS_SCROLL);
        list.setStackFromBottom(true);

        user = FirebaseAuth.getInstance().getCurrentUser();
        if (user == null){
            finish();
            startActivity(new Intent(getApplicationContext(),LoginActivity.class));
        }

        extras = getIntent().getExtras();
        Log.e("debug","get extra");

        buddy_id = extras.getString("buddy_id");
        Log.e("debug","get string buddy");
        Toast.makeText(this,"Buddy id "+buddy_id,Toast.LENGTH_SHORT).show();
        Log.e("debug","hi buddy");

//        ActionBar actionBar = getActionBar();
//        if(actionBar != null)
//            actionBar.setTitle(buddy.getName());
        Log.e("debug","oncreate end");

        buttonSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.e("debug","onclick listener");
                sendMessage();
            }
        });
        Log.e("debug","oncreate setTouchNClick");


//        handler = new Handler();
//        handler.postDelayed(new Runnable() {
//            @Override
//            public void run() {
//                loadConversationList();
//                handler.postDelayed(this, 500);
//            }
//        },500);

    }

    @Override
    protected void onResume() {
        super.onResume();
        loadConversationList();
    }

    private void sendMessage() {
        Log.e("debug","sendmessage");
        if (txt.length()==0)
            return;
        Log.e("debug","text not null");
        String s =txt.getText().toString().trim();
        Log.e("debug","string "+s);
//        Log.e("debug","Buddy id"+buddy.getId());
        MessageInformation message = new MessageInformation(s,user.getUid(),buddy_id);
        Log.e("debug","message information");
        messageList.add(message);
        Log.e("debug","added to message list");
        final String key = FirebaseDatabase.getInstance()
                .getReference("messages")
                .push().getKey();
        Log.e("debug","key created");
        FirebaseDatabase.getInstance().getReference("message").child(key).setValue(message);
        Log.e("debug","message stored");
        txt.setText(null);
    }

    private void loadConversationList() {
        FirebaseDatabase.getInstance().getReference("message").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                for (DataSnapshot ds : dataSnapshot.getChildren()){
                    MessageInformation messageInformation = ds.getValue(MessageInformation.class);
                    if ((messageInformation.getReceiver().contentEquals(user.getUid()) && messageInformation.getSender().contentEquals(buddy_id))||(messageInformation.getReceiver().contentEquals(buddy_id) && messageInformation.getSender().contentEquals(user.getUid()))) {
                        messageList.add(messageInformation);

                        adp.notifyDataSetChanged();

                    }
                }
                Log.e("debug","Message found"+messageList.size());
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });
    }

    private class ChatAdapter extends BaseAdapter {

        /* (non-Javadoc)
         * @see android.widget.Adapter#getCount()
         */
        @Override
        public int getCount() {
            return messageList.size();
        }

        /* (non-Javadoc)
         * @see android.widget.Adapter#getItem(int)
         */
        @Override
        public MessageInformation getItem(int arg0) {
            return messageList.get(arg0);
        }

        /* (non-Javadoc)
         * @see android.widget.Adapter#getItemId(int)
         */
        @Override
        public long getItemId(int arg0) {
            return arg0;
        }

        /* (non-Javadoc)
         * @see android.widget.Adapter#getView(int, android.view.View, android.view.ViewGroup)
         */
        @SuppressLint("InflateParams")
        @Override
        public View getView(int pos, View v, ViewGroup arg2) {
            MessageInformation c = getItem(pos);
            if (c.isSent())
                v = getLayoutInflater().inflate(R.layout.chat_item_sent, null);
            else
                v = getLayoutInflater().inflate(R.layout.chat_item_rcv, null);

            TextView lbl = (TextView) v.findViewById(R.id.lbl2);

//            lbl = (TextView) v.findViewById(R.id.lbl2);
            lbl.setText(c.getMsg());

//            lbl = (TextView) v.findViewById(R.id.lbl3);

            return v;
        }

    }

    /* (non-Javadoc)
     * @see android.app.Activity#onOptionsItemSelected(android.view.MenuItem)
     */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == android.R.id.home) {
            finish();
        }
        return super.onOptionsItemSelected(item);
    }


}
