package com.example.abhisek.nistev_login;

/**
 * Created by Abhisek on 9/3/2017.
 */

public class UserInformation {
    public String name;
    public String age;
    public String gender;
    public String occupation;
    public String address;
    public String mobile;
    public String blood;
    public String id;
    public Boolean online;

    public UserInformation(){

    }

    public UserInformation(String name, String age, String gender, String occupation, String address, String mobile, String blood, String id, Boolean online) {
        this.name = name;
        this.age = age;
        this.gender = gender;
        this.occupation = occupation;
        this.address = address;
        this.mobile = mobile;
        this.blood = blood;
        this.id = id;
        this.online = online;
    }

    public String getName() {
        return name;
    }

    public String getId() {
        return id;
    }

    public Boolean isOnline() {
        return online;
    }
}
