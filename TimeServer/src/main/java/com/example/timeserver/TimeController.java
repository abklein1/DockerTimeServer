package com.example.timeserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TimeController {
	
	@RequestMapping(value = "/time", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
	public String getTime() {
		Timer timer = new Timer();
		return timer.getTime();
	}
}
