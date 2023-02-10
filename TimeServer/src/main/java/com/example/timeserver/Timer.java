package com.example.timeserver;

import java.text.SimpleDateFormat;
import java.util.Date;

public class Timer {
	
	private static String dateTime = null;
	
	Timer(){
		
		SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
		Date date = new Date();
		
		dateTime = formatter.format(date);
	}
	
	public String getTime() {
		return dateTime;
	}
}
