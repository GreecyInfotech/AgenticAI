package com.bfsi.platform.tools;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = "com.bfsi.platform.tools")
public class ToolsApplication {
    public static void main(String[] args) {
        SpringApplication.run(ToolsApplication.class, args);
    }
}
