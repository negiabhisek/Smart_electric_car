package com.example.abhisek.nistev_login;

/**
 * Created by Abhisek on 19/3/2017.
 */

public class MessageInformation {
    public String msg;
    public String sender;
    public String receiver;


    public MessageInformation(){}


    public MessageInformation(String msg, String sender, String receiver) {
        this.msg = msg;
        this.sender = sender;
        this.receiver = receiver;
    }

    public String getMsg()
    {
        return msg;
    }

    public String getReceiver() {
        return receiver;
    }

    public String getSender(){
        return sender;
    }

    public boolean isSent()
    {
        return UserListActivity.user.getUid().contentEquals(sender);
    }
}
